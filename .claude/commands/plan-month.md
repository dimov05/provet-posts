---
description: Assign dates to backlog topics for a month using Provet's posting cadence
argument-hint: <month like "2026-07" or "next month">
---

You are scheduling Provet's content calendar for: **$ARGUMENTS**

Cadence rules (from real history): **~2 posts/week**, primary days **Wednesday & Saturday**, time **19:00**.
Mix series so the same type isn't back-to-back; include a `contact` ("Пост с номерата") post roughly
every 2 weeks. Holiday/`hours-holiday` posts must land on the correct real dates.

Steps:

1. Read `SCHEDULE.md` — note the **Backlog** items and any already-dated
   posts in the target month (don't double-book those slots).
2. Determine the target month's Wednesdays and Saturdays. Build the slot list at 19:00.
3. Assign backlog topics to open slots, balancing series variety. Prefer seasonally-relevant topics
   (e.g. heat-stroke in summer, fireworks before New Year).
4. For each assigned topic, update its file in `posts/`: set `date:` and `time: 19:00` in the
   frontmatter (keep `status` as is — text may still need writing via `/post`).
5. Run `python3 tools/rename-posts.py` (refreshes filenames now that dates are set), then
   `python3 tools/update-schedule.py`.
6. Report the proposed month as a table (Date · Day · ID · Title · Series) and note which slots are still
   empty or which topics still need text drafted with `/post`.

Do not invent new topics unless the backlog can't fill the month — if so, suggest topics that fit the
existing series and ask before adding them.
