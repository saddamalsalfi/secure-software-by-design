import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from urllib.error import HTTPError
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'skills' / 'secure-software-by-design' / 'scripts'))

import scan_diff_secrets as secrets
import verify_packages as packages


class PackageTests(unittest.TestCase):
    def test_names(self):
        self.assertIn('%40org%2Fpkg', packages.endpoint('npm', '@org/pkg'))
        for eco, name in [('npm', '../bad'), ('pypi', 'https://x'), ('packagist', 'a/b?x'), ('npm', 'bad name')]:
            with self.assertRaises(ValueError): packages.endpoint(eco, name)

    def test_dates(self):
        cases = [('npm', 'example', {'name': 'example', 'time': {'created': '2020-01-01T00:00:00Z'}}, 'registry-created'),
                 ('pypi', 'example', {'info': {'name': 'example'}, 'releases': {'1': [{'upload_time': '2020-01-01T00:00:00'}]}}, 'earliest-surviving-upload-not-project-creation'),
                 ('packagist', 'vendor/example', {'package': {'name': 'vendor/example', 'time': '2020-01-01T00:00:00+00:00'}}, 'packagist-package-time')]
        for eco, name, fixture, kind in cases:
            r = packages.check({'ecosystem': eco, 'name': name}, fetcher=lambda _: fixture)
            self.assertEqual(r['existence'], 'exists'); self.assertEqual(r['timestamp_kind'], kind)
            self.assertEqual(r['trust'], 'not-assessed')

    def test_errors(self):
        for code, expected in [(404, 'missing'), (429, 'unknown'), (500, 'unknown')]:
            def fail(_): raise HTTPError('https://registry.npmjs.org/example', code, 'error', {}, None)
            self.assertEqual(packages.check({'ecosystem': 'npm', 'name': 'example'}, fetcher=fail)['existence'], expected)
        for error in [TimeoutError(), ValueError()]:
            def fail(_): raise error
            self.assertEqual(packages.check({'ecosystem': 'npm', 'name': 'example'}, fetcher=fail)['existence'], 'unknown')
        self.assertEqual(packages.check({'ecosystem': 'npm', 'name': 'example'}, fetcher=lambda _: {})['existence'], 'unknown')
        r = packages.check({'ecosystem': 'npm', 'name': 'example'}, fetcher=lambda _: {'name': 'example', 'time': {'created': 123}})
        self.assertIn('date-unavailable-manual-review', r['review_flags'])

    def test_redirect_refused(self):
        self.assertIsNone(packages.NoRedirect().redirect_request(None, None, 302, "redirect", {}, "https://untrusted.invalid"))

    def test_recent(self):
        r = packages.check({'ecosystem': 'npm', 'name': 'example'}, fetcher=lambda _: {'name': 'example', 'time': {'created': '2025-01-01T00:00:00Z'}}, now=datetime(2025, 1, 2, tzinfo=timezone.utc))
        self.assertIn('recent-timestamp-manual-review', r['review_flags'])


class ScanTests(unittest.TestCase):
    def test_git_and_redaction(self):
        with tempfile.TemporaryDirectory() as folder:
            def git(*args): subprocess.run(['git', '-C', folder, *args], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            git('init'); git('config', 'user.name', 'Test'); git('config', 'user.email', 'test@example.invalid'); git('config', 'commit.gpgsign', 'false')
            p = Path(folder) / 'file.py'; p.write_text('x = 1\n'); git('add', '.'); git('commit', '-m', 'fixture')
            synthetic = 'AKIA' + 'A' * 16
            p.write_text('x = 1\nkey = "' + synthetic + '"\n')
            result = secrets.scan(folder)
            self.assertTrue(result['findings']); self.assertNotIn(synthetic, json.dumps(result))
            self.assertEqual(result['findings'][0]['line'], 2)
            git('add', '.'); self.assertTrue(secrets.scan(folder)['findings'])
            self.assertTrue(secrets.scan(folder, 'HEAD')['findings'])
            Path(folder, 'untracked.txt').write_text('-----BEGIN PRIVATE KEY-----\n')
            self.assertTrue(any(f['path'] == 'untracked.txt' for f in secrets.scan(folder, include_untracked=True)['findings']))
            Path(folder, 'binary.bin').write_bytes(b'\0binary')
            self.assertTrue(secrets.scan(folder, include_untracked=True)['incomplete'])

    def test_renamed_path_with_git_metacharacters(self):
        with tempfile.TemporaryDirectory() as folder:
            def git(*args):
                subprocess.run(['git', '-C', folder, *args], check=True,
                               stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

            git('init')
            fixture = Path(folder) / 'original.txt'
            git('config', 'user.name', 'Test')
            git('config', 'user.email', 'test@example.invalid')
            git('config', 'commit.gpgsign', 'false')
            synthetic = 'AKIA' + 'A' * 16
            fixture.write_text(
                'Binary files mentioned in prose\ntext \u2028 ' + synthetic + '\n', encoding='utf-8')
            git('add', '--', fixture.name)
            git('commit', '-m', 'fixture')
            renamed = 'literal[xyz].txt'
            git('mv', '--', fixture.name, renamed)
            result = secrets.scan(folder)
            self.assertEqual(result['incomplete'], [])
            self.assertEqual(result['findings'], [
                {'path': renamed, 'line': 2, 'rule': 'aws-access-key-id'}])

    def test_entropy(self):
        self.assertIn('high-entropy-candidate', secrets.rules('x = "AbCdEfGhIjKlMnOpQrStUvWxYz0123456789"'))
        self.assertFalse(secrets.rules('ordinary prose'))


if __name__ == '__main__': unittest.main()
