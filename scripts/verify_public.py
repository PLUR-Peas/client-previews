"""Check every deployed asset anonymously against the published manifest."""
import hashlib
import json
from pathlib import Path
import sys
import time
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def fetch(url):
    with urlopen(Request(url, headers={'Cache-Control': 'no-cache'}), timeout=25) as response:
        return response.read()


def verify(base):
    base = base.rstrip('/') + '/'
    expected = json.loads((ROOT / 'public/version.json').read_text(encoding='utf-8'))['files']
    for attempt in range(12):
        try:
            nonce = str(time.time_ns())
            manifest = json.loads(fetch(base + 'version.json?verify=' + nonce))
            if manifest['files'] != expected:
                raise ValueError('Published manifest does not match this commit')
            for name, sha in expected.items():
                data = fetch(base + quote(name) + '?verify=' + nonce)
                if hashlib.sha256(data).hexdigest() != sha:
                    raise ValueError('Published bytes differ: ' + name)
            print('Anonymous HTTPS verification passed:', base)
            print('Vconsalte:', base + 'vconsalte/')
            return
        except Exception as error:
            print('Waiting for publication:', error)
            if attempt == 11:
                raise
            time.sleep(5)


if __name__ == '__main__':
    verify(sys.argv[1])
