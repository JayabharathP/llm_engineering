from PIL import Image
from fpdf import FPDF
import os
from tqdm import tqdm

# List of image paths
image_files = [f for f in os.listdir(r"frames\0.001") if os.path.isfile(os.path.join(r"frames\0.001", f))]

# Create a PDF
pdf = FPDF()
for image in tqdm(image_files):
    img_path = os.path.join(r"frames\0.001", image)
    img = Image.open(img_path)
    width, height = img.size
    width_mm = width * 0.264583  # Convert pixels to millimeters
    height_mm = height * 0.264583  # Convert pixels to millimeters
    pdf.add_page()
    # pdf.image(img_path, 0, 0, width_mm, height_mm)
    pdf.image(img_path)
pdf.output("output.pdf")