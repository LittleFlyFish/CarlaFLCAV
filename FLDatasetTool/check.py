import os
from PIL import Image
import carla

# Connect to the CARLA server
client = carla.Client('localhost', 2000)
client.set_timeout(2.0)

# Get the current world
world = client.get_world()

# Get all the actors in the world
actors = world.get_actors()

# Print the type_id of each actor
for actor in actors:
    print(f'Actor ID: {actor.id}, Type: {actor.type_id}')


# # Specify the directory where the images are located
# image_directory = '/media/data2/ML/Data/nuScences_convert_kitti/train/image_2'
# # '/media/data2/ML/Data/nuScences/samples/CAM_FRONT'
# #'/media/data1/yanran/kitti/training_nuScences/image_2'
#
# # Get a list of all files in the directory
# image_files = os.listdir(image_directory)
#
# # Loop through each file
# for filename in image_files:
#     # Ensure file is a .png before trying to open
#     if filename.endswith('.png'):
#         try:
#             # Try to open the image file and call load() to ensure all data is read
#             img = Image.open(os.path.join(image_directory, filename))
#             img.load()
#         except Exception as e:
#             # If anything goes wrong, print the name of the file
#             print(f"File {filename} could not be opened: {e}")