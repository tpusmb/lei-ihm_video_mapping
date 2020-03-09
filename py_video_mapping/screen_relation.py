#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging.handlers
import os

from screeninfo import Monitor

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/screen_relation.log",
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


def creat_monitor(width, height):
    """
    Creat monitor
    :param width: (int) width of the monitor
    :param height: (int) height of the monitor
    :return: (Monitor)
    """
    return Monitor(0, 0, width, height)


class ScreenRelation:

    def __init__(self, ui_screen: Monitor, projector_screen: Monitor):
        """
        Class to have position relation between 2 screen
        :param ui_screen: (Monitor) first screen
        :param projector_screen: (Monitor) second screen
        """
        self.ui_screen = ui_screen
        self.projector_screen = projector_screen

    def to_projector_screen_x(self, ui_screen_x):
        """
        X position onto the first screen
        :param ui_screen_x: (int)
        :return: (int) x position onto the projector
        """
        return int((self.projector_screen.width * ui_screen_x) // self.ui_screen.width)

    def to_projector_screen_y(self, ui_screen_y):
        """
        Y position onto the first screen
        :param ui_screen_y: (int)
        :return: (int) y position onto the projector
        """
        return int((self.projector_screen.height * ui_screen_y) // self.ui_screen.height)

    def to_projector_screen(self, ui_screen_x, ui_screen_y):
        """
        Get the x, y position of the first screen to projector screen
        :param ui_screen_x: (int) X position onto the first screen
        :param ui_screen_y: (int) Y position onto the first screen
        :return: (tuple) projector x, projector y
            x position onto the projector
            y position onto the projector
        """
        new_x = self.to_projector_screen_x(ui_screen_x)
        new_y = self.to_projector_screen_y(ui_screen_y)
        return new_x, new_y
