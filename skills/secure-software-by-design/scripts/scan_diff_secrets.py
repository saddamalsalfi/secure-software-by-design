#!/usr/bin/env python3
"""Heuristic added-line scanner. Reports locations/rules, never matched values."""
import argparse
import collections
import json
import math
from pathlib import Path
import re
import subprocess
import sys

LIMIT = 8 * 1024 * 1024
PATTERNS = {
    'private-key-header': re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----'),
    'aws-access-key-id': re.compile(r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b'),
    'github-token': re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})\b'),
    'provider-token': re.compile(r'\b(?:sk_live_|sk-proj-|xox[baprs]-)[A-Za-z0-9_-]{16,}'),
    'credential-assignment': re.compile(r'''(?i)(?:api[_-]?key|secret|password|access[_-]?token)\s*[=:]\s*["'][^"'\s]{12,}["']'''),
}
TOKEN = re.compile(r'[A-Za-z0-9_+/=-]{24,}')


def rules(line):
    result = [name for name, pattern in PATTERNS.items() if pattern.search(line)]
    for match in TOKEN.finditer(line):
        value = match.group()
        if len(value) > 256:
            continue
        entropy = -sum((n / len(value)) * math.log2(n / len(value)) for n in collections.Counter(value).values())
        if entropy >= 4.5:
            result.append('high-entropy-candidate')
            break
    return result


def git(root, *args):
    p = subprocess.run(['git', '--literal-pathspecs', '-C', str(root), *args], stdout=subprocess.PIPE,
                       stderr=subprocess.DEVNULL, timeout=30, check=True)
    if len(p.stdout) > LIMIT:
        raise ValueError('limit')
    return p.stdout


def scan(root, base=None, include_untracked=False):
    findings, incomplete = [], []
    sets = [['diff', '--cached'], ['diff']] if base is None else [['diff', base]]
    if base is not None:
        git(root, 'rev-parse', '--verify', '--end-of-options', base + '^{commit}')
    for prefix in sets:
        prefix = [*prefix, '--no-renames', '--no-ext-diff', '--no-textconv']
        paths = git(root, *prefix, '--name-only', '-z', '--diff-filter=ACMRT', '--').split(b'\0')
        for raw in filter(None, paths):
            path = raw.decode('utf-8', 'surrogateescape')
            patch = git(root, *prefix, '--no-color', '--unified=0', '--', path)
            if any(line.startswith((b'Binary files ', b'GIT binary patch')) for line in patch.split(b'\n')):
                incomplete.append({'path': path, 'reason': 'binary-not-scanned'})
                continue
            try:
                lines = patch.decode('utf-8').split('\n')
            except UnicodeError:
                incomplete.append({'path': path, 'reason': 'non-utf8-not-scanned'})
                continue
            number = None
            for line in lines:
                hunk = re.match(r'^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@', line)
                if hunk:
                    number = int(hunk.group(1)); continue
                if number is None:
                    continue
                if line.startswith('+'):
                    findings.extend({'path': path, 'line': number, 'rule': rule} for rule in rules(line[1:]))
                    number += 1
                elif line.startswith(' '):
                    number += 1
    if include_untracked:
        for raw in filter(None, git(root, 'ls-files', '--others', '--exclude-standard', '-z').split(b'\0')):
            path = raw.decode('utf-8', 'surrogateescape')
            target = Path(root) / path
            if target.is_symlink() or not target.is_file() or target.stat().st_size > LIMIT:
                incomplete.append({'path': path, 'reason': 'unsupported-or-oversize'}); continue
            try:
                data = target.read_bytes()
                if b'\0' in data:
                    raise UnicodeError()
                lines = data.decode('utf-8').split('\n')
            except (UnicodeError, OSError):
                incomplete.append({'path': path, 'reason': 'unreadable-or-binary'}); continue
            for number, line in enumerate(lines, 1):
                findings.extend({'path': path, 'line': number, 'rule': rule} for rule in rules(line))
    unique = {json.dumps(item, sort_keys=True): item for item in findings}
    return {'status': 'incomplete' if incomplete else ('findings' if findings else 'no-findings'),
            'findings': list(unique.values()), 'incomplete': incomplete}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', default='.', help='Authorized Git repository; no network access.')
    parser.add_argument('--base', help='Compare a commit ref to working tree; default scans staged and unstaged changes separately.')
    parser.add_argument('--include-untracked', action='store_true', help='Include nonignored untracked regular UTF-8 files; ignored files are excluded.')
    args = parser.parse_args()
    try:
        root = git(args.repo, 'rev-parse', '--show-toplevel').decode().strip()
        if args.base and args.base.startswith('-'):
            raise ValueError('invalid ref')
        result = scan(root, args.base, args.include_untracked)
    except (OSError, ValueError, subprocess.SubprocessError):
        print(json.dumps({'status': 'incomplete', 'error': 'scan-failed-no-sensitive-details'}))
        return 2
    print(json.dumps(result, ensure_ascii=True))
    return 2 if result['incomplete'] else (1 if result['findings'] else 0)


if __name__ == '__main__':
    sys.exit(main())
