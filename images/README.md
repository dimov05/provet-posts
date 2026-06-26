# 📷 Post Images

Drop the images for your posts in **this folder**. They are stored in the repo, so you can
download and attach them from your phone or computer when scheduling in Meta Business Suite.

## Naming = how images get linked to a post

Name each image with the post's **ID number**, then `_` and a number:

| Post | Image file(s) | Result |
|------|---------------|--------|
| `#440` with one image | `440.jpg` *(or `440_1.jpg`)* | post #440 → 1 image |
| `#438` with three images | `438_1.jpg`, `438_2.jpg`, `438_3.jpg` | post #438 → 3 images (album) |

- Allowed types: `.jpg` `.jpeg` `.png` `.webp`.
- The schedule (`SCHEDULE.md`) reads this folder automatically and shows an **Img** count per post.
  No need to edit any post file — just name the image after the post ID.
- For a post **without** an ID (rare), add an `images:` line to its file instead, e.g.
  `images: [my_photo.jpg]`, and put `my_photo.jpg` here.

## How to add an image
- **Phone / browser:** open this `images` folder on GitHub → **Add file ▸ Upload files** → choose the
  photo → rename it to the post ID → **Commit**.
- **Computer:** copy the file into this folder and commit (or drag-drop on GitHub).

## How to use it when posting
Open the post in `SCHEDULE.md`, note its ID, find the matching image here, **download** it, then attach
it in **Meta Business Suite** when you schedule the post.

> Keep images reasonably sized (Facebook works great at **1080×1080**). See
> [../guides/image-style.md](../guides/image-style.md) for the clinic's visual style.
