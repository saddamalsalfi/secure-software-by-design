"""Offline checks for the release layout and its packaged links."""
import json
from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'secure-software-by-design'
LINK = re.compile(r'\]\(([^)\s]+)\)')


class PackageLayoutTests(unittest.TestCase):
    def test_entrypoint(self):
        entrypoint = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
        lines = entrypoint.splitlines()
        self.assertEqual(lines[0], '---')
        # This package deliberately uses single-line fields without YAML extensions.
        end = lines.index('---', 1)
        fields = dict(line.split(': ', 1) for line in lines[1:end])
        self.assertEqual(set(fields), {'name', 'description', 'license'})
        self.assertEqual(fields['name'], SKILL.name)
        self.assertRegex(fields['name'], r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
        self.assertLessEqual(len(fields['name']), 64)
        self.assertTrue(0 < len(fields['description'].strip()) <= 1024)
        self.assertEqual(fields['license'], 'MIT')
        self.assertTrue((SKILL / 'LICENSE').is_file())
        self.assertTrue(any(line.strip() for line in lines[end+1:]))

    def test_local_links(self):
        docs = [*ROOT.glob('README*.md'), *(ROOT / 'docs').glob('*.md'), *SKILL.rglob('*.md')]
        self.assertGreater(len(docs), 3)
        for doc in docs:
            for link in LINK.findall(doc.read_text(encoding='utf-8')):
                url = urlsplit(link)
                if url.scheme or url.netloc or not url.path:
                    continue
                with self.subTest(doc=doc.relative_to(ROOT), link=link):
                    target = (doc.parent / unquote(url.path)).resolve()
                    # An installed skill must remain usable outside this checkout.
                    boundary = SKILL if doc.is_relative_to(SKILL) else ROOT
                    self.assertTrue(target.is_relative_to(boundary))
                    self.assertTrue(target.exists())

    def test_references_and_openai_assets_are_shipped(self):
        body = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
        for reference in (SKILL / 'references').glob('*.md'):
            with self.subTest(reference=reference.name):
                self.assertIn(reference.relative_to(SKILL).as_posix(), LINK.findall(body))
        metadata = (SKILL / 'agents' / 'openai.yaml').read_text(encoding='utf-8')
        for field in ('icon_small', 'icon_large'):
            with self.subTest(field=field):
                icon = re.search(rf'^  {field}: "(\./assets/[^"]+)"$', metadata, re.M)
                self.assertIsNotNone(icon)
                self.assertTrue((SKILL / icon[1]).is_file())
        self.assertIn(f'${SKILL.name}', metadata)

    def test_distribution_scripts_are_present(self):
        for script in ('scan_diff_secrets.py', 'verify_packages.py'):
            with self.subTest(script=script):
                self.assertTrue((SKILL / 'scripts' / script).is_file())


    def test_mcp_identity_and_distribution(self):
        cfg = json.loads((ROOT / 'mcp.json').read_text(encoding='utf-8'))
        registry = json.loads((ROOT / 'server.json').read_text(encoding='utf-8'))
        plugin = json.loads((ROOT / 'plugin.json').read_text(encoding='utf-8'))
        publisher = 'saddamalsalfi'
        name = f'io.github.{publisher}/{SKILL.name}'
        self.assertEqual(plugin['name'], SKILL.name)
        self.assertEqual(plugin['version'], registry['version'])
        self.assertEqual(registry['name'], name)
        self.assertEqual(len(registry['packages']), 1)
        pkg = registry['packages'][0]
        self.assertEqual(pkg['registryType'], 'oci')
        self.assertEqual(pkg['transport'], {'type': 'stdio'})
        self.assertEqual(pkg['identifier'], f"ghcr.io/{publisher}/{SKILL.name}:{registry['version']}")
        self.assertEqual(set(cfg['mcpServers']), {SKILL.name})
        launch = cfg['mcpServers'][SKILL.name]
        self.assertEqual(launch['type'], 'stdio')
        self.assertIn('--locked', launch['args'])
        self.assertIn('\x24{PLUGIN_ROOT}/server.py', launch['args'])
        docker = (ROOT / 'Dockerfile').read_text(encoding='utf-8')
        self.assertIn(f'io.modelcontextprotocol.server.name="{name}"', docker)
        self.assertIn(f"org.opencontainers.image.version=\x22{registry['version']}\x22", docker)
        self.assertIn('USER 10001:10001', docker)
