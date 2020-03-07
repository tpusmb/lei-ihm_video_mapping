#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GNU AFFERO GENERAL PUBLIC LICENSE
    Version 3, 19 November 2007
"""

import csv
import datetime
import json
import os

from parrot_sensor import api_cloud
from utils import json_io

# Absolute path to the folder location of this python file
FOLDER_ABSOLUTE_PATH = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))

CONFIG = os.path.join(FOLDER_ABSOLUTE_PATH, "..", "projetconfig.json")

class CaptorData:
    """
    Se charge de récupérer les données sur le Cloud de Flower Power via leur API puis de les organiser dans une liste
    de dictionnaire.
    Permet de récupérer facilement ces données.
    """

    def __init__(self, time_delta=2):
        """
        Initialise la récupération de données du capteur.
        :param time_delta: Depuis combien de jours récupérer les données
        """
        self.since = (datetime.datetime.now() - datetime.timedelta(hours=time_delta)).strftime("%d-%b-%Y %H:%M:%S")
        self.today = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
        self.config = self.get_projetconfig(CONFIG)
        self.connection = api_cloud.ApiCloud(self.config[0], self.config[1])

    def get_sensor_data(self):
        """
        recupere les données du capteur température ect.
        :return:
        """
        self.connection = api_cloud.ApiCloud(self.config[0], self.config[1])
        self.connection.login(self.config[0], self.config[2])
        location_identifier = self.get_identifier_location()
        return self.init_temperature_and_humidity(self.connection.get_samples_location(location_identifier, self.since,
                                                                                       self.today))

    def get_identifier_location(self):
        """
        :return:
        """
        parrot_data = json.loads(json.dumps(self.connection.get_sensor_data_sync()))["locations"][0][
            "location_identifier"]
        return parrot_data

    def get_projetconfig(self, filename):
        """
        :param filename: fichier json
        :return: liste avec les infos de connexion
        """
        config_data = list()
        data = json_io.load(filename)
        config_data.append(data["user"]["userid"])
        config_data.append(data["user"]["usercode"])
        config_data.append(data["user"]["passwd"])
        return config_data

    def init_temperature_and_humidity(self, filename):
        """
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
