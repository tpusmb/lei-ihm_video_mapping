#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GNU AFFERO GENERAL PUBLIC LICENSE
    Version 3, 19 November 2007
"""
import json
import os


class Outils(object):
    NOM = "nom"
    TAILLE = "taille"
    DIFFICULTE = "difficulte"
    POIDS = "poids"
    FONCTION = "fonction"
    DETERMINANT = "determinant"
    PLURIEL = "pluriel"
    UTILISATION = "utilisation"



    def __init__(self, filename):
        json_data = open("datas/outils/{}.json".format(filename))
        self.data = json.load(json_data)

    def get_data(self, key):
        """
        Récupère une donnée de l'outil
        :param key: La donnée à récupérer
        :return: La valeur de la donnée
        """
        if len(self.data) == 0:
            print("Erreur! Les données n'ont pas été initialisées!")
            return None
        if key not in self.data:
            print("Erreur! La donnée demandée n'existe pas dans le dictionnaire des données!")
            return None
        return self.data[key]


    #faire une méthode statique qui retourne les noms de plante dans datas.
    @staticmethod
    def get_outils(path = "datas/outils"):
        # Liste des fichiers
        list = os.listdir(path)
        list2 = []
        for i in list:
            # On garde que la partie avant le .json
            list2.append(i.split(".json")[0])
        return list2

    @staticmethod
    def get_outils_obj(path="datas/outils"):
        return [Outils(o) for o in Outils.get_outils()]
