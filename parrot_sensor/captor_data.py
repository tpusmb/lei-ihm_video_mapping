#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import json
import os

from parrot_sensor import api_cloud
from utils.config_reader import ConfigReader

FOLDER_ABSOLUTE_PATH = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))


class CaptorData:
    """
    Is responsible for retrieving data from the Flower Power Cloud via their API and then organizing it in a list.
    Allows you to easily recover this data.
    """

    def __init__(self, time_delta=24, config_reader: ConfigReader = ConfigReader()):
        """
        Initializes data recovery from the sensor.
        :param time_delta: How many days have the data been recovered
        """
        self.since = (datetime.datetime.now() - datetime.timedelta(hours=time_delta)).strftime("%d-%b-%Y %H:%M:%S")
        self.today = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
        self.config = self.get_projetconfig(config_reader)
        self.user_id = config_reader.Parrot["userid"]
        self.user_code = config_reader.Parrot["usercode"]
        self.password = config_reader.Parrot["passwd"]
        self.have_sensor = self.user_id is not None and self.user_code is not None and self.password is not None
        if self.have_sensor:
            self.connection = api_cloud.ApiCloud(self.user_id, self.user_code)
        else:
            print("off line sensor")
            self.connection = None

    def get_sensor_data(self):
        """
        retrieves data from sensor
        :return:
        """
        if self.have_sensor:
            self.connection = api_cloud.ApiCloud(self.user_id, self.user_code)
            self.connection.login(self.user_id, self.password)
            location_identifier = self.get_identifier_location()
            return self.init_temperature_and_humidity(
                self.connection.get_samples_location(location_identifier, self.since, self.today))
        else:
            return 0, 0

    def get_identifier_location(self):
        """
        recover the position of the plant
        :return:
        """
        if self.have_sensor:
            parrot_data = json.loads(
                json.dumps(self.connection.get_sensor_data_sync()))["locations"][0]["location_identifier"]
            return parrot_data
        else:
            return {}

    @staticmethod
    def init_temperature_and_humidity(filename):
        """
        get temperature and humidity from sensor data
        :param filename: fichier json
        :return:
        """
        temperature = 0
        humidity = 0
        data = json.loads(json.dumps(filename))['samples']
        if len(data):
            temperature = data[len(data) - 1]['air_temperature_celsius']
            humidity = data[len(data) - 1]['calibrated_soil_moisture_percent']
        return temperature, humidity
