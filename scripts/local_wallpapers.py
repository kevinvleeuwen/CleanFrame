"""Personal wallpapers kept out of Git and added at build time.

Files under .local/wallpapers/ mirror app/ paths (assets/wallpapers/*, assets/materials/*).
Packaging adds them on top of app/, so an overlay catalog.js replaces the bundled gallery.
The preview serves them only with --local-wallpapers, so the regular checks keep the
public gallery.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = re.compile(r'^assets/(wallpapers|materials)/([a-z0-9][a-z0-9-]{0,80}\.(jpg|js|json)|SOURCES\.json)$')


def wallpaper_overlay(root=ROOT):
    base = root / '.local/wallpapers'
    files = {}
    if not base.is_dir():
        return files
    for source in sorted(base.rglob('*')):
        if source.is_symlink():
            raise ValueError('Local wallpapers must be regular files, not symlinks: ' + source.name)
        if not source.is_file() or source.name.startswith('.'):
            continue
        name = source.relative_to(base).as_posix()
        if not ALLOWED.match(name):
            raise ValueError('Unexpected file in .local/wallpapers: ' + name)
        files[name] = source
    return files
