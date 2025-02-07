from moviepy.editor import ImageSequenceClip

# Path to the folder containing images
image_folder = "frames/0.001"
output_video = "slideshow1.mp4"

# List of image filenames
import os
images = sorted([os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith(".jpg")])

# Create a slideshow video
clip = ImageSequenceClip(images, fps=1)  # 2 fps for 0.5 seconds per image
clip.write_videofile(output_video, codec="libx264")
