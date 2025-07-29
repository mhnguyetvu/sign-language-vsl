import streamlit as st
import json
import os

st.set_page_config(layout="centered", page_title="Gesture Annotation Tool")

VIDEO_DIR = "data/videos"
OUTPUT_JSON = "annotations/annotations.json"

if not os.path.exists("annotations"):
    os.makedirs("annotations")

st.title("🎥 Video Annotation Tool – Sign Language")

video_files = [f for f in os.listdir(VIDEO_DIR) if f.endswith(".mp4")]
selected_video = st.selectbox("🎬 Chọn video để annotate", video_files)

video_path = os.path.join(VIDEO_DIR, selected_video)
st.video(video_path)

st.subheader("📝 Nhập thông tin annotation")
start_time = st.number_input("Start time (giây)", min_value=0.0, value=0.0, step=0.1)
end_time = st.number_input("End time (giây)", min_value=0.0, value=1.0, step=0.1)
label = st.text_input("Gesture Label (e.g. Hello, Thanks)")
translation = st.text_input("Vietnamese Translation (e.g. Xin chào, Cảm ơn...)")

if st.button("✅ Thêm annotation"):
    entry = {
        "video_id": selected_video,
        "start_time": float(start_time),
        "end_time": float(end_time),
        "label": label,
        "translation": translation
    }

    # Load existing
    annotations = []
    if os.path.exists(OUTPUT_JSON):
        with open(OUTPUT_JSON, "r") as f:
            try:
                annotations = json.load(f)
            except:
                annotations = []

    annotations.append(entry)
    with open(OUTPUT_JSON, "w") as f:
        json.dump(annotations, f, indent=2, ensure_ascii=False)

    st.success("✅ Annotation saved!")

st.markdown("---")
st.subheader("📄 Annotation Preview")
if os.path.exists(OUTPUT_JSON):
    with open(OUTPUT_JSON) as f:
        st.json(json.load(f))
