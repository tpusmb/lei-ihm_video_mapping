#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging.handlers
import os

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from data_drawer import DataDrawer

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/bar_draw.log",
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

MAX_BAR_HEIGHT = 100


class BarDraw(DataDrawer):
    """
        Display percentage in vertical bar. You can add bars during the execution
    """

    def __init__(self, title):
        """

            **Input:**
                * window_title (String): Title of the window
        """
        super().__init__(title)
        # We generate a list of 255 numbers decreasing from 1 to 0 with a regular interval
        self.color_gradient_value = np.atleast_2d(np.linspace(1, 0, 255)).T
        # factor to convert a 0-255 value to 0-1
        fact = 1.0 / 255.0
        # Dictionary of all the different color values starting from red and going to green
        color_gradient_value_dic = {'red': [(0.0, 255 * fact, 255 * fact),
                                            (0.25, 255 * fact, 255 * fact),
                                            (0.5, 255 * fact, 255 * fact),
                                            (0.75, 150 * fact, 150 * fact),
                                            (1.0, 0, 0)],
                                    'green': [(0.0, 0, 0),
                                              (0.25, 50 * fact, 50 * fact),
                                              (0.5, 150 * fact, 150 * fact),
                                              (0.75, 255 * fact, 255 * fact),
                                              (1.0, 255 * fact, 255 * fact)],
                                    'blue': [(0.0, 0, 0),
                                             (0.25, 0, 0),
                                             (0.5, 0, 0),
                                             (0.75, 0, 0),
                                             (1.0, 0, 0)]}
        # Set a white color. Use to hide the color gradient bar
        white_color = {'red': [(0.0, 255 * fact, 255 * fact), (1.0, 255 * fact, 255 * fact)],
                       'green': [(0.0, 255 * fact, 255 * fact), (1.0, 255 * fact, 255 * fact)],
                       'blue': [(0.0, 255 * fact, 255 * fact), (1.0, 255 * fact, 255 * fact)]}
        self.color_gradient = mpl.colors.LinearSegmentedColormap('gray_to_blue', color_gradient_value_dic, 256)
        self.white_color = mpl.colors.LinearSegmentedColormap('white', white_color, 256)
        # Width of each bar
        self.bars_width = 0.2
        # Title put under each bars
        self.title_bars_list = list()
        # Number of bar in the canvas
        self.nb_bars = 0
        # Value of each bars
        self.bars_values = list()
        # Figure of the plot
        self.plot_figure = None
        # All the bars
        self.bars = None

        # The list of all the white bars to hide the gradient bars
        self.white_color_bar = list()
        # position of the bars
        self.list_bar_positions = None

    def _reset_graph(self):
        """
            Reset the graph and add the new bars
        """
        if self.nb_bars == 0:
            return

        # Clear the graph
        plt.cla()
        # Add information
        plt.ylabel('Experience')
        plt.title('Your experience')
        # tiks bar position with the bars title
        plt.xticks(self.list_bar_positions, self.title_bars_list)

        # Create bars
        self.bars = plt.bar(self.list_bar_positions, self.bars_values, self.bars_width)

        # Get the bars axes
        bars_axes = self.bars[0].axes

        # Hide the right and top spines
        bars_axes.spines['right'].set_visible(False)
        bars_axes.spines['top'].set_visible(False)

        # Only show ticks on the left and bottom spines
        bars_axes.yaxis.set_ticks_position('left')
        bars_axes.xaxis.set_ticks_position('bottom')

        # Set the y axes between 0 and 100
        bars_axes.set_ylim((0, MAX_BAR_HEIGHT))
        lim = bars_axes.get_xlim() + bars_axes.get_ylim()

        self.white_color_bar = list()
        for bar in self.bars:
            # Very first display of the bar will be at 100% (1 frame)
            # This is to avoid initialization problems when comparing models.
            bar.set_height(MAX_BAR_HEIGHT)
            bar.set_zorder(1)
            bar.set_facecolor("none")
            bar_x, bar_y = bar.get_xy()
            current_bar_width = bar.get_width()

            # Show the image color on the bars on full graph height
            bars_axes.imshow(self.color_gradient_value,
                             extent=[bar_x, bar_x + current_bar_width, bar_y, MAX_BAR_HEIGHT], aspect="auto",
                             zorder=0, cmap=self.color_gradient)

            # Hide the color gradient image with a white image to the value of the bar
            self.white_color_bar.append(bars_axes.imshow(self.color_gradient_value,
                                                         extent=[bar_x, bar_x + current_bar_width, MAX_BAR_HEIGHT,
                                                                 bar_y + MAX_BAR_HEIGHT],
                                                         aspect="auto",
                                                         zorder=1, cmap=self.white_color))
            bars_axes.imshow(self.color_gradient_value,
                             extent=[bar_x, bar_x + current_bar_width, MAX_BAR_HEIGHT, bar_y + MAX_BAR_HEIGHT],
                             aspect="auto",
                             zorder=1, cmap=self.white_color)

        bars_axes.axis(lim)

    def update_value(self, bar_name, bar_value):
        """
            Update the real value of the bar

            **Input:**
                * bar_name (string): name of the bar to update his value
                * bar_value (int): Value of select bar
        """
        try:
            position = self.title_bars_list.index(bar_name)
        except ValueError:
            PYTHON_LOGGER.error("Can't find {} name in the list".format(bar_value))
            return

        self.bars_values[position] = bar_value

        # Get bar object
        bar = self.bars[position]

        # Update the bar height
        bar.set_height(self.bars_values[position])
        # Get the new position of the bar
        bar_x, bar_y = bar.get_xy()
        # Get dimension
        w, h = bar.get_width(), bar.get_height()

        # Change the bar size
        self.white_color_bar[position].set_extent([bar_x, bar_x + w, MAX_BAR_HEIGHT, bar_y + h])

    def add_bar(self, title):
        """
            Add bar in the plot

            **Input:**
                * title (String): Title of the bar
        """
        self.bars_values.append(MAX_BAR_HEIGHT)
        self.title_bars_list.append(title)
        self.nb_bars += 1
        final_bar_position = 0.3 * self.nb_bars
        # we are using linspace here to get the good number of values for bars positions
        # (7 bars = 7 positions)
        # np.arange is subject to floating point routing problems, that can lead to
        # the wrong number of values being generated in some cases
        self.list_bar_positions = np.linspace(0.0, final_bar_position, self.nb_bars)
        self._reset_graph()


if __name__ == '__main__':
    import cv2

    gui = BarDraw("Demo")
    gui.start()

    gui.add_bar("bar number 1")

    gui.update_value("bar number 1", 10)
    cv2.imshow("main", gui.get_figure_cv2_image())
    cv2.waitKey(0)

    gui.update_value("bar number 1", 20)
    cv2.imshow("main", gui.get_figure_cv2_image())
    cv2.waitKey(0)

    gui.update_value("bar number 1", 50)
    cv2.imshow("main", gui.get_figure_cv2_image())
    cv2.waitKey(0)
