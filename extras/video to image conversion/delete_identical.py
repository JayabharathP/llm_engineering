import os
import cv2
import numpy as np
from tqdm import tqdm

def remove_identical_images(folder):
    # Gather all .png files in the folder, sorted alphabetically
    files = sorted([f for f in os.listdir(folder) if f.lower().endswith('.png')])

    prev_image = None
    prev_file = None

    for filename in tqdm(files, desc="Processing images", unit="image"):
        path = os.path.join(folder, filename)
        
        # Read current image in 'unchanged' mode (so alpha channel is preserved)
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        
        if img is None:
            print(f"Warning: could not read '{path}'. Skipping.")
            continue

        # Debug: show shape of current image
        print(f"Checking {filename}, shape = {img.shape}")

        if prev_image is None:
            # First image in the sequence
            prev_image = img
            prev_file = path
        else:
            # Check if current image has the same dimensions
            if img.shape == prev_image.shape:
                # Compute absolute difference
                diff = cv2.absdiff(img, prev_image)
                # Sum of all differences
                diff_sum = np.sum(diff)

                if diff_sum == 0:
                    # Exactly the same pixel-wise
                    os.remove(path)
                    print(f"Deleted identical file: {path}")
                else:
                    # Different image
                    prev_image = img
                    prev_file = path
                    print(f"Images differ by {diff_sum} in pixel values.")
            else:
                # Different shapes => definitely not identical
                prev_image = img
                prev_file = path
                print(f"Different shapes: {img.shape} vs {prev_image.shape} (previous).")

if __name__ == "__main__":
    folder_path = "frames"
    remove_identical_images(folder_path)
    print("Done checking consecutive PNG images for duplicates.")
