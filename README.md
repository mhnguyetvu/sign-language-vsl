# Vietnamese Sign Language (VSL) Recognition Toolkit

This repository contains 4 core components:

1. **Q1**: Viết hàm đã mô phỏng lại cử động từ file JSON
2. **Q2**: Train mô hình (SVM)  để phân loại 11 cử chỉ trong gesture_labels.json
3. **Q3**: Tải 50 videos từ youtube.
4. **Q4**: Xây streamlit-based web app để annotate.

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

### Phần 1: Xử lý ảnh/video
#### Question 1: 
```
python src/extract_hand_keypoints.py --video data/videos/asl_cut.mp4
```
#### Question 2:
```
python src/train_gesture_classifier.py --keypoints data/keypoints_filtered.json --labels data/gesture_labels.json
```

### Phần 3: Xây dựng và xử lý dữ liệu
#### Question 1:
```
python download_vsl_videos.py
```

#### Question 2:
```
streamlit run annotations/annotation_tool/app.py
```
