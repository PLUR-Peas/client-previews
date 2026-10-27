"""Explicit publication allowlist and safe local export boundaries."""
import json
from pathlib import PurePosixPath
import re
import shutil

ALLOWED_SUFFIXES = {'.html', '.css', '.js', '.json', '.svg', '.ttf', '.woff',
                    '.woff2', '.png', '.jpg', '.jpeg', '.webp', '.ico', '.txt'}


def approved_files(policy):
    data = json.loads(policy.read_text(encoding='utf-8'))
    paths = data['files']
    if data.get('version') != 1 or not isinstance(paths, list) or not paths:
        raise ValueError('Invalid public file policy')
    approved = set()
    for path in paths:
        if not isinstance(path, str) or not path or '\\' in path:
            raise ValueError('Invalid approved path')
        parsed = PurePosixPath(path)
        if (parsed.is_absolute() or parsed.as_posix() != path
                or any(part.startswith('.') or ':' in part for part in parsed.parts)
                or parsed.suffix.lower() not in ALLOWED_SUFFIXES):
            raise ValueError('Unsafe or unsupported approved path')
        if path in approved:
            raise ValueError('Duplicate approved path')
        approved.add(path)
    if 'index.html' not in approved or 'version.json' not in approved:
        raise ValueError('Policy needs root index.html and version.json')
    return approved


def checked_path(base, relative):
    if base.is_symlink():
        raise ValueError('Symlink root is not supported')
    candidate = base
    for part in PurePosixPath(relative).parts:
        candidate = candidate / part
        if candidate.is_symlink():
            raise ValueError('Symlink path is not supported')
    if not candidate.resolve().is_relative_to(base.resolve()):
        raise ValueError('Path escapes approved root')
    return candidate


def validate_artifact(folder, approved):
    if folder.is_symlink() or not folder.is_dir():
        raise ValueError('Public root must be a regular directory')
    actual = set()
    for file in folder.rglob('*'):
        relative = file.relative_to(folder).as_posix()
        checked_path(folder, relative)
        if file.is_dir():
            if any(part.startswith('.') for part in file.relative_to(folder).parts):
                raise ValueError('Hidden directory in artifact')
            continue
        if not file.is_file():
            raise ValueError('Non-regular file in artifact')
        actual.add(relative)
    unexpected = actual - approved
    missing = (approved - {'version.json'}) - actual
    if unexpected or missing:
        # Never print file contents or potential secret values.
        raise ValueError(f'Public file policy mismatch: {len(unexpected)} unexpected, '
                         f'{len(missing)} missing. Review security/public-files.json.')


def export_projects(root, public, approved):
    mapping = root / 'local-projects.json'
    if not mapping.is_file():
        raise ValueError('--export requires local-projects.json')
    projects = json.loads(mapping.read_text(encoding='utf-8'))
    copies = []
    for slug, source_value in projects.items():
        if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', slug):
            raise ValueError('Invalid project slug')
        source_path = root / source_value
        if any(part.is_symlink() for part in [source_path, *source_path.parents]):
            raise ValueError('Symlink source root is not supported')
        source = source_path.resolve()
        paths = sorted(path for path in approved if path.startswith(slug + '/'))
        if slug + '/index.html' not in paths:
            raise ValueError('Project needs a reviewed file list including index.html')
        for path in paths:
            candidate = checked_path(source, path[len(slug) + 1:])
            destination = checked_path(public, path)
            if not candidate.is_file():
                raise ValueError('Missing approved source file: ' + path)
            copies.append((candidate, destination))
    # Preflight every source before changing the export; never copy entire trees.
    for candidate, destination in copies:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(candidate, destination)
