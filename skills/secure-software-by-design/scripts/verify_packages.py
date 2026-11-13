#!/usr/bin/env python3
"""Check explicit public package candidates without installing code. Existence is not trust."""
import argparse
from datetime import datetime, timezone
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

LIMIT = 8 * 1024 * 1024


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def endpoint(ecosystem, name):
    if not isinstance(name, str) or len(name) > 214:
        raise ValueError('invalid-name')
    if ecosystem == 'pypi' and re.fullmatch(r'[A-Za-z0-9](?:[A-Za-z0-9._-]*[A-Za-z0-9])?', name):
        name = re.sub(r'[-_.]+', '-', name).lower()
        return 'https://pypi.org/pypi/' + name + '/json'
    if ecosystem == 'npm' and re.fullmatch(r'(?:@[a-z0-9][a-z0-9._-]*/)?[a-z0-9][a-z0-9._-]*', name):
        return 'https://registry.npmjs.org/' + urllib.parse.quote(name, safe='')
    if ecosystem == 'packagist' and re.fullmatch(r'[a-z0-9][a-z0-9_.-]*/[a-z0-9][a-z0-9_.-]*', name):
        return 'https://packagist.org/packages/' + name + '.json'
    raise ValueError('invalid-name-or-ecosystem')


def fetch(url):
    # Do not inherit proxy credentials, cookies, authentication handlers, or redirects.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    req = urllib.request.Request(url, headers={'Accept': 'application/json', 'User-Agent': 'secure-software-package-check/1'})
    with opener.open(req, timeout=10) as response:
        data = response.read(LIMIT + 1)
        if len(data) > LIMIT:
            raise ValueError('response-limit')
        return json.loads(data)


def date(value):
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
        return parsed.replace(tzinfo=timezone.utc) if parsed.tzinfo is None else parsed.astimezone(timezone.utc)
    except ValueError:
        return None


def check(item, young_days=90, fetcher=fetch, now=None):
    eco, name = item.get('ecosystem'), item.get('name')
    output = {'ecosystem': eco, 'name': name, 'existence': 'unknown', 'timestamp': None,
              'timestamp_kind': 'unknown', 'review_flags': [], 'trust': 'not-assessed'}
    url = endpoint(eco, name)
    output['registry_url'] = url
    try:
        data = fetcher(url)
        timestamp = None
        if eco == 'pypi':
            actual = data['info']['name']
            if re.sub(r'[-_.]+', '-', actual).lower() != re.sub(r'[-_.]+', '-', name).lower():
                raise ValueError('name-mismatch')
            timestamps = [date(f.get('upload_time_iso_8601') or f.get('upload_time'))
                          for files in data['releases'].values() for f in files]
            valid = [x for x in timestamps if x]
            timestamp = min(valid) if valid else None
            output['timestamp_kind'] = 'earliest-surviving-upload-not-project-creation'
        elif eco == 'npm':
            if data['name'] != name:
                raise ValueError('name-mismatch')
            timestamp = date(data.get('time', {}).get('created'))
            output['timestamp_kind'] = 'registry-created'
        else:
            if data['package']['name'] != name:
                raise ValueError('name-mismatch')
            timestamp = date(data['package'].get('time'))
            output['timestamp_kind'] = 'packagist-package-time'
        output['existence'] = 'exists'
        if timestamp:
            output['timestamp'] = timestamp.isoformat()
            age = ((now or datetime.now(timezone.utc)) - timestamp).total_seconds() / 86400
            output['observed_age_days'] = round(age, 2)
            if age < 0:
                output['review_flags'].append('future-timestamp')
            elif age < young_days:
                output['review_flags'].append('recent-timestamp-manual-review')
        else:
            output['review_flags'].append('date-unavailable-manual-review')
    except urllib.error.HTTPError as exc:
        exc.close()
        if exc.code == 404:
            output['existence'] = 'missing'
        else:
            output['review_flags'].append('registry-http-error-' + str(exc.code))
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        output['review_flags'].append('network-or-metadata-error')
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', help='JSON array of {ecosystem: pypi|npm|packagist, name: exact-name}. Public names only; requests disclose these names to official registries.')
    parser.add_argument('--young-days', type=int, default=90, help='Review threshold; age never establishes trust.')
    args = parser.parse_args()
    try:
        if not 0 <= args.young_days <= 36500:
            raise ValueError()
        with open(args.input, 'rb') as stream:
            raw = stream.read(1024 * 1024 + 1)
        if len(raw) > 1024 * 1024:
            raise ValueError()
        items = json.loads(raw)
        if not isinstance(items, list) or not 1 <= len(items) <= 100:
            raise ValueError()
        # Validate the full batch before making any requests.
        for item in items:
            if not isinstance(item, dict) or set(item) != {'ecosystem', 'name'}:
                raise ValueError()
            endpoint(item['ecosystem'], item['name'])
        results = [check(item, args.young_days) for item in items]
    except (OSError, ValueError, TypeError):
        print(json.dumps({'status': 'invalid-input', 'error': 'invalid-batch-no-sensitive-details'}))
        return 2
    print(json.dumps({'results': results, 'limitation': 'Metadata and age do not verify package safety, maintainer reputation, provenance, or version integrity.'}))
    if any(r['existence'] == 'unknown' for r in results):
        return 2
    return 1 if any(r['existence'] == 'missing' or r['review_flags'] for r in results) else 0


if __name__ == '__main__':
    sys.exit(main())
