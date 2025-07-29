import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import argparse

def load_keypoints(json_file):
    with open(json_file) as f:
        data = json.load(f)
    frame_to_keypoints = {frame["frame"]: frame["keypoints"] for frame in data if frame["keypoints"] is not None}
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
    for frame_id, keypoints in keypoints_data.items():
        if frame_id not in frame_labels:
            continue
        flattened = []
        for kp in keypoints:
            flattened.extend([kp["x"], kp["y"], kp["z"]])
        X.append(flattened)
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
    parser.add_argument("--keypoints", default="keypoints_filtered.json", help="Path to JSON with keypoints")
    parser.add_argument("--labels", default="gesture_labels.json", help="Path to gesture label ranges")
    parser.add_argument("--model_out", default="gesture_classifier.pkl", help="Output file for trained model")
    args = parser.parse_args()

    main(args.keypoints, args.labels, args.model_out)
