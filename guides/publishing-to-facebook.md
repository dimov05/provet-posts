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

## Optional later phase — Graph API auto-publish (NOT built yet)
If you later want hands-off publishing straight from the repo, the path is:
- Create a Meta **Developer app**, add the **Pages** product, get a **long-lived Page access token**
  (with `pages_manage_posts`, `pages_read_engagement`).
- Script (Python) calling `POST /{page-id}/photos` (with `published=false` to stage, or `scheduled_publish_time`
  for scheduling) or `/{page-id}/feed` for text-only.
- Run it locally or on a **GitHub Actions** cron (free) reading `SCHEDULE.md`.

**Trade-offs to know before enabling:** tokens expire (~60 days, need refreshing); images must be uploaded
or hosted at a public URL; Meta app/permission setup has friction. Manual Meta Business Suite is recommended
until the content workflow is proven. Ask Claude to scaffold this when you're ready.
