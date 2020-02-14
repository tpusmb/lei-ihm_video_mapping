#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GNU AFFERO GENERAL PUBLIC LICENSE
    Version 3, 19 November 2007
"""
import json
import os


class Plant(object):
    NOM = "nom"
    DIFFICULTE = "difficulte"
    TYPE_SOL = "type sol"
    DESCRIPTION = "description"
    NOM_LATIN = "nom latin"
    HAUTEUR_MIN = "hauteur minimum"  # en centimètres
    HAUTEUR_MAX = "hauteur maximum"  # en centimètres
    SEMIS = "semis"
    PLANTATION = "plantation"  # Contient un dico, pour savoir comment planter
    ARROSAGE = "arrosage"
    RECOLTE = "recolte"
    HUMIDITE_MIN = "humidite minimum"
    HUMIDITE_MAX = "humidite maximum"
    ENSOLEILLEMENT_MIN = "ensoleillement minimum"
    ENSOLEILLEMENT_MAX = "ensoleillement maximum"
    TAUX_ENGRAIS_MIN = "taux engrais minimum"
    TAUX_ENGRAIS_MAX = "taux engrais maximum"
    TEMPERATURE_MIN = "temperature minimum"
    TEMPERATURE_MAX = "temperature maximum"
    FAIBLESSE = "faiblesse"  # Vent, soleil, pluie...
    CONSEILS = "conseils"  # Ceux de mémé
    PARASITE = "parasite"  # Les ennemis de la plante
    MALADIE = "maladie"  # Les maladie de la plante
    ENTRETIEN = "entretien"
    TRAITEMENT = "traitement"  # comment repousser les insectes et les maladies
    DETERMINANT = "determinant"  # pour le, la ou l'
    PLURIEL = "pluriel"  # pour connaitre l'écriture du pluriel
    VALEURS_IDEALES = "valeursIdeales"

    def __init__(self, plant_name=""):
        if not plant_name:
            self.data = {}
            return
        json_data = open("datas/plants/{}.json".format(plant_name))
        self.data = json.load(json_data)

    def get_data(self, key):
        """
        Récupère une donnée de la plante
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

    @staticmethod
    def get_plantes(path = "datas/plants"):
        # Liste des fichiers
        list = os.listdir(path)
        list2 = []
        for i in list:
            # On garde que la partie avant le .json
            list2.append(i.split(".json")[0])
        return list2

    @staticmethod
    def get_plantes_obj(path="datas/plants"):
        return [Plant(p) for p in Plant.get_plantes()]

if __name__ == "__main__":
    carotte = Plant("carotte.gnao")
    print "Nom:", carotte.get_data(Plant.NOM), ", Nom latin:", carotte.get_data(Plant.NOM_LATIN)
