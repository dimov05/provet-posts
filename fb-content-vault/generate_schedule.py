#!/usr/bin/env python3
"""
Generates SCHEDULE.md (the master content calendar) from every markdown file
in posts-archive/. Source of truth = the frontmatter in each post file.

Usage:  python3 generate_schedule.py
Run it any time after adding/editing posts to refresh the table.
The `/schedule` Claude command just invokes this script.
"""
import os
import re
import glob
import datetime

ARCHIVE_DIR = os.path.join(os.path.dirname(__file__), "posts-archive")
IMAGES_DIR = os.path.join(os.path.dirname(__file__), "images")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "SCHEDULE.md")
TODAY = datetime.date.today().isoformat()
IMG_EXT = (".jpg", ".jpeg", ".png", ".webp")

# Rules checked against the TITLE first (high confidence), then the BODY.
# First match wins. Order matters: most specific first.
SERIES_RULES = [
    (r"пост с номерата", "contact"),
    (r"знаете ли,? че", "did-you-know"),
    (r"митове и легенди", "myths"),
    (r"породит[еа] кучета|порода:?\s*[а-я]", "breed-dog"),
    (r"породит[еа] котки", "breed-cat"),
    (r"топ\s*\d+|10 .*имена|10 .*породи", "list"),
    (r"оценете ни|google|отзив", "review-ask"),
    (r"празнично работно време|великден|коледа|нова година|работно време", "hours-holiday"),
    (r"скенер|томограф|ендоскоп|анестези|лаборатор|стационар|рентген|стоматолог", "service"),
]
# Body-only contact detector (a post that is essentially the contact card).
CONTACT_BODY = re.compile(r"book\.timify|очакваме ви", re.I)


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


def classify(title, body):
    # 1) Title is the strongest signal (Trello cards always have one).
    if title:
        t = title.lower()
        for pattern, label in SERIES_RULES:
            if re.search(pattern, t):
                return label
    # 2) Body: a short post dominated by the contact card.
    if CONTACT_BODY.search(body) and len(body) < 700:
        return "contact"
    # 3) Body keywords (for published posts that have no title).
    b = body.lower()
    for pattern, label in SERIES_RULES:
        if re.search(pattern, b):
            return label
    return "general"


def extract_id(title):
    m = re.search(r"#\s?(\d+(?:\.\d+)?)", title or "")
    return f"#{m.group(1)}" if m else ""


def list_images():
    if not os.path.isdir(IMAGES_DIR):
        return []
    return [f for f in os.listdir(IMAGES_DIR) if f.lower().endswith(IMG_EXT)]


def count_images(id_str, fm, body_image_source, image_files):
    """How many images belong to this post.
    1) explicit `images:` frontmatter wins; 2) else match files named after the
    post ID (e.g. 439.jpg, 439_1.jpg); 3) else a legacy single `image_source`."""
    explicit = fm.get("images", "")
    if explicit:
        items = [x.strip() for x in explicit.strip("[]").split(",") if x.strip()]
        return len(items)
    num = id_str.lstrip("#")
    if num:
        pat = re.compile(rf"^{re.escape(num)}([_.\-].*)?\.(jpg|jpeg|png|webp)$", re.I)
        n = sum(1 for f in image_files if pat.match(f))
        if n:
            return n
    if body_image_source and body_image_source not in ("None", ""):
        return 1
    return 0


def short_title(title, body):
    if title:
        return re.sub(r"^#\s?[\d.]+\s*", "", title).strip()[:60]
    first = next((l.strip() for l in body.splitlines() if l.strip()), "")
    return re.sub(r"[#❓👇🐾*]+", "", first).strip()[:60]


def main():
    image_files = list_images()
    rows = []
    for path in glob.glob(os.path.join(ARCHIVE_DIR, "*.md")):
        fname = os.path.basename(path)
        with open(path, encoding="utf-8") as f:
            fm, body = parse_frontmatter(f.read())

        title = fm.get("trello_title", "")
        date = fm.get("date", "TBD")
        time = fm.get("time", "")
        is_trello = fname.startswith("Trello")
        has_text = len(body.strip()) > 40

        # --- Status model (date-driven) ---
        # published : already live on Facebook (the date has passed)
        # scheduled : text done + loaded into Meta Business Suite, will auto-post
        # ready     : approved, just needs loading into Meta Business Suite
        # drafted   : text exists, awaiting your review
        # topic     : only a title/idea, needs writing
        fm_status = fm.get("status", "")
        is_dated = bool(re.match(r"\d{4}-\d{2}-\d{2}", date))
        if not is_trello:
            status = "published"                       # from FB export = already live
        elif is_dated and date <= TODAY:
            status = "published"                       # its date has passed
        elif fm_status in ("scheduled", "ready", "drafted"):
            status = fm_status                          # explicit workflow state wins
        else:                                           # future-dated OR undated backlog
            status = "drafted" if has_text else "topic"

        post_id = extract_id(title)
        rows.append({
            "date": date,
            "time": time[:5] if time and time != "TBD" else "",
            "id": post_id,
            "title": short_title(title, body),
            "series": classify(title, body),
            "status": status,
            "img": count_images(post_id, fm, fm.get("image_source", ""), image_files),
            "file": fname,
        })

    def sortkey(r):
        d = r["date"]
        return (0, d) if re.match(r"\d{4}-\d{2}-\d{2}", d) else (1, "")

    rows.sort(key=sortkey)

    published = [r for r in rows if r["status"] == "published"]
    backlog = [r for r in rows if not re.match(r"\d{4}-\d{2}-\d{2}", r["date"])]
    upcoming = [r for r in rows if r["status"] != "published"
                and re.match(r"\d{4}-\d{2}-\d{2}", r["date"])]

    def table(items):
        out = ["| Date | Time | ID | Title | Series | Status | Img | File |",
               "|------|------|----|-------|--------|--------|-----|------|"]
        for r in items:
            img = f"📷×{r['img']}" if r['img'] > 1 else ("📷" if r['img'] == 1 else "—")
            out.append(f"| {r['date']} | {r['time']} | {r['id']} | {r['title']} | "
                       f"{r['series']} | {r['status']} | {img} | `{r['file']}` |")
        return "\n".join(out)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"# 📅 Provet — Content Schedule\n\n")
        f.write(f"_Auto-generated by `generate_schedule.py` on {TODAY}. "
                f"Edit posts in `posts-archive/`, then run the script (or `/schedule`) to refresh._\n\n")
        f.write(f"**Cadence:** ~2 posts/week · primary days **Wed & Sat** · ~**19:00**\n\n")
        f.write("**Status legend:**\n"
                "- ✅ `published` — already live on Facebook (its date has passed)\n"
                "- 📅 `scheduled` — text done & loaded into Meta Business Suite, will auto-post\n"
                "- 👍 `ready` — approved, just needs loading into Meta Business Suite\n"
                "- ✍️ `drafted` — text written, awaiting your review\n"
                "- 💡 `topic` — only a title/idea, needs writing (use `/post`)\n\n")
        f.write("**Img** = images attached (named after the post ID in `images/`). "
                "`—` means none yet. See [images/README.md](images/README.md).\n\n")
        f.write(f"## 🟢 Upcoming — dated, not yet published ({len(upcoming)})\n\n")
        f.write((table(upcoming) if upcoming else "_Nothing scheduled ahead yet — run `/plan-month`._") + "\n\n")
        f.write(f"## 📝 Backlog — topics waiting for a date ({len(backlog)})\n\n")
        f.write((table(backlog) if backlog else "_Empty._") + "\n\n")
        f.write(f"## 📚 Published archive\n\n<details>\n<summary>{len(published)} past posts — click to expand</summary>\n\n")
        f.write(table(published) + "\n\n</details>\n")

    print(f"Wrote {OUTPUT_FILE}: {len(upcoming)} upcoming, {len(backlog)} backlog, "
          f"{len(published)} published.")


if __name__ == "__main__":
    main()
