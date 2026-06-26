---
description: Rebuild SCHEDULE.md from the post files, then show what's upcoming
argument-hint: (optional) a month or filter to summarize
---

Run `python3 fb-content-vault/generate_schedule.py` to rebuild `fb-content-vault/SCHEDULE.md`
from the current state of `posts-archive/`.

Then:
- If `$ARGUMENTS` is empty: summarize the next ~8 upcoming posts and how many backlog topics still need a date or text.
- If `$ARGUMENTS` names a month/filter: show that slice of the schedule and flag any `topic`/`drafted` items that still need `/post` or review.

Keep the summary short and scannable.
