"""Install a fixed official Gitleaks release only after its archive hash matches."""
import hashlib
import io
import os
from pathlib import Path
import platform
import tarfile
from urllib.request import urlopen
import zipfile

VERSION = '8.30.1'
# Digests verified against the official GitHub release asset metadata.
ASSETS = {
    'Linux': ('linux_x64.tar.gz', '551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb', 'gitleaks'),
    'Windows': ('windows_x64.zip', 'd29144deff3a68aa93ced33dddf84b7fdc26070add4aa0f4513094c8332afc4e', 'gitleaks.exe'),
}


def verify_archive(data, expected):
    if hashlib.sha256(data).hexdigest() != expected:
        raise ValueError('Gitleaks archive checksum mismatch; refusing installation')


def install():
    if platform.machine().lower() not in ('x86_64', 'amd64'):
        raise ValueError('Only x64 runners are supported')
    asset, digest, filename = ASSETS[platform.system()]
    url = f'https://github.com/gitleaks/gitleaks/releases/download/v{VERSION}/gitleaks_{VERSION}_{asset}'
    with urlopen(url, timeout=60) as response:
        data = response.read()
    verify_archive(data, digest)
    target = Path(os.environ.get('RUNNER_TEMP', Path(__file__).resolve().parents[1] / '.tools')) / 'plur-gitleaks'
    target.mkdir(parents=True, exist_ok=True)
    if asset.endswith('.zip'):
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            binary = archive.read(filename)
    else:
        with tarfile.open(fileobj=io.BytesIO(data), mode='r:gz') as archive:
            binary = archive.extractfile(filename).read()
    executable = target / filename
    executable.write_bytes(binary)
    executable.chmod(0o700)
    print(f'Installed verified Gitleaks {VERSION}: {executable}')


if __name__ == '__main__':
    install()
