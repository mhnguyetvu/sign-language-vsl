import json
import cv2
import numpy as np

HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (17, 18), (18, 19), (19, 20),
    (0, 17)
]

def draw_hand(canvas, keypoints, scale=400, offset=(50, 50)):
    for start, end in HAND_CONNECTIONS:
        x1 = int(keypoints[start]['x'] * scale + offset[0])
        y1 = int(keypoints[start]['y'] * scale + offset[1])
        x2 = int(keypoints[end]['x'] * scale + offset[0])
        y2 = int(keypoints[end]['y'] * scale + offset[1])
        cv2.line(canvas, (x1, y1), (x2, y2), (0, 255, 0), 2)

    for point in keypoints:
        x = int(point['x'] * scale + offset[0])
        y = int(point['y'] * scale + offset[1])
        cv2.circle(canvas, (x, y), 4, (0, 0, 255), -1)

def main(json_path, output_path="annotations/motion/hand_motion.mp4", fps=20):
    with open(json_path) as f:
        data = json.load(f)

    width, height = 500, 500
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for frame in data:
        if frame['keypoints'] is None:
            continue

        for hand in frame['keypoints']:
            draw_hand(canvas, hand)


        canvas = np.ones((height, width, 3), dtype=np.uint8) * 255
        draw_hand(canvas, frame['keypoints'])
        cv2.putText(canvas, f"Frame {frame['frame']}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        out.write(canvas)

    out.release()
    print(f"✅ Saved simulated motion to: {output_path}")

if __name__ == "__main__":
    main("data/keypoints_filtered.json")
