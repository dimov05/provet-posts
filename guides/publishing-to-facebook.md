# 📤 Publishing to Facebook

The repo writes and schedules the **text**; Facebook publishing is done through **Meta Business Suite**
(free, official, works on laptop and phone). Claude does **not** auto-publish.

## The workflow (default)
1. Draft posts for the period with `/post <#ID>` (and `/plan-month` to date them).
   Each finished post lives in `posts/<file>.md` with `status: drafted`.
2. Open **Meta Business Suite** → **Planner** (business.facebook.com or the *Meta Business Suite* phone app).
3. For each post: **Create post** → paste the text from the file → attach the image →
   **Schedule** for the date/time in `SCHEDULE.md` (your Wed/Sat 19:00 slots).
4. You can batch a whole month in one sitting — the Planner shows everything on a calendar.
5. After scheduling, optionally mark the post `status: scheduled` in its file and run `/schedule`.

### Tips
- Meta Business Suite lets you schedule up to ~75 days ahead and reschedule by drag-and-drop.
- The hashtag block is already at the bottom of each drafted post — paste as-is.
- Keep the first 1–2 lines strong; Facebook truncates with "See more" after a few lines.

## Graph API auto-publish (BUILT — opt-in)
Hands-off scheduling straight from the repo is now available via the Graph API + GitHub Actions:
- Mark a post `status: ready` (with a real date), commit & push to `master`.
- `tools/publish.py` runs on GitHub Actions, schedules it on the Page for its Europe/Sofia time,
  then writes `status: scheduled` + `fb_post_id` back to the post file (never double-posts).
- Images are matched by post ID just like `SCHEDULE.md`; this public repo sends them by raw URL.

**One-time setup (owner):** follow [`facebook-api-setup.md`](facebook-api-setup.md) to create a Meta
app, get a Page token, and add the `FB_PAGE_TOKEN` / `FB_PAGE_ID` GitHub secrets. Test with the
workflow's **dry_run** button first.

**Good to know:** tokens can expire (use a System User token so it doesn't); the Graph schedule
window is 10 min–75 days ahead. Manual Meta Business Suite above remains a fine fallback.
