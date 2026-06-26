#!/usr/bin/env python3
"""
Normalizes post filenames to:  <date-or-TBD>_<ID>_<short-name>.md
e.g.  2026-06-18_430_porodite-kucheta-bigal.md  /  TBD_440_top-10-kucheshki-imena.md

Reads each post's frontmatter to build the name, so it's safe to re-run any time
(after changing a date or title the filename can be refreshed). Bulgarian names are
transliterated to Latin. Uses os.rename; `git add -A` records these as renames.

Usage:  python3 tools/rename-posts.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS = os.path.join(ROOT, "posts")

TRANSLIT = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ж": "zh", "з": "z",
    "и": "i", "й": "y", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o", "п": "p",
    "р": "r", "с": "s", "т": "t", "у": "u", "ф": "f", "х": "h", "ц": "ts", "ч": "ch",
    "ш": "sh", "щ": "sht", "ъ": "a", "ь": "y", "ю": "yu", "я": "ya",
}


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
    if not m:
        return {}, text
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"')
    return fm, m.group(2)


def translit(s):
    return "".join(TRANSLIT.get(c, c) for c in s.lower())


def slugify(text, maxlen=45):
    s = re.sub(r"[^a-z0-9]+", "-", translit(text)).strip("-")
    if len(s) > maxlen:
        s = s[:maxlen].rsplit("-", 1)[0]
    return s or "post"


def post_id(title, fname):
    m = re.search(r"#\s?(\d+(?:\.\d+)?)", title or "")    # Trello #NNN — authoritative
    if m:
        return m.group(1).replace(".", "-")
    # already in canonical form <date|TBD>_<ID>_<slug>.md → reuse the ID (idempotent)
    m = re.match(r"(?:\d{4}-\d{2}-\d{2}|TBD)_([^_]+)_", fname)
    if m:
        return m.group(1)
    m = re.match(r"\d{4}-\d{2}-\d{2}_(\d+)\.md$", fname)   # original FB: 2026-06-07_032.md
    if m:
        return m.group(1)
    m = re.match(r"Trello_(?:[\d-]+|TBD)_(\w+)\.md$", fname)  # original bonus Trello (no number)
    if m:
        return m.group(1)
    return "na"


def name_source(title, body):
    if title:
        return re.sub(r"^#?\s*\d+(?:\.\d+)?\s*", "", title)   # drop leading #ID
    first = next((l.strip() for l in body.splitlines() if l.strip()), "post")
    return first


def main():
    used = set()
    renamed = 0
    for fname in sorted(os.listdir(POSTS)):
        if not fname.endswith(".md"):
            continue
        path = os.path.join(POSTS, fname)
        with open(path, encoding="utf-8") as f:
            fm, body = parse_frontmatter(f.read())

        date = fm.get("date", "TBD")
        date = date if re.match(r"\d{4}-\d{2}-\d{2}", date) else "TBD"
        pid = post_id(fm.get("trello_title", ""), fname)
        slug = slugify(name_source(fm.get("trello_title", ""), body))

        new = f"{date}_{pid}_{slug}.md"
        # avoid collisions
        base, n = new[:-3], 2
        while new in used or (new != fname and os.path.exists(os.path.join(POSTS, new))):
            new = f"{base}-{n}.md"
            n += 1
        used.add(new)

        if new != fname:
            os.rename(path, os.path.join(POSTS, new))
            renamed += 1

    print(f"Renamed {renamed} files; {len(used)} posts total.")


if __name__ == "__main__":
    main()
