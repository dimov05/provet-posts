# Facebook Auto-Publisher — One-Time Setup

This sets up automatic **scheduling** of approved posts to the Provet Facebook Page.
You only do this **once**. After that, marking a post `status: ready` (with a date) and
pushing it is enough — GitHub schedules it on Facebook for you. Manual posting in Meta
Business Suite still works as a fallback.

> You'll need: admin access to the Provet Facebook Page, and admin access to this GitHub repo.
> Everything here is free.

---

## How it works (in one paragraph)
A small script (`tools/publish.py`) runs on GitHub Actions. It looks for posts marked
`status: ready` that have a real date, and uses Facebook's official **Graph API** to schedule
them for that date/time (Europe/Sofia). Once Facebook accepts a post, the script writes
`status: scheduled` and the Facebook post id back into the post file, so the same post is never
posted twice. Images are matched by post ID exactly like the schedule does, and (because this
repo is public) are sent to Facebook as plain image URLs — no upload step.

---

## Step 1 — Create a Meta (Facebook) Developer App
1. Go to <https://developers.facebook.com/> and log in with the Facebook account that manages the Page.
2. Click **My Apps → Create App**.
3. Choose use case **Other → Business**. Give it a name like `Provet Publisher`. Create it.

## Step 2 — Find your Page ID
1. Open your Facebook Page → **About**, or visit
   <https://www.facebook.com/help/1503421039731588> for where the Page ID is shown.
2. Copy the numeric **Page ID** (a long number). You'll paste it into GitHub as `FB_PAGE_ID`.

## Step 3 — Get a Page access token
You have two options. **Option B (System User) is strongly recommended** because it does not
expire — otherwise you'd have to refresh the token periodically.

### Option A — Quick token (good for first test, expires)
1. Open the **Graph API Explorer**: <https://developers.facebook.com/tools/explorer/>.
2. Top-right: select your app. Click **Generate Access Token**.
3. Add these permissions, then regenerate:
   - `pages_manage_posts`
   - `pages_read_engagement`
   - `pages_show_list`
4. Switch the token dropdown from *User Token* to your **Page** — this gives a **Page token**.
5. (Recommended) Exchange it for a **long-lived** token (~60 days) using the
   Access Token Tool: <https://developers.facebook.com/tools/debug/accesstoken/>.

### Option B — System User token (does not expire) ✅ recommended
1. Go to **Meta Business Settings** → <https://business.facebook.com/settings>.
2. **Users → System Users → Add** → create one (e.g. `provet-publisher`), role **Admin** or **Employee**.
3. **Assign assets** → add your **Page** with **Manage Page / full control**.
4. Click **Generate new token**, pick your app, and select scopes:
   `pages_manage_posts`, `pages_read_engagement`, `pages_show_list`.
5. Set expiration to **Never**. Copy the token now — you can't view it again later.

> Keep this token secret. It is like a password for posting to your Page. Never paste it into a
> post, a commit, or a chat. If it ever leaks, revoke it (Step 6) and generate a new one.

## Step 4 — Add the secrets to GitHub
1. In this repo on GitHub: **Settings → Secrets and variables → Actions → New repository secret**.
2. Add two secrets (names must match exactly):
   - `FB_PAGE_TOKEN` → the token from Step 3.
   - `FB_PAGE_ID` → the numeric Page ID from Step 2.
3. (No need to set `REPO_RAW_BASE` — the workflow fills it in automatically for this public repo.)

## Step 5 — Test it safely
1. On GitHub: **Actions → "Publish ready posts to Facebook" → Run workflow**.
2. Leave **Dry run = true** and run it. Open the log: it should list which posts it *would*
   schedule and the exact Europe/Sofia times — **without** calling Facebook or changing anything.
3. When that looks right, do a real test: pick one post, set `status: ready` and a date a few hours
   in the future, commit & push to `master`. Within the hour (or immediately on push) the workflow
   runs for real.
4. Confirm in **Meta Business Suite → Planner** that the post shows as **Scheduled**. Back in the
   repo, that post's frontmatter should now say `status: scheduled` with an `fb_post_id`.

---

## Token refresh & revoke (Step 6)
- **System User token (Option B):** set to *Never expire* — nothing to do. If you ever rotate it,
  generate a new one and update the `FB_PAGE_TOKEN` secret in GitHub.
- **Long-lived user/page token (Option A):** expires (~60 days). When posting starts failing with an
  auth error, repeat Step 3 and update the `FB_PAGE_TOKEN` secret.
- **Revoke a token:** Business Settings → System Users → (your user) → remove the token, or
  remove the app under your Page's **Business integrations** / app settings. Then generate a fresh
  one and update the GitHub secret.

## Troubleshooting
- **"missing required env"** in the log → the `FB_PAGE_TOKEN` / `FB_PAGE_ID` secrets aren't set
  (or are misspelled) in GitHub.
- **A post was skipped** → it wasn't `status: ready`, had no real date, was already scheduled
  (has an `fb_post_id`), or its time was >75 days out / >24h in the past. The log says which.
- **Image failed to attach** → make sure the image file is committed in `images/` and named after
  the post ID (e.g. `439.jpg`, `439_1.jpg`). The repo must be public for URL mode to work.
- **A post failed** → it stays `status: ready` and is retried on the next run; the log explains why.
- Nothing is ever printed that contains your token; errors are sanitized.
