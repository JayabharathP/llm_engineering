import os

# Specify the folder containing the files
folder_path = r'frames\0.001'

# Fetch all files with the desired pattern from the folder
files = [f for f in os.listdir(folder_path) if f.startswith("out_") and f.endswith(".jpg")]

# Sort files to maintain numerical order
files.sort()

# Rename files with consecutive numbers
for i, file_name in enumerate(files, start=1):
    # Construct new file name with zero-padded numbers
    new_name = f"out_{i:03}.jpg"  # Example: out_001.jpg, out_002.jpg
    # Full paths
    old_file = os.path.join(folder_path, file_name)
    new_file = os.path.join(folder_path, new_name)
    # Rename file
    os.rename(old_file, new_file)
    print(f"Renamed: {file_name} -> {new_name}")

print("Renaming completed.")
