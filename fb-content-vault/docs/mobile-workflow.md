# 📱 Using this from your phone

Everything is plain text in Git, so the phone workflow needs no special app.

## View / edit the schedule (GitHub)
- Open the repo on **github.com** (mobile browser) or the **GitHub mobile app**.
- `fb-content-vault/SCHEDULE.md` renders as a calendar table. Browse upcoming posts and the backlog.
- To tweak a topic or date: open the post file in `posts-archive/` → tap the ✏️ (edit) → commit.
  (Remember `SCHEDULE.md` is generated; edit the post files, not the table directly.)

## Draft a post from your phone (Claude app)
1. In the **Claude mobile app**, connect this GitHub repo (Settings → connectors → GitHub, or share the
   repo link in chat).
2. Ask: *"Using this repo, draft post #430 following BRAND-VOICE.md and the series template."*
   Claude reads the same files and writes the Bulgarian text.
3. Copy the result into **Meta Business Suite** (phone app) and schedule it.

> Note: the `/post` and `/plan-month` slash commands run in **Claude Code** (laptop). On the phone you get
> the same result by asking the Claude app in plain language to follow `BRAND-VOICE.md` + the templates.

## Publish from your phone
- **Meta Business Suite** app → Planner → paste text + image → Schedule. See
  [facebook-publishing.md](facebook-publishing.md).

## Typical mobile loop
Review `SCHEDULE.md` on GitHub → ask Claude app to draft the next 1–2 posts → paste into Meta Business
Suite and schedule. No laptop required.
