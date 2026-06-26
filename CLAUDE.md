# Provet — Facebook Content Assistant

This repo is the planning + writing brain for the Facebook page of **Provet**, a veterinary clinic in
Plovdiv (Bulgaria). All posts are in **Bulgarian**. Claude's job: keep the schedule, and draft posts in
the clinic's established brand voice on request.

## Layout
```
CLAUDE.md                      ← you are here
USER-GUIDE.md                  ← plain-language guide for non-technical operators
.claude/commands/              ← slash commands: /post, /plan-month, /schedule
fb-content-vault/
├── SCHEDULE.md                ← master content calendar (GENERATED — do not hand-edit)
├── BRAND-VOICE.md             ← Bulgarian style guide (voice, structure, hashtags)
├── CLINIC-INFO.md             ← exact hours/phones/addresses — the ONLY source for clinic facts
├── generate_schedule.py       ← rebuilds SCHEDULE.md from posts-archive/
├── posts-archive/             ← one .md per post (frontmatter + text) = source of truth
│   ├── YYYY-MM-DD_NNN.md       ← past published Facebook posts (306)
│   └── Trello_<date|TBD>_<id>.md ← future posts / topics imported from Trello
├── images/                    ← post images; named after post ID (439.jpg, 438_1.jpg…); auto-linked in SCHEDULE
├── docs/
│   ├── series-templates.md    ← skeletons per recurring series
│   ├── facebook-publishing.md ← how posts reach Facebook (Meta Business Suite)
│   ├── mobile-workflow.md     ← using this from a phone
│   └── image-style.md         ← visual style analysis + image briefs (later phase)
├── parse_posts.py / parse_trello.py ← one-time importers (FB export / Trello export)
└── your_facebook_data/        ← raw FB export + media (read-only reference)
```

## Key facts
- **Cadence:** ~2 posts/week, primarily **Wed & Sat ~19:00**.
- **Voice:** formal capitalized address (Вие/Ви/Вашата), 🐾 section markers, educational + caring,
  ends with an engagement question + the canonical hashtag block. Full rules in `BRAND-VOICE.md`.
- **Two locations with DIFFERENT hours** — Тракия (Mon–Sun 08:00–22:00) and Кършияка (Mon–Fri 10:00–19:00).
  Always read `CLINIC-INFO.md`; never invent clinic details.
- **Series** are labeled in `SCHEDULE.md`; each has a template in `docs/series-templates.md`.

## Post statuses (the lifecycle)
Status lives in each post file's frontmatter; `published` is inferred from the date.
- ✅ `published` — already live on Facebook. Auto-detected: any post whose date is today or earlier. Don't set this by hand.
- 📅 `scheduled` — text done and loaded into Meta Business Suite (will auto-post). Set when the user confirms it's queued.
- 👍 `ready` — text approved by the user, just needs loading into Meta Business Suite.
- ✍️ `drafted` — text exists but not yet reviewed (set by `/post`, and the raw Trello imports).
- 💡 `topic` — only a title/idea, no real text yet; needs `/post`.
- A post with no future date yet lives in the **Backlog**; give it a date via `/plan-month`.

## Images
- Images live in `fb-content-vault/images/`, named after the post **ID**: `439.jpg` (single) or
  `438_1.jpg`, `438_2.jpg`… (album). `generate_schedule.py` auto-links them and shows an **Img** count.
- A post can have 0, 1, or many images. No frontmatter editing needed — naming does the linking.
  (Posts with no ID can use an explicit `images: [file.jpg]` frontmatter line instead.)
- Claude does not generate images yet (later phase). When drafting a post, remind the user to add an
  image to `images/` named after the ID. Visual style guide: `docs/image-style.md`.

## How to work in this repo
- **Draft a post:** `/post <#ID | title | filename>` — writes brand-voice text into the post file.
- **Plan a month:** `/plan-month <YYYY-MM>` — assigns backlog topics to Wed/Sat slots.
- **Refresh calendar:** `/schedule` (or `python3 fb-content-vault/generate_schedule.py`).
- **Publishing:** posts are pasted/scheduled manually in **Meta Business Suite** (see `docs/facebook-publishing.md`). Claude does not auto-publish.

## Rules
- Never hand-edit `SCHEDULE.md` — edit the post files, then regenerate.
- Clinic facts come only from `CLINIC-INFO.md`. If unsure about hours/medical claims, say so.
- Keep changes additive; the `your_facebook_data/` export and parse scripts are reference, leave them be.
- Write Bulgarian that matches the existing posts' tone — study real examples before drafting.
