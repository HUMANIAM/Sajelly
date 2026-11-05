"""Git evidence tooling and PR-contract acceptance tests, no network required."""
from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from local_git_evidence import safe_path  # noqa: E402
from review_contract import validate  # noqa: E402


def cmd(*args, cwd):
    return subprocess.check_output(list(args), cwd=cwd, text=True).strip()


def tool(repo, *args):
    p = subprocess.run([sys.executable, str(ROOT / 'tools/local_git_evidence.py'), '--repo', str(repo), *args],
                       capture_output=True, text=True)
    return p.returncode, json.loads(p.stdout if p.returncode == 0 else p.stderr)


class ToolManifestTests(unittest.TestCase):
    def test_readonly_manifest_covers_review_window(self):
        manifest=json.loads((ROOT/'common/reviewer_tools.json').read_text())
        self.assertEqual('read_only', manifest['default_permission'])
        present={c['id'] for c in manifest['capabilities']}
        self.assertTrue({'change_context','changed_files','diff','file_at_revision','review_discussion','ci_evidence'}.issubset(present))
        allowed={name for c in manifest['capabilities'] for name in c['github_actions']}
        self.assertFalse(allowed.intersection(manifest['forbidden_github_actions']))
        self.assertIn('add_review_to_pr', manifest['forbidden_github_actions'])


class GitEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.repo = Path(self.t.name)
        cmd('git', 'init', '-q', cwd=self.repo)
        cmd('git', 'config', 'user.email', 'test@example.test', cwd=self.repo)
        cmd('git', 'config', 'user.name', 'Test', cwd=self.repo)
        (self.repo / 'src').mkdir()
        (self.repo / 'src/feature.py').write_text('def answer():\n    return 1\n')
        cmd('git', 'add', '.', cwd=self.repo)
        cmd('git', 'commit', '-qm', 'base', cwd=self.repo)
        self.base = cmd('git', 'rev-parse', 'HEAD', cwd=self.repo)
        (self.repo / 'src/feature.py').write_text('def answer():\n    return 2\n')
        cmd('git', 'add', '.', cwd=self.repo)
        cmd('git', 'commit', '-qm', 'change value', cwd=self.repo)
        self.head = cmd('git', 'rev-parse', 'HEAD', cwd=self.repo)

    def tearDown(self):
        self.t.cleanup()

    def test_overview_returns_immutable_shas_and_changed_files(self):
        rc, data = tool(self.repo, 'overview', '--base', self.base)
        self.assertEqual(0, rc, data)
        self.assertEqual(self.head, data['head_sha'])
        self.assertEqual(self.base, data['merge_base_sha'])
        self.assertEqual('src/feature.py', data['changed_files'][0]['path'])

    def test_diff_and_file_return_real_evidence(self):
        rc, diff = tool(self.repo, 'diff', '--base', self.base, '--path', 'src/feature.py')
        self.assertEqual(0, rc, diff)
        self.assertIn('+    return 2', diff['patch']['text'])
        self.assertFalse(diff['patch']['truncated'])
        rc, content = tool(self.repo, 'file', '--revision', self.base, '--path', 'src/feature.py')
        self.assertEqual(0, rc, content)
        self.assertIn('return 1', content['content']['text'])

    def test_history_is_read_only(self):
        rc, history = tool(self.repo, 'history', '--path', 'src/feature.py')
        self.assertEqual(0, rc, history)
        self.assertIn('change value', history['history']['text'])
        self.assertEqual(self.head, cmd('git', 'rev-parse', 'HEAD', cwd=self.repo))
        self.assertEqual('', cmd('git', 'status', '--porcelain', cwd=self.repo))

    def test_invalid_path_rejected(self):
        for bad in ('../credentials', '/etc/passwd', '-c', 'src/../test', 'src\\file'):
            with self.subTest(path=bad):
                with self.assertRaises(Exception):
                    safe_path(bad)

    def test_invalid_sha_reports_failure_not_fabricated_diff(self):
        rc, result = tool(self.repo, 'diff', '--base', 'missing-tag')
        self.assertNotEqual(0, rc)
        self.assertIn('error', result)

    def test_github_pr_locator_allows_reviewer_discovery_of_changed_files(self):
        for stack in ('frontend', 'backend'):
            req=json.loads((ROOT/stack/'examples/request.json').read_text())
            req['change']['changed_files']=[]
            req['change']['diff']={'kind':'pull_request','value':'example/repository#12'}
            validate('request', stack, req)
            invalid=copy.deepcopy(req)
            invalid['change']['diff']={'kind':'git_range','value':'base..head'}
            with self.assertRaisesRegex(ValueError, 'schema invalid'):
                validate('request', stack, invalid)


if __name__ == '__main__':
    unittest.main()
