import cv2
import mediapipe as mp
import json
from tqdm import tqdm
import argparse
import os

def extract_keypoints(video_path, output_json):
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,  
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )


    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    results = []
    frame_idx = 0

    print(f"🔍 Processing {total_frames} frames from {video_path}...")
    with tqdm(total=total_frames) as pbar:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            frame_data = {"frame": frame_idx, "keypoints": []}

            # ⚠️ Cần chuyển frame sang RGB trước khi dùng MediaPipe
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            detection = hands.process(image_rgb)

            if detection.multi_hand_landmarks:
                for hand_landmarks in detection.multi_hand_landmarks:
                    keypoints = [{"x": lm.x, "y": lm.y, "z": lm.z} for lm in hand_landmarks.landmark]
                    frame_data["keypoints"].append(keypoints)
            else:
                frame_data["keypoints"] = None

            results.append(frame_data)
            frame_idx += 1
            pbar.update(1)

    cap.release()
    hands.close()

    with open(output_json, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n✅ Keypoints saved to: {output_json}")


def filter_valid_frames(input_json, output_json):
    with open(input_json) as f:
        data = json.load(f)

    valid_frames = [f for f in data if f["keypoints"] is not None]

    with open(output_json, "w") as f:
        json.dump(valid_frames, f, indent=2)

    print(f"✅ Filtered: {len(valid_frames)} valid frames kept (from {len(data)} total frames)")
    print(f"💾 Saved filtered keypoints to: {output_json}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract hand keypoints from a video.")
    parser.add_argument("--video", required=True, help="Path to input .mp4 video")
    parser.add_argument("--output_raw", default="data/keypoints_raw.json", help="Raw output file (with null frames)")
    parser.add_argument("--output_filtered", default="data/keypoints_filtered.json", help="Filtered output file")

    args = parser.parse_args()

    # Step 1: Extract all keypoints (raw, including null)
    extract_keypoints(args.video, args.output_raw)

    # Step 2: Filter out null frames
    filter_valid_frames(args.output_raw, args.output_filtered)
