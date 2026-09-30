#!/usr/bin/env python3
"""Append ?v=<content hash> to local css/js/image/video links in every page.

GitHub Pages lets browsers cache files for 10 minutes, so after an update a
visitor can get a stale mix of old and new files. A changed file gets a new
?v= and is always fetched fresh. Run before committing: python3 tools/bust-cache.py
"""
import hashlib, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXT = r'(?:css|js|png|jpe?g|svg|webp|mp4)'
ATTR = re.compile(r'((?:href|src|poster)=")((?!https?:|//|mailto:|#)[^"?#]+\.' + EXT + r')(?:\?v=[0-9a-f]+)?(")')

def digest(path):
    return hashlib.sha1(path.read_bytes()).hexdigest()[:8]

changed = 0
for page in sorted(ROOT.rglob('*.html')):
    if '.git' in page.parts:
        continue
    text = page.read_text()
    def repl(m):
        target = (page.parent / m.group(2)).resolve() if not m.group(2).startswith('/') else ROOT / m.group(2).lstrip('/')
        if not target.exists():
            print(f'  missing: {page.relative_to(ROOT)} -> {m.group(2)}')
            return m.group(0)
        return f'{m.group(1)}{m.group(2)}?v={digest(target)}{m.group(3)}'
    new = ATTR.sub(repl, text)
    if new != text:
        page.write_text(new); changed += 1
        print(f'updated {page.relative_to(ROOT)}')
print(f'{changed} page(s) updated')
