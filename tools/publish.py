#!/usr/bin/env python3
"""
Facebook auto-publisher for Provet posts.

Scans posts/, finds every post with `status: ready` that has a real date, and
SCHEDULES it on the Provet Facebook Page via the Graph API (or publishes it now
if its time is essentially upon us). After a post is accepted by Facebook this
script rewrites that post's frontmatter to `status: scheduled` and records the
returned `fb_post_id` + `scheduled_for`, so reruns never double-post.

Image handling mirrors tools/update-schedule.py: images live in images/ and are
matched by the post ID (439.jpg, 439_1.jpg, ...). 0, 1, or many are supported.
  - Public repo  → pass the raw GitHub URL of each image (set REPO_RAW_BASE).
  - Private repo → upload the image bytes via multipart.
The mode is auto-detected from REPO_RAW_BASE; override with --image-mode.

Usage:
  python3 tools/publish.py --dry-run     # print the plan, no API calls, no writes
  python3 tools/publish.py               # really schedule/publish

Environment:
  FB_PAGE_TOKEN   Page access token (required unless --dry-run). NEVER printed.
  FB_PAGE_ID      Numeric Facebook Page ID (required unless --dry-run).
  FB_API_VERSION  Graph API version (default v25.0).
  REPO_RAW_BASE   e.g. https://raw.githubusercontent.com/dimov05/provet-posts/master
                  When set (and image-mode is auto/url) images are sent by URL.
"""
import argparse
import datetime
import glob
import json
import os
import re
import sys
import time
from zoneinfo import ZoneInfo

try:
    import requests
except ImportError:  # pragma: no cover - only matters at real runtime
    requests = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(ROOT, "posts")
IMAGES_DIR = os.path.join(ROOT, "images")

SOFIA = ZoneInfo("Europe/Sofia")
IMG_EXT = (".jpg", ".jpeg", ".png", ".webp")

# Graph API scheduling window + safety thresholds.
MIN_AHEAD = 10 * 60            # 10 minutes: minimum lead time to "schedule".
MAX_AHEAD = 75 * 24 * 60 * 60  # 75 days: Graph API's maximum schedule horizon.
PAST_GRACE = 24 * 60 * 60      # up to 24h past → publish now; older → skip (no back-posting).


# --------------------------------------------------------------------------- #
# Frontmatter parsing / rewriting
# --------------------------------------------------------------------------- #
def parse_frontmatter(text):
    """Return (dict, body). Same shape as update-schedule.py's parser."""
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
    if not m:
        return {}, text
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"')
    return fm, m.group(2)


def update_frontmatter(raw_text, updates):
    """Apply `updates` (key->str) to the frontmatter, preserving everything else
    (key order, quoting of untouched lines, and the full body verbatim)."""
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", raw_text, re.DOTALL)
    if not m:
        raise ValueError("post has no frontmatter block")
    block, body = m.group(1), m.group(2)
    seen = set()
    out = []
    for line in block.splitlines():
        if ":" in line:
            k = line.split(":", 1)[0].strip()
            if k in updates:
                out.append(f"{k}: {updates[k]}")
                seen.add(k)
                continue
        out.append(line)
    for k, v in updates.items():
        if k not in seen:
            out.append(f"{k}: {v}")
    return f"---\n" + "\n".join(out) + f"\n---\n{body}"


# --------------------------------------------------------------------------- #
# Post ID + image resolution (mirrors update-schedule.py)
# --------------------------------------------------------------------------- #
def extract_id(title):
    m = re.search(r"#\s?(\d+(?:\.\d+)?)", title or "")
    return f"#{m.group(1)}" if m else ""


def id_from_filename(fname):
    m = re.match(r"(?:\d{4}-\d{2}-\d{2}|TBD)_([^_]+)_", fname)
    return f"#{m.group(1)}" if m else ""


def list_images():
    if not os.path.isdir(IMAGES_DIR):
        return []
    return [f for f in os.listdir(IMAGES_DIR) if f.lower().endswith(IMG_EXT)]


def resolve_images(id_str, fm, image_files):
    """Return the ordered list of image filenames belonging to this post.
    1) explicit `images:` frontmatter wins; 2) else files named after the post
    ID (439.jpg, 439_1.jpg...); 3) else a legacy single `image_source`."""
    explicit = fm.get("images", "")
    if explicit:
        return [x.strip() for x in explicit.strip("[]").split(",") if x.strip()]
    num = id_str.lstrip("#")
    if num:
        pat = re.compile(rf"^{re.escape(num)}([_.\-].*)?\.(jpg|jpeg|png|webp)$", re.I)
        matched = sorted(f for f in image_files if pat.match(f))
        if matched:
            return matched
    src = fm.get("image_source", "")
    if src and src not in ("None", ""):
        return [src]
    return []


# --------------------------------------------------------------------------- #
# Scheduling math
# --------------------------------------------------------------------------- #
def compute_time(date_str, time_str):
    """Combine date + time in Europe/Sofia → (unix_ts, aware datetime)."""
    t = (time_str or "").strip()[:5]
    if not t or t.upper() == "TBD" or ":" not in t:
        t = "19:00"
    dt = datetime.datetime.strptime(f"{date_str} {t}", "%Y-%m-%d %H:%M")
    dt = dt.replace(tzinfo=SOFIA)
    return int(dt.timestamp()), dt


def decide_action(ts, now):
    """Return ('schedule'|'now'|'skip', reason)."""
    delta = ts - now
    if delta > MAX_AHEAD:
        return "skip", f"more than 75 days out ({delta // 86400} days) — outside Graph window"
    if delta >= MIN_AHEAD:
        return "schedule", ""
    if delta > -PAST_GRACE:
        return "now", "within 10 min / just past — publishing now"
    return "skip", f"more than 24h in the past ({-delta // 3600}h) — refusing to back-post"


# --------------------------------------------------------------------------- #
# Graph API
# --------------------------------------------------------------------------- #
class GraphError(Exception):
    pass


def _sanitize(text, token):
    """Make sure a token can never leak into logs/exceptions."""
    if token and token in text:
        text = text.replace(token, "***TOKEN***")
    return text


def graph_post(session, version, edge, data, token, files=None):
    url = f"https://graph.facebook.com/{version}/{edge}"
    payload = dict(data, access_token=token)
    try:
        resp = session.post(url, data=payload, files=files, timeout=60)
    except requests.RequestException as e:
        raise GraphError(_sanitize(str(e), token))
    try:
        body = resp.json()
    except ValueError:
        body = {"_raw": resp.text}
    if resp.status_code >= 400 or "error" in body:
        err = body.get("error", body)
        raise GraphError(_sanitize(json.dumps(err, ensure_ascii=False), token))
    return body


def _image_field(filename, image_mode, raw_base, open_files):
    """Return (data_extra, files_extra) for one image depending on mode."""
    path = os.path.join(IMAGES_DIR, filename)
    if image_mode == "url":
        if not raw_base:
            raise GraphError("url image-mode requires REPO_RAW_BASE")
        return {"url": f"{raw_base.rstrip('/')}/images/{filename}"}, {}
    # upload mode
    if not os.path.isfile(path):
        raise GraphError(f"image file not found: images/{filename}")
    fh = open(path, "rb")
    open_files.append(fh)
    return {}, {"source": fh}


def publish_post(session, version, page_id, token, message, image_files,
                 image_mode, raw_base, action, ts):
    """Create the post on Facebook; return the resulting object id."""
    sched = {}
    if action == "schedule":
        sched = {"published": "false", "scheduled_publish_time": str(ts)}

    open_files = []
    try:
        # ---- 0 images: plain feed post -------------------------------------
        if not image_files:
            data = dict(sched, message=message)
            res = graph_post(session, version, f"{page_id}/feed", data, token)
            return res["id"]

        # ---- 1 image: single photo with caption ---------------------------
        if len(image_files) == 1:
            data, files = _image_field(image_files[0], image_mode, raw_base, open_files)
            data = dict(data, **sched, caption=message)
            res = graph_post(session, version, f"{page_id}/photos", data,
                             token, files=files or None)
            return res.get("post_id") or res["id"]

        # ---- 2+ images: upload unpublished, then attach to a feed post -----
        media_ids = []
        for fn in image_files:
            data, files = _image_field(fn, image_mode, raw_base, open_files)
            data = dict(data, published="false")
            res = graph_post(session, version, f"{page_id}/photos", data,
                             token, files=files or None)
            media_ids.append(res["id"])
            # close any opened handle promptly between uploads
            for fh in open_files:
                if not fh.closed:
                    fh.close()
            open_files = []
        data = dict(sched, message=message)
        for i, mid in enumerate(media_ids):
            data[f"attached_media[{i}]"] = json.dumps({"media_fbid": mid})
        res = graph_post(session, version, f"{page_id}/feed", data, token)
        return res["id"]
    finally:
        for fh in open_files:
            if not fh.closed:
                fh.close()


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def select_posts():
    """Yield (path, fm, body) for posts that are ready, dated, and not yet sent."""
    selected = []
    for path in sorted(glob.glob(os.path.join(POSTS_DIR, "*.md"))):
        with open(path, encoding="utf-8") as f:
            raw = f.read()
        fm, body = parse_frontmatter(raw)
        if fm.get("status", "").strip() != "ready":
            continue
        date = fm.get("date", "").strip()
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
            print(f"  skip {os.path.basename(path)}: status ready but no real date")
            continue
        if fm.get("fb_post_id", "").strip():
            print(f"  skip {os.path.basename(path)}: already has fb_post_id")
            continue
        selected.append((path, fm, body, raw))
    return selected


def main():
    ap = argparse.ArgumentParser(description="Schedule ready Provet posts to Facebook.")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print the plan; make no API calls and write no files.")
    ap.add_argument("--image-mode", choices=("auto", "url", "upload"), default="auto",
                    help="How to send images. auto=url if REPO_RAW_BASE set, else upload.")
    args = ap.parse_args()

    token = os.environ.get("FB_PAGE_TOKEN", "")
    page_id = os.environ.get("FB_PAGE_ID", "")
    version = os.environ.get("FB_API_VERSION", "v25.0")
    raw_base = os.environ.get("REPO_RAW_BASE", "").strip()

    image_mode = args.image_mode
    if image_mode == "auto":
        image_mode = "url" if raw_base else "upload"

    if not args.dry_run:
        if requests is None:
            print("ERROR: the 'requests' package is required (pip install requests).")
            return 2
        missing = [n for n, v in (("FB_PAGE_TOKEN", token), ("FB_PAGE_ID", page_id)) if not v]
        if missing:
            print(f"ERROR: missing required env: {', '.join(missing)}")
            return 2

    print(f"Provet publisher — {'DRY RUN' if args.dry_run else 'LIVE'} | "
          f"image-mode={image_mode} | api={version}")
    if image_mode == "url" and not raw_base:
        print("WARNING: image-mode=url but REPO_RAW_BASE is empty; posts with images will fail.")

    selected = select_posts()
    if not selected:
        print("Nothing to do: no ready+dated posts pending.")
        return 0

    image_files = list_images()
    now = time.time()
    session = None if args.dry_run else requests.Session()

    scheduled, published_now, skipped, failed = [], [], [], []

    for path, fm, body, raw in selected:
        name = os.path.basename(path)
        title = fm.get("trello_title", "")
        post_id = extract_id(title) or id_from_filename(name)
        message = body.strip()
        imgs = resolve_images(post_id, fm, image_files)
        ts, dt = compute_time(fm["date"], fm.get("time", ""))
        action, reason = decide_action(ts, now)

        when = dt.strftime("%Y-%m-%d %H:%M %Z")
        imgdesc = f"{len(imgs)} img" + (f" {imgs}" if imgs else "")
        print(f"\n• {name} [{post_id or 'no-id'}] → {when} | {imgdesc} | action={action}")
        if reason:
            print(f"    note: {reason}")

        if action == "skip":
            skipped.append(name)
            continue

        if args.dry_run:
            print(f"    DRY RUN: would {action} ({len(message)} chars)")
            (scheduled if action == "schedule" else published_now).append(name)
            continue

        try:
            fbid = publish_post(session, version, page_id, token, message, imgs,
                                image_mode, raw_base, action, ts)
        except GraphError as e:
            print(f"    FAILED: {e}")
            print("    leaving status: ready (will retry next run)")
            failed.append(name)
            continue

        updates = {
            "status": "scheduled",
            "fb_post_id": fbid,
            "scheduled_for": dt.isoformat(),
        }
        new_raw = update_frontmatter(raw, updates)
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_raw)
        print(f"    OK: fb_post_id={fbid} → status: scheduled")
        (scheduled if action == "schedule" else published_now).append(name)

    print(f"\nSummary: {len(scheduled)} scheduled, {len(published_now)} published-now, "
          f"{len(skipped)} skipped, {len(failed)} failed.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
