from PIL import Image
import os
from tqdm import tqdm

# List of image paths
image_folder = "frames/0.001"
images = sorted([os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith(".jpg")])
# images = ["image1.png", "image2.png", "image3.png"]

# Open images and convert them to RGB mode
frames = []
for img in tqdm(images, desc="Processing images", unit="image"):
    frames.append(Image.open(img).convert("RGB"))

# Save as GIF
frames[0].save("output.gif", save_all=True, append_images=frames[1:], duration=500, loop=0)

print("GIF creation completed!")
