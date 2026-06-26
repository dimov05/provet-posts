import os
import json
import datetime

# --- CONFIGURATION ---
# Path to the extracted Facebook "your_posts_1.json" file
FB_JSON_PATH = "./your_facebook_data/your_posts_1.json" 
# Directory where you want your clean markdown files saved
OUTPUT_DIR = "./posts-archive"
# ---------------------

os.makedirs(OUTPUT_DIR, exist_ok=True)

def parse_facebook_posts():
    if not os.path.exists(FB_JSON_PATH):
        print(f"Error: Could not find Facebook JSON file at {FB_JSON_PATH}")
        return

    with open(FB_JSON_PATH, "r", encoding="utf-8") as f:
        posts_data = json.load(f)

    # Facebook exports can be a list directly or nested inside an object
    posts = posts_data if isinstance(posts_data, list) else posts_data.get("attachments", [])
    if not posts and isinstance(posts_data, dict):
        # Look for typical Meta export keys
        posts = posts_data.get("entries", []) or posts_data.get("data", [])

    count = 0
    for idx, item in enumerate(posts):
        # Extract timestamp
        timestamp_raw = item.get("timestamp", 0)
        if not timestamp_raw:
            continue
            
        dt = datetime.datetime.fromtimestamp(timestamp_raw)
        date_str = dt.strftime("%Y-%m-%d")
        time_str = dt.strftime("%H:%M:%S")
        day_of_week = dt.strftime("%A")

        # Extract post text
        post_text = ""
        data_list = item.get("data", [])
        for d in data_list:
            if "post" in d:
                post_text = d["post"]
                break

        # Fix potential encoding issues common in Facebook JSON dumps
        try:
            post_text = post_text.encode('latin1').decode('utf-8')
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass

        # Extract image path if available
        image_path = "None"
        attachments = item.get("attachments", [])
        if attachments:
            for attach in attachments:
                data = attach.get("data", [])
                for d in data:
                    media = d.get("media", {})
                    if "uri" in media:
                        image_path = media["uri"]
                        break

        # Skip completely empty posts (e.g., purely profile picture updates with no text)
        if not post_text.strip() and image_path == "None":
            continue

        # Generate standard filename
        filename = f"{date_str}_{idx:03d}.md"
        filepath = os.path.join(OUTPUT_DIR, filename)

        # Write clean, token-efficient Markdown file
        with open(filepath, "w", encoding="utf-8") as md_file:
            md_file.write("---\n")
            md_file.write(f"date: {date_str}\n")
            md_file.write(f"time: {time_str}\n")
            md_file.write(f"day: {day_of_week}\n")
            md_file.write(f"image_source: {image_path}\n")
            md_file.write("---\n\n")
            md_file.write(post_text.strip())
            md_file.write("\n")

        count += 1

    print(f"Success! Processed {count} posts into clean markdown files inside '{OUTPUT_DIR}'.")

if __name__ == "__main__":
    parse_facebook_posts()