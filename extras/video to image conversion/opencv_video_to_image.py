import cv2
import os
import sys

def extract_frames(video_path, output_folder):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Total number of frames in the video
    frame_rate = cap.get(cv2.CAP_PROP_FPS)  # Frame rate of the video
    prev_frame = None
    frame_id = 0

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    print("Starting frame extraction...")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if prev_frame is not None:
            diff = cv2.absdiff(frame, prev_frame)
            if diff.mean() > 10:  # Adjust threshold for pixel difference
                output_path = os.path.join(output_folder, f"frame_{frame_id:04d}.jpg")
                cv2.imwrite(output_path, frame)

        prev_frame = frame
        frame_id += 1

        # Update progress
        progress = (frame_id / total_frames) * 100
        sys.stdout.write(f"\rProgress: {progress:.2f}%")
        sys.stdout.flush()

    cap.release()
    print("\nFrame extraction completed.")

# Example usage
extract_frames("PCA.mp4", "opencv_output_images")
