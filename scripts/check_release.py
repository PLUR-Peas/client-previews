"""Require a deliberate public release of the exact checked-out main commit."""
import os
import re
import subprocess


def check_release(event, ref, expected, actual, confirmation):
    if event != 'workflow_dispatch' or ref != 'refs/heads/main':
        raise ValueError('Public releases require a manual run from main')
    if not re.fullmatch(r'[0-9a-f]{40}', expected):
        raise ValueError('Supply the complete lowercase 40-character approved commit SHA')
    if expected != actual or confirmation != 'PUBLISH':
        raise ValueError('Release confirmation does not match this exact commit')


if __name__ == '__main__':
    actual = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
    check_release(os.environ.get('GITHUB_EVENT_NAME'), os.environ.get('GITHUB_REF'),
                  os.environ.get('APPROVED_SHA', ''), actual,
                  os.environ.get('RELEASE_CONFIRMATION'))
    print('Explicit public release confirmed for the checked-out main commit.')
