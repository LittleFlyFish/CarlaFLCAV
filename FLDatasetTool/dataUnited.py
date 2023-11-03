import os
import shutil

def GenerateCalib(calib_path, root_path, num_files, fillnums):

    # Loop to generate and copy files
    for i in range(num_files):
        # Generate the new file name
        new_file_name = str(i).zfill(fillnums) + ".txt"

        # Path to the new file
        new_file_path = f"{destination_folder}/{new_file_name}"

        # Copy the source file to the new file path
        shutil.copy2(source_file, new_file_path)

# Define source and target directories
root = '/media/data1/yanran/CarlaFLCAV/FLDatasetTool'
src_dir = root + '/dataset'
target_dir = root + '/dataset/TotalTraining'

# Define subdirectories to copy
subdirs = ['image_2', 'label_2']

# Create target directories if they don't exist
for subdir in subdirs:
    os.makedirs(os.path.join(target_dir, subdir), exist_ok=True)


# Initialize a counter for PNG files
total_files = 0
# Use os.walk to traverse the directory tree
for dirpath, dirnames, filenames in os.walk(src_dir):
    # Check each file to see if it ends in '.png'
    for filename in filenames:
        if filename.lower().endswith('.png'):
            total_files += 1

# Print the count of PNG files
print(f"There are {total_files} PNG files in {src_dir} and its subdirectories.")

# Calculate total number of digits to maintain in file names
total_digits = 6 # len(str(total_files))

# Second pass to copy and rename files
image_counter = 0
label_counter = 0
for record in os.listdir(src_dir):
    record_path = os.path.join(src_dir, record)
    if os.path.isdir(record_path):
        for vehicle in os.listdir(record_path):
            vehicle_path = os.path.join(record_path, vehicle)
            if os.path.isdir(vehicle_path):
                for kitti_object in os.listdir(vehicle_path):
                    kitti_object_path = os.path.join(vehicle_path, kitti_object)
                    if os.path.isdir(kitti_object_path):
                        for training in os.listdir(kitti_object_path):
                            training_path = os.path.join(kitti_object_path, training)
                            if os.path.isdir(training_path):
                                for subdir in subdirs:
                                    subdir_path = os.path.join(training_path, subdir)
                                    if os.path.isdir(subdir_path):
                                        for filename in os.listdir(subdir_path):
                                            file_path = os.path.join(subdir_path, filename)
                                            if os.path.isfile(file_path):
                                                target_subdir_path = os.path.join(target_dir, subdir)
                                                base, ext = os.path.splitext(filename)
                                                if subdir == 'image_2':
                                                    target_filename = f"{image_counter:0{total_digits}d}{ext}"
                                                    image_counter += 1
                                                if subdir == 'label_2':
                                                    target_filename = f"{label_counter:0{total_digits}d}{ext}"
                                                    label_counter += 1
                                                target_file_path = os.path.join(target_subdir_path, target_filename)
                                                # Copy and rename the file
                                                shutil.copyfile(file_path, target_file_path)


GenerateCalib(target_dir+'calib1382X512.txt', target_dir +'calib', image_counter, total_digits)

