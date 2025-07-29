import subprocess
import json
import os

CHANNEL_URL = "https://www.youtube.com/@trungtamngonngukyhieuhanoi/videos"
OUTPUT_DIR = "data/videos"
METADATA_FILE = "data/metadata.jsonl"
MAX_DURATION = 120  # Giây
MAX_VIDEOS = 50

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Step 1: Get video info list from channel
print("📦 Fetching video metadata...")
cmd = [
    "yt-dlp",
    "--flat-playlist",
    "--dump-json",
    CHANNEL_URL
]
result = subprocess.run(cmd, capture_output=True, text=True)
all_entries = [json.loads(line) for line in result.stdout.strip().split("\n")]

print(f"🔍 Found {len(all_entries)} video entries...")

selected = []
for entry in all_entries:
    video_url = f"https://www.youtube.com/watch?v={entry['id']}"
    print(f"⏳ Checking duration: {entry['title']}")
    # Step 2: Get full metadata of each video
    cmd2 = [
        "yt-dlp",
        "--skip-download",
        "--print-json",
        video_url
    ]
    info = subprocess.run(cmd2, capture_output=True, text=True)
    try:
        video_info = json.loads(info.stdout)
        duration = video_info.get("duration", 9999)
        if duration <= MAX_DURATION:
            selected.append(video_info)
            print(f"✅ Kept: {video_info['title']} ({duration}s)")
        if len(selected) >= MAX_VIDEOS:
            break
    except:
        continue

# Step 3: Download selected videos
print(f"\n🚀 Downloading {len(selected)} videos to {OUTPUT_DIR}...")
for vid in selected:
    url = vid['webpage_url']
    outname = os.path.join(OUTPUT_DIR, f"{vid['id']}.mp4")
    cmd3 = [
        "yt-dlp",
        "-f", "mp4",
        "-o", outname,
        url
    ]
    subprocess.run(cmd3)

# Step 4: Save metadata
with open(METADATA_FILE, "w") as f:
    for vid in selected:
        f.write(json.dumps({
            "video_id": vid["id"],
            "title": vid["title"],
            "url": vid["webpage_url"],
            "duration": vid["duration"],
            "fps": vid.get("fps", None),
            "resolution": f"{vid.get('width')}x{vid.get('height')}" if "width" in vid else None
        }) + "\n")

print(f"\n📁 Saved metadata to: {METADATA_FILE}")
