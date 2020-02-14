#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GNU AFFERO GENERAL PUBLIC LICENSE
    Version 3, 19 November 2007
"""

import csv
import datetime

import api_cloud
import csv_dump

class CaptorData(object):
    """
    Se charge de récupérer les données sur le Cloud de Flower Power via leur API puis de les organiser dans une liste
    de dictionnaire.
    Permet de récupérer facilement ces données.
    """

    NICKNAME = "nickname"
    TIMESTAMP = "timestamp"
    FERTILIZER = "fertilizer"
    SOIL_MOISTURE = "soil_moisture"  # percent
    TEMPERATURE = "temperature"  # celsius
    LIGHT = "light"

    def __init__(self, client_id="faubet.mael@gmail.com",
                 client_secret="7vhQGmU3BP0cmJhIamnH7Pyxr3yo8XoU6B4jOShVFK8ZtCdS",
                 username="speedbirds@hotmail.fr",
                 password="darkofthemoon3", time_delta=7, do_init=True):
        """
        Initialise la récupération de données du capteur.
        :param client_id: Identifiant du client
        :param client_secret: Clé secrète du client
        :param username: Nom d'utilisateur
        :param password: Mot de passe
        :param time_delta: Depuis combien de jours récupérer les données
        """
        if not do_init:
            self.data = list()
            return
        since = (datetime.datetime.now() - datetime.timedelta(days=time_delta)).strftime("%d-%b-%Y %H:%M:%S")
        today = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")

        self.connection = api_cloud.ApiCloud(client_id, client_secret)
        self.connection.login(username, password)
        csv_dump.dump_all_flower_power(self.connection, since, today)
        self.data = list()

    @staticmethod
    def get_data_from_csv_file(filename):
        """
        Récupère les données d'un fichier .csv (formatté pour le Flower Power) et les place dans un tableau de
        dictionnaire de la forme:
        {"timestamp": date d'acquisition,
         "fertilizer_level": niveau d'engrais,
         "soil_moisture_percent": niveau d'humidité,
         "air_temperature_celsius": témpérature (°C),
         "light": lumière (en lux)}
        :param filename: Nom du fichier où extraire les données
        """
        c = CaptorData(do_init=False)

        reader = csv.reader(open(filename, "rb"))

        for row in reader:
            time = datetime.datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
            try:
                rowdic = {
                    CaptorData.NICKNAME: row[0],
                    CaptorData.TIMESTAMP: time,
                    CaptorData.FERTILIZER: float(row[2]),
                    CaptorData.LIGHT: float(row[3]),
                    CaptorData.SOIL_MOISTURE: float(row[4]),
                    CaptorData.TEMPERATURE: float(row[5])
                }
            except Exception as e:
                print ("Erreur lors de la lecture des données du capteur !\n" + e.message)
            c.data += [rowdic]

        return c

    def get_datas(self, quarter_of_hour=0):
        """
        Récupère toutes les données correspondant à un quart d'heure (à partir du dernier)
        ex: le quart d'heure 0 correspond à la toute dernière donnée récupérée.
        :param quarter_of_hour: Le quart d'heure nous intéressant
        :return: Un dictionnaire contenant les données du quart d'heure donné en paramètre
        """
        if len(self.data) == 0:
            import NaoCreator.setting as s
            s.Setting.error("get_datas on Uninitialized Captor !")
            return None
        return self.data[-(quarter_of_hour + 1)]

    def get_data(self, key, quarter_of_hour=0):
        """
        Récupère une certaine donnée correspondant à un quart d'heure (à partir du dernier)
        ex: le quart d'heure 0 correspond à la toute dernière donnée récupérée.
        :param key: Le nom de la donnée à récupérer
        :param quarter_of_hour: Le quart d'heure nous intéressant
        :return: La donnée correspondant au quart d'heure donné en paramètre
        """
        if len(self.data) == 0:
            import NaoCreator.setting as s
            s.Setting.error("CaptorData.get_datas: get_datas on Uninitialized Captor !")
            return None
        return self.data[-(quarter_of_hour + 1)][key]

    def get_avg_data(self, key, since=0, to=0):
        """
        Récupère la valeur moyenne d'une donnée sur une période donnée (par quart d'heures)
        :param key: Le nom de la donnée à récupérer
        :param since: Le quart d'heure depuis quand analyser
        :param to: Le quart d'heure jusqu'où analyser
        :return: La moyenne de cette donnée sur la durée since->to
        """
        if to > since:
            return sum([i[key] for i in self.data[len(self.data)-to: len(self.data)-since]])/float((to-since))
        elif to == since:
            return self.data[-(to + 1)][key]
        else:
            import NaoCreator.setting as s
            s.Setting.error("CaptorData.get_avg_data: ")

datas = [csv_dump.datas_directory + csv_dump.basename + "Bernard" + csv_dump.extension,
         csv_dump.datas_directory + csv_dump.basename + "Giselle" + csv_dump.extension]

try:

    __tmpCaptorData = CaptorData()

    cpt_bernard = __tmpCaptorData.get_data_from_csv_file(datas[0])
    cpt_giselle = __tmpCaptorData.get_data_from_csv_file(datas[1])
    cpts = {"Bernard": cpt_bernard,
            "Giselle": cpt_giselle}

except Exception as e:
    cpt_giselle = CaptorData.get_data_from_csv_file(datas[1])
    print "error captor data: ", e
