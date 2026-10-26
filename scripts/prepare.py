"""Copy approved static projects, validate references, produce a version manifest."""
from pathlib import Path
import hashlib
import json
import re
import shutil
from datetime import datetime, timezone
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'


def validate(folder):
    if not (folder / 'index.html').is_file():
        raise ValueError('Missing index.html: ' + str(folder))
    for file in folder.rglob('*'):
        if file.is_symlink():
            raise ValueError('Symlink in static output: ' + str(file))
        if not file.is_file():
            continue
        if file.name.startswith('.') or file.suffix.lower() in ('.pem', '.key', '.env'):
            raise ValueError('Unexpected hidden/secret file: ' + str(file))
        if file.suffix not in ('.html', '.css'):
            continue
        content = file.read_text(encoding='utf-8')
        refs = re.findall(r'(?:src|href)=[\'"]([^\'"]+)', content) if file.suffix == '.html' else re.findall(r'url\([\'"]?([^\)\'"]+)', content)
        for ref in refs:
            if ref.startswith(('#', 'data:', '//')):
                continue
            parsed = urlsplit(ref)
            if parsed.scheme or not parsed.path:
                continue
            target = (PUBLIC / unquote(parsed.path.lstrip('/'))) if parsed.path.startswith('/') else file.parent / unquote(parsed.path)
            target = target.resolve()
            if not target.is_relative_to(PUBLIC.resolve()):
                raise ValueError('Resource escapes public directory: ' + ref)
            if not target.exists():
                raise ValueError('Missing resource in ' + str(file) + ': ' + ref)


def prepare():
    projects_file = ROOT / 'local-projects.json'
    projects = json.loads(projects_file.read_text(encoding='utf-8')) if projects_file.exists() else {}
    # Validate source before touching its previously exported version.
    for slug, source in projects.items():
        if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', slug):
            raise ValueError('Invalid project slug')
        source = (ROOT / source).resolve()
        if not (source / 'index.html').is_file():
            raise ValueError('Source needs index.html: ' + str(source))
        for file in source.rglob('*'):
            if file.is_symlink():
                raise ValueError('Symlink source is not supported')
        destination = PUBLIC / slug
        # Only generated output for this explicitly configured slug can be replaced.
        if destination.resolve().parent != PUBLIC.resolve():
            raise ValueError('Unsafe export destination')
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(source, destination)
    validate(PUBLIC)
    versions = {p.relative_to(PUBLIC).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted(PUBLIC.rglob('*')) if p.is_file() and p.name != 'version.json'}
    (PUBLIC / 'version.json').write_text(json.dumps({'prepared_at': datetime.now(timezone.utc).isoformat(), 'files': versions}, indent=2), encoding='utf-8')
    print(f'Validated {len(versions)} static files. Output: {PUBLIC}')


if __name__ == '__main__':
    prepare()
