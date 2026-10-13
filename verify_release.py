"""Verify this local release's exact inventory without executing components."""
import hashlib
import json
from pathlib import Path


def verify(root):
    if any(p.is_symlink() for p in root.rglob('*')):
        raise ValueError('symlinks are not allowed')
    manifest=json.loads((root/'manifest.json').read_text())
    pins=manifest['artifacts']
    actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
    if actual!=set(pins)|{'manifest.json'}:
        raise ValueError('unexpected or missing file')
    for name,h in pins.items():
        p=root/name
        if not p.resolve().is_relative_to(root.resolve()):raise ValueError('unsafe path')
        if hashlib.sha256(p.read_bytes()).hexdigest()!=h:raise ValueError('file hash mismatch')
    return len(pins)


if __name__=='__main__':
    print('Verified payload files:',verify(Path(__file__).resolve().parent))
