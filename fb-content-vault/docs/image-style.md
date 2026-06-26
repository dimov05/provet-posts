# 🎨 Image Style & Brief Template (analysis + later phase)

Derived from the published image library (289 JPGs). **Image generation is a later phase** — this doc
captures the visual identity so any future image (made in Canva, AI, or by hand) stays on-brand.

## Recurring visual identity
- **Format:** square (~1:1, ~480px in the export; produce at **1080×1080** for Facebook).
- **Brand color:** Provet purple/magenta (logo + accent bars). Clean white space.
- **Logo:** „ПРОВЕТ" wordmark (with the heart in the O) placed in a top or bottom corner, small.
- **Subject:** one clear, well-lit animal photo (cat, dog, exotic) — calm, warm, high quality.
- **Typography:** sans-serif Cyrillic, white or dark depending on background, high contrast/readable.
- **Mood:** clean, friendly, professional veterinary — not clinical/cold.

## The two layout templates observed
**Template A — "card" (e.g. Знаете ли, че?)**
- White/light rounded frame around the photo.
- Top-left: Provet logo. Top-right: title in a **speech-bubble** (e.g. „Знаете ли, че?").
- Bottom: **two location bars** with 📍 pin + phones — `Кв. Тракия: 0879 285 209 / 032 207 209` and
  `Кв. Кършияка: 0879 284 720 / 032 576 397`.

**Template B — "full-bleed"**
- Photo fills the frame.
- Title top corner in white. Bottom corner: **„Работно време"** with both locations' hours
  (Тракия 08:00–22:00 · Кършияка 10:00–19:00). Logo small in opposite corner.

> Series mapping: educational/`did-you-know`/breed posts → Template A; `service`/`hours-holiday`/
> seasonal → Template B. Keep the location/hours overlays accurate per [CLINIC-INFO.md](../CLINIC-INFO.md).

## Reusable image brief (fill per post)
```
Series:        <breed-dog | did-you-know | service | ...>
Template:      <A card | B full-bleed>
Subject:       <e.g. a Beagle outdoors, alert, ears forward>
Title text:    <Bulgarian, short — matches post hook>
Overlay info:  <contact bars (A) | working hours (B) | none>
Color/mood:    Provet purple accent, warm natural light, clean
Output:        1080×1080 JPG
```

## Free production options (for the later build phase)
- **Canva (free):** build Template A & B as reusable templates with the logo/colors locked — fastest,
  most consistent, phone + laptop. Recommended default.
- **AI image generation:** good for the *animal photo* layer; brand frame/text still added in Canva
  for accuracy (AI struggles with exact Cyrillic text and phone numbers).
- Whatever the source, do the **text/logo/contact overlay** in a template so clinic facts are never wrong.

_When ready to build: create the two Canva templates, then a `/image-brief <#ID>` command can output the
brief above per post._
