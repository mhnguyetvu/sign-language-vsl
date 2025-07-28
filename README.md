# Vietnamese Sign Language (VSL) Recognition Toolkit

This repository contains 4 core components:

1. **Keypoint Extraction (Q1)**: Extract 21 hand landmarks using MediaPipe.
2. **Gesture Classification (Q2)**: Train a classifier (SVM) to classify gestures from frame keypoints.
3. **Video Collection (Q3)**: Metadata + storage of at least 50 VSL videos.
4. **Annotation Tool (Q4)**: Streamlit-based web app for labeling gestures in video.

# Project Structure
```
sign-language-vsl/
├── data/
│   ├── videos/                    # Video thô (.mp4)
│   ├── metadata.jsonl             # Metadata các video
│   ├── gesture_labels.json        # Label dạng (start–end–label)
│   └── keypoints_filtered.json    # Output từ MediaPipe
│
├── annotations/
│   ├── annotations.json           # File chứa nhãn người dùng gán
│   └── annotation_tool/           # Tool web để gán nhãn
│       ├── app.py
│       └── requirements.txt
│
├── src/
│   ├── extract_hand_keypoints.py  # Câu hỏi 1: Trích keypoints từ video
│   ├── train_gesture_classifier.py# Câu hỏi 2: Train mô hình phân loại
│   └── utils.py                   # Hàm chung xử lý keypoints/data
│
├── notebooks/
│   └── visualize_data.ipynb       # Phân tích keypoints, vẽ demo
│
├── README.md                      # Giải thích 4 câu hỏi & hướng dẫn
├── .gitignore
└── requirements.txt
```

## Answer

### 1. Install
```bash
pip install -r requirements.txt
```

### 2. Question
#### Question 1: 
```
python src/extract_hand_keypoints.py --video data/videos/asl_cut.mp4
```
#### Question 2:
```
python src/train_gesture_classifier.py --keypoints data/keypoints_filtered.json --labels data/gesture_labels.json
```
#### Question 3:
