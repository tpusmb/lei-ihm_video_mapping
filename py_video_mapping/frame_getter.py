#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging.handlers
import os
from abc import ABC, abstractmethod

import imutils

from py_video_mapping import FileVideoStream
from utils.img_utils import add_sub_image

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/frame_getter.log",
                                                 when="midnight", backupCount=60)
STREAM_HDLR = logging.StreamHandler()
FORMATTER = logging.Formatter("%(asctime)s %(filename)s [%(levelname)s] %(message)s")
HDLR.setFormatter(FORMATTER)
STREAM_HDLR.setFormatter(FORMATTER)
PYTHON_LOGGER.addHandler(HDLR)
PYTHON_LOGGER.addHandler(STREAM_HDLR)
PYTHON_LOGGER.setLevel(logging.DEBUG)

# Absolute path to the folder location of this python file
FOLDER_ABSOLUTE_PATH = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))


class FrameGetter(ABC):
    """
    Abstract class for frame getter. A frame getter his a class return a frame (from a video, image, etc)
    """

    @abstractmethod
    def get_image(self):
        """
        :return: (ndarray) Return an image
        """
        pass

    @abstractmethod
    def stop(self):
        """
        Stop the frame getter
        """
        pass


class VideoGetter(FrameGetter):

    def __init__(self, path_video, play_audio):
        """
        Read frame into video file
        :param path_video: (string) Path to the video
        :param play_audio: (bool) If true play audio of the video
        """
        self.path_video = path_video
        self.file_video_stream = FileVideoStream(self.path_video, play_audio=play_audio).start()
        self.play_audio = play_audio

    def get_image(self):
        """
        :return: (ndarray) return a frame of the video
        """
        frame = self.file_video_stream.read()
        # If no more frame
        if frame is None:
            # Restart the video reading
            self.file_video_stream.stop()
            self.file_video_stream = FileVideoStream(self.path_video, play_audio=self.play_audio).start()
        # Wait that the video file reading get frame
        while frame is None:
            frame = self.file_video_stream.read()
        return frame

    def stop(self):
        """
        Stop the video file reader
        """
        self.file_video_stream.stop()


class ImageGetter(FrameGetter):

    def __init__(self, image):
        """
        Simple image getter
        :param image: (ndarray) Image to return every get_image
        """
        self.image = image

    def get_image(self):
        """
        :return: (ndarray) return the image
        """
        return self.image

    def stop(self):
        pass


class VideoOnWallpaper(FrameGetter):

    def __init__(self, image, video_path, x_offset, y_offset, width, height, play_video_audio):
        """
        Add a video on wall paper
        :param image: (ndarray) Wallpaper
        :param video_path: (string) Path to the video
        :param x_offset: (int) X position of the video
        :param y_offset: (int) y position of the video
        :param width: (int) width of the video
        :param height: (int) height of the video
        """
        # control the video position
        offset_ok = 0 <= x_offset < image.shape[1] and 0 <= y_offset < image.shape[1]
        # control the dimention
        dim_ok = 0 < width < image.shape[1] and 0 < height < image.shape[0]
        assert offset_ok and dim_ok
        self.video_getter = VideoGetter(video_path, play_video_audio)
        self.image_getter = ImageGetter(image)
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.width = width
        self.height = height

    def get_image(self):
        """
        :return: (ndarray) A frame of the video on a wall paper
        """
        # Get video frame and wall paper
        video_img = self.video_getter.get_image()
        wall_paper = self.image_getter.get_image()
        video_img = imutils.resize(video_img, width=self.width, height=self.height)
        wall_image = add_sub_image(wall_paper, video_img, self.x_offset, self.y_offset)
        return wall_image

    def stop(self):
        """
        Stop video getter and image getter
        """
        self.video_getter.stop()
        self.image_getter.stop()
