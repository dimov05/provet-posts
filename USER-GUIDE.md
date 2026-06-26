# 📖 User Guide — Provet Facebook Assistant

**For everyone — no coding, no VS Code, no technical knowledge needed.**

This system helps you **plan**, **write**, and **publish** the clinic's Facebook posts. Everything is
already set up. This guide shows you exactly what to tap and type.

---

## 1. What it does (in one minute)

- All past and future posts live in one place (a GitHub repository — think of it as an online folder).
- A **schedule** shows what's coming up and what still needs to be written.
- **Claude** (the AI) writes each post in the clinic's exact style and language — you just ask.
- You then **publish** through Facebook's free **Meta Business Suite**.

You will use **3 free apps**. Install them once:

| App | What it's for | Phone | Computer |
|-----|---------------|-------|----------|
| **GitHub** | See & store the schedule and posts | GitHub app | github.com in any browser |
| **Claude** | Write and review posts | Claude app | claude.ai in any browser |
| **Meta Business Suite** | Publish/schedule to Facebook | Meta Business Suite app | business.facebook.com |

> One-time setup (ask whoever set this up to do it with you): in the **Claude app**, connect this
> GitHub repository so Claude can read the schedule and the style guide on its own.

---

## 2. Understanding the schedule

Open the file **`fb-content-vault/SCHEDULE.md`** on GitHub. It's a table of every post.

**Columns:** Date · Time · ID (like `#440`) · Title · Series (the type of post) · Status · File.

**The schedule has 3 parts:**
1. **🟢 Upcoming** — posts that have a date but haven't gone out yet.
2. **📝 Backlog** — topic ideas waiting for a date.
3. **📚 Published archive** — everything already posted (click to expand).

**Status — what each one means:**

| Status | Meaning | What to do |
|--------|---------|------------|
| ✅ `published` | Already live on Facebook | Nothing — it's done |
| 📅 `scheduled` | Written **and** queued in Meta Business Suite | Nothing — it will post itself |
| 👍 `ready` | Approved, but not yet put into Meta Business Suite | Load it into Meta Business Suite |
| ✍️ `drafted` | Text exists but you haven't reviewed it | Read it, fix anything, approve |
| 💡 `topic` | Just an idea/title, no text yet | Ask Claude to write it |

---

## 3. 📱 Doing it from your PHONE

### A) See what's coming up
1. Open the **GitHub app** → your repository → `fb-content-vault` → `SCHEDULE.md`.
2. Look at the **Upcoming** and **Backlog** sections.

### B) Ask Claude to write a post
1. Open the **Claude app**.
2. Say, in plain words, for example:
   > "Write Facebook post **#440 — ТОП 10 кучешки имена** for Provet. Follow `BRAND-VOICE.md`
   > and the matching template in `series-templates.md` from the repo."
3. Claude writes the full Bulgarian post, ending with the hashtags.

### C) Review and adjust
- Read it. If you want changes, just say so: *"Make it a bit shorter"*, *"Add a sentence about
  microchipping"*, *"Use a warmer opening."* Claude rewrites it.

### D) Publish to Facebook
1. Copy the final text.
2. Open the **Meta Business Suite** app → **Planner** (the calendar) → **Create post**.
3. Paste the text, attach the photo, and tap **Schedule** for the date/time from the schedule
   (usually **Wednesday or Saturday around 19:00**).

That's the whole loop — no laptop required.

---

## 4. 💻 Doing it from your COMPUTER (no VS Code)

Exactly the same as the phone, just on bigger screens in your browser:
- **github.com** → open `fb-content-vault/SCHEDULE.md` to see the plan.
- **claude.ai** → ask Claude to write/review (same wording as above).
- **business.facebook.com** → Planner → paste + schedule.

To **save** a post back into the library from a browser: open the post's file on GitHub →
tap the **✏️ pencil** (Edit) → paste the new text → green **Commit changes** button.

> 💡 You do **not** need to edit `SCHEDULE.md` yourself — it rebuilds automatically from the post files.

---

## 5. ⚡ The shortcut commands (optional power tools)

If this repo is opened in **Claude Code** (a free assistant on a laptop), there are one-line commands.
**You don't have to use them** — anything they do, you can also just ask Claude in plain language
(phone or web). Here's the cheat sheet:

| Command | Plain-language version (works in the Claude app too) | What happens |
|---------|------------------------------------------------------|--------------|
| `/post #440` | "Write post #440 in Provet's style." | Writes the post, saves it, updates the schedule |
| `/plan-month 2026-07` | "Plan July: put my backlog topics on Wednesdays and Saturdays." | Assigns dates to ideas for the month |
| `/schedule` | "Show me what's coming up." | Refreshes and summarizes the calendar |

---

## 6. 📋 Common tasks (recipes)

**"Write the next post that's due"**
→ Check `SCHEDULE.md` for the nearest 🟢 Upcoming post → ask Claude: *"Write post #__ in Provet's style."*

**"Plan all of next month"**
→ Ask Claude: *"Plan next month — spread my backlog topics across Wednesdays and Saturdays at 19:00,
mix up the topic types, and put a contact post roughly every two weeks."*

**"Change a post's date"**
→ On GitHub, open the post's file → ✏️ Edit → change the `date:` line → Commit.

**"Add a brand-new topic idea"**
→ Ask Claude: *"Add a backlog topic: 'Признаци на алергия при котки'."* (Or create a new file on GitHub.)

**"See what still needs writing"**
→ In `SCHEDULE.md`, look for 💡 `topic` and ✍️ `drafted` rows.

**"I want a holiday working-hours post"**
→ Ask Claude: *"Write a holiday hours post for [holiday] — use the exact hours from `CLINIC-INFO.md`
for both locations."* (Тракия and Кършияка have **different** hours — Claude handles this.)

---

## 7. ❓ Good to know

- **Clinic facts** (phones, addresses, working hours) come only from `CLINIC-INFO.md`. If hours ever
  change, tell whoever maintains the repo to update that one file — every future post will then be correct.
- **Two locations, different hours:** Тракия (Mon–Sun 08:00–22:00) and Кършияка (Mon–Fri 10:00–19:00).
- **If Claude states a medical fact you're unsure about**, double-check with the vets before posting.
- **Images** are stored in the repo — see the dedicated section below.
- **Never worry about breaking the schedule table** — it's rebuilt automatically from the posts.

---

## 8. 📷 Images for posts

Images live in the **`fb-content-vault/images/`** folder, so you can add and grab them from your phone
or computer. The trick: **name each image after the post's ID number** and the schedule links it
automatically (you'll see a 📷 in the **Img** column).

**A post can have no image, one image, or several.**

| What you want | Name the file | 
|---------------|---------------|
| One image for post **#440** | `440.jpg` |
| Three images for post **#438** | `438_1.jpg`, `438_2.jpg`, `438_3.jpg` |

### Add an image from your phone
1. Open the **`images`** folder on GitHub (app or browser).
2. **Add file ▸ Upload files** → pick the photo → rename it to the post ID (e.g. `440.jpg`) → **Commit**.
3. Done — `SCHEDULE.md` will now show 📷 next to that post.

### Add an image from your computer
- Drag the file into the `images` folder on GitHub and commit, or copy it into the folder on disk.

### Use an image when publishing
1. In `SCHEDULE.md`, find the post and note its ID (and whether it shows 📷).
2. Open the `images` folder, tap the matching image, **download** it.
3. In **Meta Business Suite**, attach the downloaded image to the post when you schedule it.

> Posts in the schedule showing **`—`** in the Img column still need a picture.
> Recommended size: **1080×1080**. Style notes: `docs/image-style.md`.

---

## 9. 🔁 Your simple weekly routine

1. **Monday:** open `SCHEDULE.md`, see the week's 🟢 Upcoming posts.
2. Ask **Claude** to write any that are still `topic` or `drafted`; review them.
3. Open **Meta Business Suite** → paste + attach photo → **Schedule** for Wed & Sat 19:00.
4. Done. The posts go out by themselves.
