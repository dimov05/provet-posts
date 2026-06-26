---
description: Draft a Facebook post in Provet's brand voice from a scheduled topic
argument-hint: <post ID like #430, or part of a title, or a file name>
---

You are writing a Bulgarian Facebook post for the Provet veterinary clinic.

**Target:** `$ARGUMENTS`

Follow these steps exactly:

1. **Locate the topic.** Search `SCHEDULE.md` and `posts/`
   for the post matching `$ARGUMENTS` (by `#ID`, title fragment, or filename). If several match,
   pick the most likely and state which you chose. If none match, list the closest candidates and stop.

2. **Read the source.** Open the matching file in `posts/`. The Trello body (if any) is your
   raw brief/topic — use its facts and intent, but rewrite it fully in brand voice. Note its `Series`.

3. **Load the rules** (read these files):
   - `guides/writing-style.md` — voice, structure, hashtag block.
   - `guides/post-types.md` — find the skeleton for this post's series.
   - `guides/clinic-info.md` — ONLY for `contact`/`hours-holiday`/`service` posts; use exact hours per location.

4. **Study 2–3 real examples.** Find published posts of the **same series** in `posts/`
   (files starting with a date) and skim them so your length, rhythm, and tone match.

5. **Write the post.** Bulgarian, formal capitalized address (Вие/Ви/Вашата), correct structure for the
   series, ~150–200 words for feature posts (~60–90 for `did-you-know`), ending with the canonical
   hashtag block. Be medically careful; never invent clinic details.

6. **Save it.** Write the final text back into the SAME source file, replacing the raw brief but KEEPING
   and updating the frontmatter:
   - If it was a Trello topic, keep `trello_title`, keep/keep-as-is the `date`/`time`, set `status: drafted`.

7. **Refresh filenames + schedule.** Run `python3 tools/rename-posts.py` (updates the filename from the
   frontmatter, e.g. if a date was set), then `python3 tools/update-schedule.py`.

8. **Report.** Show the finished post text in a code block so it's easy to copy into Meta Business Suite.
   Then check `images/` for a file matching this post's ID (e.g. `439*.jpg`): if none
   exists, remind the user to add an image to `images/` named after the ID (e.g. `439.jpg`, or
   `439_1.jpg`/`439_2.jpg` for several). Suggest a visual per `guides/image-style.md`.
