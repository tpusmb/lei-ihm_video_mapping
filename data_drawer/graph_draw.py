#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging.handlers
import os

import matplotlib.pyplot as plt

from data_drawer import DataDrawer

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/graph_draw.log",
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


class GraphDraw(DataDrawer):

    def __init__(self, title):
        # Graph values
        super().__init__(title)
        self.graph_values = list()
        self.plot = None

    def _reset_graph(self):
        plt.cla()
        plt.ylabel("Health score")
        plt.xlabel("Joure")
        self.plot = self.plot_figure.add_subplot()
        self.plot.set_ylim([0, 100])
        self.plot.plot(self.graph_values)

    def add_value(self, value):
        """

        :param value:
        :return:
        """
        if not self.plot_is_running:
            PYTHON_LOGGER.error("Need to run the graph before")
            return
        self.graph_values.append(value)
        self._reset_graph()


if __name__ == '__main__':
    import cv2

    gui = GraphDraw("Demo")
    gui.start()

    gui.add_value(100)
    cv2.imshow("main", gui.get_figure_cv2_image())
    cv2.waitKey(0)

    gui.add_value(20)
    cv2.imshow("main", gui.get_figure_cv2_image())
    cv2.waitKey(0)

    gui.add_value(50)
    cv2.imshow("main", gui.get_figure_cv2_image())
    cv2.waitKey(0)