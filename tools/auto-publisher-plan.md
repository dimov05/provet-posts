# Implementation Plan — Facebook Auto-Publisher (Graph API + GitHub Actions)

> Goal: automatically **schedule** `ready` posts onto the Provet Facebook Page via the official
> Graph API, triggered by GitHub Actions. Manual Meta Business Suite stays as a fallback.
> Read `CLAUDE.md` first for repo conventions (status model, image ID-matching, filenames).

## How it fits the existing system
- Posts live in `posts/` with frontmatter `status` (`topic→drafted→ready→scheduled→published`).
- The publisher only ever touches posts with **`status: ready`** (explicit human approval gate).
- After scheduling a post on Facebook, it sets **`status: scheduled`** and records the returned id.
- `published` is still inferred from the date by `tools/update-schedule.py`; no change needed there.

## Deliverables
1. `tools/publish.py` — the publisher.
2. `.github/workflows/publish.yml` — the automation.
3. `guides/facebook-api-setup.md` — one-time Meta setup walkthrough for the owner.
4. Small docs touch-ups (`CLAUDE.md`, `guides/publishing-to-facebook.md`) noting auto-publish is live.

---

## 1. `tools/publish.py`
**Inputs (env):** `FB_PAGE_TOKEN`, `FB_PAGE_ID`, optional `FB_API_VERSION` (default a recent `v21.0`),
optional `REPO_RAW_BASE` (e.g. `https://raw.githubusercontent.com/dimov05/provet-posts/master`).
**Flags:** `--dry-run` (no API calls, just print the plan).

**Logic:**
1. Scan `posts/*.md`, parse frontmatter (reuse the parser style from `update-schedule.py`).
2. Select posts where `status == ready` AND `date` is a real date AND no `fb_post_id` yet.
3. For each selected post:
   - **Text** = the markdown body (everything after frontmatter), trimmed.
   - **Images** = reuse the ID-based matching from `update-schedule.py` (`count_images`/glob on `images/`):
     resolve to actual files in `images/`.
   - **When** = combine `date` + `time` (default 19:00) in **Europe/Sofia** tz → Unix timestamp.
     - If timestamp ≥ now + 10 min and ≤ now + 75 days → **schedule** it (`scheduled_publish_time`, `published=false`).
     - If within 10 min or slightly past → **publish now**.
     - If more than ~24h in the past → **skip + warn** (avoid accidental back-posting).
   - **Post to Graph API** by image count:
     - **0 images:** `POST /{PAGE_ID}/feed` with `message`, scheduling params.
     - **1 image:** `POST /{PAGE_ID}/photos` with the image (see attachment modes below) + `message`/`caption` + scheduling params.
     - **2+ images (album):** upload each photo unpublished (`/{PAGE_ID}/photos?published=false`, collect `id`s),
       then `POST /{PAGE_ID}/feed` with `attached_media[{media_fbid}]` + `message` + scheduling params.
   - **Image attachment modes** (pick automatically; allow override):
     - **Public repo:** pass `url=<raw GitHub URL of the image>` — no upload needed.
     - **Private repo:** upload bytes via multipart `source=@file`.
   - On success: rewrite that post's frontmatter → `status: scheduled`, add `fb_post_id: <id>` and
     `scheduled_for: <iso datetime>`. Keep everything else intact.
4. Print a summary (scheduled / skipped / failed). Exit non-zero if any post failed (so CI flags it).
5. Be defensive: one post failing must not abort the others; never print the token.

## 2. `.github/workflows/publish.yml`
- **Triggers:**
  - `push` to the default branch with `paths: ['posts/**']` (marking a post `ready` = a commit = runs it).
  - `workflow_dispatch` with a boolean `dry_run` input (manual "Run workflow" button).
  - `schedule:` hourly cron (`'0 * * * *'`) as a safety net.
- **Job steps:** checkout → setup Python 3.12 → `pip install requests` → run `python tools/publish.py`
  (pass `--dry-run` when the manual input asks) → if frontmatter changed, **commit & push back**
  with a message containing `[skip ci]` (prevents a trigger loop).
- **Secrets → env:** `FB_PAGE_TOKEN`, `FB_PAGE_ID` from `secrets`.
- **Permissions:** `contents: write` (for the status push-back).
- Idempotent: posts already `scheduled` (have `fb_post_id`) are skipped, so reruns are safe.

## 3. `guides/facebook-api-setup.md` (owner does this once)
Step-by-step, beginner-friendly:
1. Create a Meta Developer account → **Create App** (type: Business). Free.
2. Add the **Pages**/**Facebook Login** product; find your **Page ID**.
3. Generate a **Page access token** with `pages_manage_posts`, `pages_read_engagement`, `pages_show_list`.
   - Then exchange for a **long-lived** token, or (preferred) create a **System User** token in Business
     Settings for one that effectively never expires. Explain both, recommend System User.
4. In GitHub: repo **Settings → Secrets and variables → Actions** → add `FB_PAGE_TOKEN` and `FB_PAGE_ID`.
5. Test: run the workflow manually with **dry_run = true**, read the log, then try one real future-dated post.
6. Token refresh notes + how to revoke.

## 4. Status / safety notes
- Add optional `error` handling: if a post fails, leave it `ready` and log why (don't mark scheduled).
- Decide repo visibility before building image attachment: **public** = simplest (raw URLs).
  The script should support both and auto-detect via `REPO_RAW_BASE` presence.
- Timezone is **Europe/Sofia** (use `zoneinfo`).
- Graph API scheduling window: **10 minutes to 75 days** ahead.

## Test plan
1. `python tools/publish.py --dry-run` locally with a fake token → verify selection + computed times.
2. Manual workflow run with `dry_run=true` → verify it reads secrets and lists the right posts.
3. Mark one real post `ready` dated a few hours out → confirm it appears as **Scheduled** in Meta
   Business Suite, and the repo shows `status: scheduled` + `fb_post_id`.

## Open decisions for the owner (confirm in the new chat)
- **Repo public or private?** (affects image attachment mode)
- **Default branch** is `master` here (PRs target `main`) — confirm which branch the workflow watches.
- Auto-publish all `ready` posts, or require they also be dated? (Plan assumes: ready **and** dated.)
