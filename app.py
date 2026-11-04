import streamlit as st
import cv2
import numpy as np
import tempfile
import os

st.set_page_config(
    page_title="Sketchify",
    page_icon="🎨",
    layout="wide"
)

st.title("🎨 SKETCHIFY")
st.subheader("Transform your videos into beautiful pencil sketches.")

st.write("Upload a video and let Sketchify turn every frame into art!")

uploaded_file = st.file_uploader(
    "Upload your video",
    type=["mp4", "avi", "mov"]
)


def convert_to_sketch(input_path, output_path):

    cap = cv2.VideoCapture(input_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 25

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    out = cv2.VideoWriter(
        output_path,
        fourcc,
        fps,
        (width, height)
    )

    progress = st.progress(0)

    frame_count = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        inverted = 255 - gray

        blurred = cv2.GaussianBlur(
            inverted,
            (21, 21),
            0
        )

        inverted_blur = 255 - blurred

        sketch = cv2.divide(
            gray,
            inverted_blur,
            scale=256
        )

        sketch = cv2.cvtColor(
            sketch,
            cv2.COLOR_GRAY2BGR
        )

        out.write(sketch)

        frame_count += 1

        if total_frames > 0:
            progress.progress(
                min(frame_count / total_frames, 1.0)
            )

    cap.release()
    out.release()

    progress.empty()


if uploaded_file is not None:

    st.success("Video uploaded successfully!")

    st.video(uploaded_file)

    if st.button("✨ Convert to Sketch"):

        with tempfile.TemporaryDirectory() as temp_dir:

            input_path = os.path.join(
                temp_dir, "input.mp4"
            )

            output_path = os.path.join(
                temp_dir, "sketch.mp4"
            )

            with open(input_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            with st.spinner("Creating your sketch..."):

                convert_to_sketch(
                    input_path,
                    output_path
                )

            with open(output_path, "rb") as f:
                video_bytes = f.read()

            st.success("Your sketch video is ready!")

            st.subheader("🎬 Sketch Preview")

            st.video(video_bytes)

            st.download_button(
                label="⬇️ Download Sketch Video",
                data=video_bytes,
                file_name="sketchify_output.mp4",
                mime="video/mp4"
            )

st.markdown("---")
st.markdown(
    "Made with ❤️ using Python, OpenCV and Streamlit"
)