#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import logging.handlers
import os

import matplotlib as mpl
import matplotlib.image as image
import matplotlib.pyplot as plt
import numpy as np

from utils.utils import fig2opencv_img

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/data_drawer.log",
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


class DataDrawer:

    def __init__(self, title):
        # Title of the window
        self.title = title
        self.img_path = os.path.join(FOLDER_ABSOLUTE_PATH, "assets")
        # Figure of the plot
        self.plot_figure = None

        self.plot_is_running = False

    def get_figure_cv2_image(self):
        """
            Draw all the changes made in the graph
        """
        return fig2opencv_img(self.plot_figure)

    def start(self):

        if self.plot_is_running:
            return
        # Remove the toolbar
        mpl.rcParams['toolbar'] = 'None'
        # Set the font of the graph
        font = {'weight': 'bold', 'size': 25}
        mpl.rc('font', **font)
        self.plot_figure = plt.figure(self.title)
        # Load the splash image
        percentage_icon = image.imread(os.path.join(self.img_path, "percentage_icon.png"))
        # Display the splash image
        self.plot_figure.figimage(percentage_icon, 0, self.plot_figure.bbox.ymax - percentage_icon.shape[0] - 10,
                                  zorder=0, alpha=0.4)
        # Update the canvas
        self.plot_figure.canvas.draw()
        PYTHON_LOGGER.info("Start the ui bar")
        self.plot_is_running = True
