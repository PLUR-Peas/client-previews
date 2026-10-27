"""Regression tests for accidental disclosure and unintended release boundaries."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import shutil
import uuid
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from public_policy import approved_files, export_projects, validate_artifact
from check_release import check_release
from install_gitleaks import verify_archive


class PublicationTests(unittest.TestCase):
    def setUp(self):
        # Python 3.13's Windows mode=0700 temp directories conflict with restricted
        # desktop tokens. Use an isolated workspace directory with inherited ACLs.
        self.base = Path(__file__).resolve().parents[1] / '.test-work'
        self.root = self.base / uuid.uuid4().hex
        self.root.mkdir(parents=True)
        self.addCleanup(self.cleanup_workspace)
        self.public = self.root / 'public'
        self.public.mkdir()
        (self.public / 'index.html').write_text('public index', encoding='utf-8')
        self.approved = {'index.html', 'version.json'}

    def cleanup_workspace(self):
        if self.root.resolve().parent != self.base.resolve():
            raise ValueError('Refusing cleanup outside the test workspace')
        shutil.rmtree(self.root)

    def policy(self, paths):
        path = self.root / 'policy.json'
        path.write_text(json.dumps({'version': 1, 'files': paths}), encoding='utf-8')
        return path

    def symlink(self, link, target, directory=False):
        try:
            link.symlink_to(target, target_is_directory=directory)
        except OSError:
            self.skipTest('OS does not allow this account to create symlinks')

    def test_reviewed_artifact_accepts_missing_generated_manifest(self):
        validate_artifact(self.public, self.approved)

    def test_rejects_extra_personal_data_file(self):
        (self.public / 'customers.json').write_text('[]', encoding='utf-8')
        with self.assertRaises(ValueError):
            validate_artifact(self.public, self.approved)

    def test_rejects_missing_reviewed_file(self):
        with self.assertRaises(ValueError):
            validate_artifact(self.public, self.approved | {'site.js'})

    def test_rejects_hidden_directory_even_when_empty(self):
        (self.public / '.git').mkdir()
        with self.assertRaises(ValueError):
            validate_artifact(self.public, self.approved)

    def test_rejects_unsafe_policy_paths(self):
        for path in ('../outside.js', '/outside.js', 'a/../../outside.js',
                     'a\\outside.js', '.env', 'a/.private/site.js',
                     'a//site.js', 'a/./site.js', 'a/key.pem', 'C:/site.js'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                approved_files(self.policy(['index.html', 'version.json', path]))

    def test_rejects_duplicate_policy_paths(self):
        with self.assertRaises(ValueError):
            approved_files(self.policy(['index.html', 'version.json', 'index.html']))

    def test_rejects_symlink_file_to_outside_artifact(self):
        outside = self.root / 'private.json'
        outside.write_text('private', encoding='utf-8')
        self.symlink(self.public / 'data.json', outside)
        with self.assertRaises(ValueError):
            validate_artifact(self.public, self.approved | {'data.json'})

    def test_rejects_symlink_directory_to_outside_artifact(self):
        outside = self.root / 'private'
        outside.mkdir()
        self.symlink(self.public / 'assets', outside, directory=True)
        with self.assertRaises(ValueError):
            validate_artifact(self.public, self.approved)

    def test_export_ignores_unapproved_source_material(self):
        source = self.root / 'source'
        source.mkdir()
        (source / 'index.html').write_text('approved', encoding='utf-8')
        (source / 'client-contract.txt').write_text('private', encoding='utf-8')
        (self.root / 'local-projects.json').write_text(json.dumps({'demo': 'source'}))
        export_projects(self.root, self.public, self.approved | {'demo/index.html'})
        self.assertEqual((self.public / 'demo/index.html').read_text(), 'approved')
        self.assertFalse((self.public / 'demo/client-contract.txt').exists())

    def test_missing_source_does_not_partially_overwrite_export(self):
        source = self.root / 'source'
        source.mkdir()
        (source / 'index.html').write_text('new', encoding='utf-8')
        target = self.public / 'demo'
        target.mkdir()
        (target / 'index.html').write_text('old', encoding='utf-8')
        (self.root / 'local-projects.json').write_text(json.dumps({'demo': 'source'}))
        with self.assertRaises(ValueError):
            export_projects(self.root, self.public,
                            self.approved | {'demo/index.html', 'demo/missing.js'})
        self.assertEqual((target / 'index.html').read_text(), 'old')

    def test_export_rejects_symlink_destination(self):
        source = self.root / 'source'
        source.mkdir()
        (source / 'index.html').write_text('new', encoding='utf-8')
        outside = self.root / 'outside'
        outside.mkdir()
        (outside / 'index.html').write_text('untouched', encoding='utf-8')
        self.symlink(self.public / 'demo', outside, directory=True)
        (self.root / 'local-projects.json').write_text(json.dumps({'demo': 'source'}))
        with self.assertRaises(ValueError):
            export_projects(self.root, self.public, self.approved | {'demo/index.html'})
        self.assertEqual((outside / 'index.html').read_text(), 'untouched')

    def test_export_rejects_symlink_source_root(self):
        source = self.root / 'source'
        source.mkdir()
        (source / 'index.html').write_text('private', encoding='utf-8')
        self.symlink(self.root / 'linked', source, directory=True)
        (self.root / 'local-projects.json').write_text(json.dumps({'demo': 'linked'}))
        with self.assertRaises(ValueError):
            export_projects(self.root, self.public, self.approved | {'demo/index.html'})


class ReleaseTests(unittest.TestCase):
    SHA = 'a' * 40

    def test_accepts_explicit_exact_main_release(self):
        check_release('workflow_dispatch', 'refs/heads/main', self.SHA, self.SHA, 'PUBLISH')

    def test_rejects_push_and_pr_even_with_confirmation(self):
        for event in ('push', 'pull_request'):
            with self.subTest(event=event), self.assertRaises(ValueError):
                check_release(event, 'refs/heads/main', self.SHA, self.SHA, 'PUBLISH')

    def test_rejects_non_main_release(self):
        with self.assertRaises(ValueError):
            check_release('workflow_dispatch', 'refs/heads/feature', self.SHA, self.SHA, 'PUBLISH')

    def test_rejects_stale_or_abbreviated_sha(self):
        for expected in ('b' * 40, self.SHA[:7], '', '$(command)'):
            with self.subTest(expected=expected), self.assertRaises(ValueError):
                check_release('workflow_dispatch', 'refs/heads/main', expected, self.SHA, 'PUBLISH')

    def test_rejects_missing_confirmation(self):
        with self.assertRaises(ValueError):
            check_release('workflow_dispatch', 'refs/heads/main', self.SHA, self.SHA, '')

    def test_rejects_tampered_scanner_download(self):
        with self.assertRaises(ValueError):
            verify_archive(b'tampered archive', hashlib.sha256(b'official archive').hexdigest())


if __name__ == '__main__':
    unittest.main()
