"""Public seams: offline skill install/check CLI and narrated-script review CLI.
No live network, hosted model, API key, or regeneration of the delivery video.
"""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


class SkillInstallationTests(unittest.TestCase):
    def cli(self, *args):
        return subprocess.run([sys.executable, str(ROOT / 'workshop/skills.py'), *args],
                              capture_output=True, text=True)

    def test_installed_skills_and_sources_verify_offline(self):
        p = self.cli('--check')
        self.assertEqual(p.returncode, 0, p.stderr + p.stdout)
        result = json.loads(p.stdout)
        self.assertGreaterEqual(result['skillCount'], 25)
        self.assertTrue(result['ok'])

    def test_install_is_idempotent_and_never_clobbers_unknown_files(self):
        with tempfile.TemporaryDirectory() as d:
            dest = Path(d)
            args = ['--install', '--target', d]
            first = self.cli(*args)
            self.assertEqual(first.returncode, 0, first.stderr)
            skill = dest / '.agents/skills/ytb-script/SKILL.md'
            original = skill.read_bytes()
            second = self.cli(*args)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(skill.read_bytes(), original)
            skill.write_text('User-authored skill; preserve me.\n')
            third = self.cli(*args)
            self.assertNotEqual(third.returncode, 0)
            self.assertEqual(skill.read_text(), 'User-authored skill; preserve me.\n')

    def test_modified_vendor_source_is_detected_before_install(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            shutil.copytree(ROOT / 'workshop/vendor', base / 'workshop/vendor')
            shutil.copy(ROOT / 'workshop/skills.py', base / 'workshop/skills.py')
            shutil.copy(ROOT / 'workshop/skills-lock.json', base / 'workshop/skills-lock.json')
            victim = base / 'workshop/vendor/ytb-research-skills/tools/script_check.py'
            victim.write_text(victim.read_text() + '\n# tampered\n')
            p = subprocess.run([sys.executable, str(base / 'workshop/skills.py'), '--install'],
                               capture_output=True, text=True)
            self.assertNotEqual(p.returncode, 0)
            self.assertIn('script_check.py', p.stderr)
            self.assertFalse((base / '.agents').exists())

    def test_index_covers_every_installed_skill(self):
        lock = json.loads((ROOT / 'workshop/skills-lock.json').read_text())
        guide = (ROOT / 'agent.md').read_text()
        for skill in lock['skills']:
            self.assertIn(f'.agents/skills/{skill["name"]}/SKILL.md', guide)
            installed = ROOT / '.agents/skills' / skill['name'] / 'SKILL.md'
            self.assertEqual(installed.read_text(),
                             (ROOT / '.claude/skills' / skill['name'] / 'SKILL.md').read_text())

    def test_finished_video_is_unchanged(self):
        self.assertEqual(hashlib.sha256((ROOT / 'output/final_video.mp4').read_bytes()).hexdigest(),
                         '3f92a10306f3efe36772c607d8c614d0c0df613cb4dc1f042f096d79128ae1b7')


class ScriptReviewTests(unittest.TestCase):
    def review(self, text):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'episode.json'
            p.write_text(json.dumps({'sections': [{'text': text}]}))
            return subprocess.run([sys.executable, str(ROOT / 'workshop/review_script.py'), str(p)],
                                  capture_output=True, text=True)

    def test_weak_spoken_hook_fails_upstream_checker(self):
        result = self.review('Welcome back to my channel. Today we discuss the Sun.')
        self.assertEqual(result.returncode, 1, result.stderr + result.stdout)
        self.assertIn('FAIL', result.stdout)

    def test_spoken_text_only_is_checked_not_editorial_notes(self):
        result = self.review('What if the Sun vanished? Light would still travel toward Earth.')
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn('0 fail', result.stdout)
        self.assertIn('estimate', result.stdout.lower())


if __name__ == '__main__':
    unittest.main()
