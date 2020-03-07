#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import configparser
import logging.handlers
import os

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/config_reader.log",
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


class ConfigReader:
    """
    Example usage:
    config.ini:
        [SectionA]
        param1=toto
        param2 = titi

        [SectionB]
        param3=zoro

    Class usage:
    config = ConfigReader("config.ini")
    config.SectionA["param1"]
    """

    def __init__(self, absolute_path_config_file="config.ini"):
        """
        :param absolute_path_config_file:
        """
        self.config = configparser.ConfigParser(allow_no_value=True)
        if len(self.config.read(absolute_path_config_file)) == 0:
            raise FileNotFoundError("The config file {} his not found !".format(absolute_path_config_file))
        try:
            self.__dict__.update(self.config)
        except Exception as e:
            PYTHON_LOGGER.error("Error to load the configurations: {}".format(e))


if __name__ == "__main__":
    config = ConfigReader("../config.ini")
    print(config)
