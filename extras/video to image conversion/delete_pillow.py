from PIL import Image
import numpy as np
import os

def images_are_identical(image_path1, image_path2):
    """
    Return True if the two given PNG images are visually identical,
    ignoring PNG metadata/compression differences.
    """
    with Image.open(image_path1) as img1, Image.open(image_path2) as img2:
        # Convert both images to a common format, e.g. 'RGB'
        img1_rgb = img1.convert('RGB')
        img2_rgb = img2.convert('RGB')
        
        # Check that dimensions match
        if img1_rgb.size != img2_rgb.size:
            return False
        
        # Convert to Numpy arrays for direct comparison
        arr1 = np.array(img1_rgb)
        arr2 = np.array(img2_rgb)
        
        # Check if all pixel values are the same
        return np.array_equal(arr1, arr2)

def remove_duplicate_images_in_folder(folder_path):
    """
    Walk through a folder, compare consecutive PNG images, and delete
    one if they are visually identical.
    """
    # Get a sorted list of PNG files
    all_files = os.listdir(folder_path)
    png_files = sorted([f for f in all_files if f.lower().endswith(".png")])
    
    for i in range(len(png_files) - 1):
        img_path1 = os.path.join(folder_path, png_files[i])
        img_path2 = os.path.join(folder_path, png_files[i + 1])
        
        if images_are_identical(img_path1, img_path2):
            # If they are identical, remove the second (or the first, your choice)
            print(f"Removing {img_path2} because it's identical to {img_path1}")
            os.remove(img_path2)

# Example usage:
# remove_duplicate_images_in_folder("path/to/your/images")
remove_duplicate_images_in_folder("frames")