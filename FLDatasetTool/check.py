import os

# Replace with your actual directories
label_dir = "/media/data1/yanran/kitti/training/label_2"
image_dir = "/media/data1/yanran/kitti/training/image_2"

# Get list of all files in both directories
label_files = set(os.listdir(label_dir))
image_files = set(os.listdir(image_dir))

# Remove the file extension for image_files
image_files_no_ext = {os.path.splitext(file)[0] for file in image_files}

# Check for files that exist in label_files but not in image_files
missing_in_image = label_files - image_files_no_ext

# Check for files that exist in image_files but not in label_files
missing_in_label = image_files_no_ext - label_files

# Print out the results
print(f"Files in label_2 but not in image_2: {missing_in_image}")
print(f"Files in image_2 but not in label_2: {missing_in_label}")