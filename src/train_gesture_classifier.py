import json
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import argparse

def load_keypoints(json_file):
    with open(json_file) as f:
        data = json.load(f)

    frame_to_keypoints = {}
    for frame in data:
        frame_id = frame["frame"]
        keypoints = frame.get("keypoints", [])

        if not keypoints or not isinstance(keypoints, list):
            continue  # skip nếu không có tay

        flattened = []
        try:
            for hand in keypoints:
                for kp in hand:
                    flattened.extend([kp["x"], kp["y"], kp["z"]])
        except (TypeError, KeyError):
            print(f"⚠️ Frame {frame_id} có keypoints sai định dạng, bỏ qua.")
            continue

        # Nếu chỉ có 1 tay → pad thêm 63 chiều (21 điểm * 3)
        if len(keypoints) == 1:
            flattened.extend([0.0] * 63)

        if len(flattened) != 126:
            print(f"⚠️ Frame {frame_id} chiều dữ liệu khác 126, bỏ qua.")
            continue

        frame_to_keypoints[frame_id] = flattened

    print(f"✅ Đã load {len(frame_to_keypoints)} frames hợp lệ với 2 tay (63x2 = 126 chiều).")
    return frame_to_keypoints

def load_labels(label_file):
    with open(label_file) as f:
        label_ranges = json.load(f)

    frame_to_label = {}
    for entry in label_ranges:
        for frame_id in range(entry["start"], entry["end"] + 1):
            frame_to_label[frame_id] = entry["label"]
    return frame_to_label

def build_dataset(keypoints_data, frame_labels):
    X, y = [], []
    for frame_id, features in keypoints_data.items():
        if frame_id not in frame_labels:
            continue
        X.append(features)
        y.append(frame_labels[frame_id])
    return np.array(X), np.array(y)

def main(keypoint_file, label_file, model_output):
    print("🔄 Loading data...")
    keypoints = load_keypoints(keypoint_file)
    labels = load_labels(label_file)
    X, y = build_dataset(keypoints, labels)

    print(f"🧩 Dataset size: {len(X)} samples, {len(set(y))} classes")

    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

    print("🎯 Training SVM classifier...")
    clf = SVC(kernel='rbf', C=10, gamma='scale', probability=True)
    clf.fit(X_train, y_train)

    print("✅ Evaluation:")
    y_pred = clf.predict(X_test)
    print(classification_report(y_test, y_pred))
    print("📊 Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    joblib.dump(clf, model_output)
    print(f"💾 Model saved to {model_output}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--keypoints", default="./data/keypoints_filtered.json", help="Path to JSON with keypoints")
    parser.add_argument("--labels", default="./data/gesture_labels.json", help="Path to gesture label ranges")
    parser.add_argument("--model_out", default="gesture_classifier.pkl", help="Output file for trained model")
    args = parser.parse_args()

    main(args.keypoints, args.labels, args.model_out)
