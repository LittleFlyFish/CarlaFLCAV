#!/usr/bin/python3
import csv
import carla
import cv2 as cv
import numpy as np
import transforms3d
import math

from recorder.sensor import Sensor
from utils.geometry_types import Transform, Rotation
from utils.transform import carla_transform_to_transform


class CameraBase(Sensor):
    def __init__(self,
                 uid,
                 name: str,
                 base_save_dir: str,
                 parent,
                 carla_actor: carla.Sensor,
                 color_converter: carla.ColorConverter = None):
        super().__init__(uid, name, base_save_dir, parent, carla_actor)
        self.color_converter = color_converter

    def save_to_disk_impl(self, save_dir, sensor_data) -> bool:
        # Convert to target color template
        if self.color_converter is not None:
            sensor_data.convert(self.color_converter)

        # Convert raw data to numpy array, image type is 'bgra8'
        carla_image_data_array = np.ndarray(shape=(sensor_data.height,
                                                   sensor_data.width,
                                                   4),
                                            dtype=np.uint8,
                                            buffer=sensor_data.raw_data)

        # Save image to [RAW_DATA_PATH]/.../[ID]_[SENSOR_TYPE]/[FRAME_ID].png
        success = cv.imwrite("{}/{:0>10d}.png".format(save_dir,
                                                      sensor_data.frame),
                             carla_image_data_array)

        if success and self.is_first_frame():
            self.save_camera_info(save_dir)

        return success

    def save_camera_info(self, save_dir):
        with open('{}/camera_info.csv'.format(save_dir), 'w', encoding='utf-8') as csv_file:
            fieldnames = {'width',
                          'height',
                          'fx',
                          'fy',
                          'cx',
                          'cy'}
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            camera_info = self.get_camera_info()
            writer.writerow(camera_info)

    # def get_camera_info(self):
    #     camera_width = int(self.carla_actor.attributes['image_size_x'])
    #     camera_height = int(self.carla_actor.attributes['image_size_y'])
    #     fx = camera_width / (
    #             2.0 * math.tan(float(self.carla_actor.attributes['fov']) * math.pi / 360.0))
    #     return {
    #         'width': camera_width,
    #         'height': camera_height,
    #         'cx': camera_width / 2.0,
    #         'cy': camera_height / 2.0,
    #         'fx': fx,
    #         'fy': fx
    #     }

    def get_camera_info(self):
        # 从相机参数中获取图像的宽度和高度（以像素为单位）
        camera_width = 1920 # self.camera_parameters['image_resolution_in_px']['width']
        camera_height = 1080 # self.camera_parameters['image_resolution_in_px']['height']

        # 计算像素尺寸（以毫米为单位）
        pixel_size_in_mm = 0.0029 # self.camera_parameters['pixel_size_in_mm']

        # 计算焦距（以毫米为单位）
        focal_length_in_mm = 3.15 # self.camera_parameters['focal_length_in_mm']

        # 使用以下公式将焦距从毫米转换为像素：
        # Focal length (in pixels) = (Focal length in mm / Pixel size in mm)
        fx = focal_length_in_mm / pixel_size_in_mm
        fy = fx  # 假设 x 和 y 方向的焦距是相同的

        return {
            'width': camera_width,
            'height': camera_height,
            'cx': camera_width / 2.0,
            'cy': camera_height / 2.0,
            'fx': fx,
            'fy': fy
        }

    def get_transform(self) -> Transform:
        c_trans = self.carla_actor.get_transform()
        trans = carla_transform_to_transform(c_trans)
        quat = trans.rotation.get_quaternion()
        quat_swap = transforms3d.quaternions.mat2quat(np.matrix(
                      [[0, 0, 1],
                       [-1, 0, 0],
                       [0, -1, 0]]))
        quat_camera = transforms3d.quaternions.qmult(quat, quat_swap)
        roll, pitch, yaw = transforms3d.euler.quat2euler(quat_camera)
        return Transform(trans.location, Rotation(roll=math.degrees(roll),
                                                  pitch=math.degrees(pitch),
                                                  yaw=math.degrees(yaw)))


class RgbCamera(CameraBase):
    def __init__(self, uid, name: str, base_save_dir: str, parent, carla_actor: carla.Sensor,
                 color_converter: carla.ColorConverter = None):
        super().__init__(uid, name, base_save_dir, parent, carla_actor, color_converter)


class SemanticSegmentationCamera(CameraBase):
    def __init__(self, uid, name: str, base_save_dir: str, parent, carla_actor: carla.Sensor,
                 color_converter: carla.ColorConverter = None):
        color_converter = carla.ColorConverter.CityScapesPalette
        super().__init__(uid, name, base_save_dir, parent, carla_actor, color_converter)


class DepthCamera(CameraBase):
    def __init__(self, uid, name: str, base_save_dir: str, parent, carla_actor: carla.Sensor,
                 color_converter: carla.ColorConverter = None):
        color_converter = carla.ColorConverter.Raw
        super().__init__(uid, name, base_save_dir, parent, carla_actor, color_converter)