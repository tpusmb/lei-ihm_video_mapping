#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GNU AFFERO GENERAL PUBLIC LICENSE
    Version 3, 19 November 2007
"""
from __future__ import unicode_literals
import sys
import codecs
import NaoSensor.plant as p
import json
import os


template = {
    "nom": None,
    "nom latin": None,
    "difficulte": None,
    "hauteur minimum": None,
    "hauteur maximum": None,
    "type de sol": None,
    "plantation": {
        "date": None,
        "creuser": None,
        "engrais": None,
        "planter": None,
        "recouvrir": None,
        "arroser": None
    },
    "arrosage": None,
    "recolte": None,
    "humidite minimum": None,
    "humidite maximum": None,
    "ensoleillement minimum" : None,
    "ensoleillement maximum" : None,
    "temperature minimum" : None,
    "temperature maximum" : None,
    "taux engrais minimum" : None,
    "taux engrais maximum" : None,
    "faiblesse": None,
    "parasite": None,
    "maladie": None,
    "entretien": None,
    "determinant": None,
    "pluriel": None
}

def choix():
    choix = raw_input("Veux tu ajouter une nouvelle plante ou changer une plante déjà existante ? o pour l'ajout et n pour changer. \n")
    if choix == 'o':
        add_plante()
    else:
        modif_plante()

def get_file_name():
    file_name = raw_input("Quelle est la plante que tu veux ajouter ? \n")
    list = p.Plant.get_plantes(path="../datas/plants")
    while file_name in list:
        print "Fichier déjà existant"
        file_name = raw_input("Quelle est la plante que tu veux ajouter ? \n")
    return file_name

def get_file_name_existant():
    file_name = raw_input("Quelle est la plante que tu veux modifier ? \n")
    list = p.Plant.get_plantes(path="../datas/plants")
    while file_name not in list:
        print "Fichier non existant \n"
        file_name = raw_input("Quelle est la plante que tu veux modifier ? \n")
    return file_name

def add_plante():
    """
    :return:
    """
    plante_name = get_file_name()
    template["nom"] = plante_name
    for k in template:
        if k != "nom":
            if type(template[k]) == dict:
                for k_sous_dict in template[k]:
                    choix = raw_input(u"{} \n".format(k_sous_dict)).decode(sys.stdin.encoding)
                    template[k][k_sous_dict] = choix
            else:
                choix = raw_input(u"{} \n".format(k)).decode(sys.stdin.encoding)
                template[k] = choix
    json.dump(template, codecs.open("../datas/plants/{}.json".format(plante_name), 'w', 'utf-8'))

def modif_plante():
    """
        :return:
        """
    plante_name = get_file_name_existant()
    plante = open ("../datas/plants/{}.json".format(plante_name))
    jp = json.load(plante)
    cle = raw_input("Quelle phrase veux tu changer ? (arrosage, recolte....) \n")
    directory = "../datas/plants"
    nom = False
    while cle not in jp:
        print("Rentre un mot parmi ces clés : nom, difficulte, hauteur minimum...")
        cle = raw_input(u"Quelle phrase veux tu changer ? (arrosage, recolte....) \n")
    if cle == "nom":
        print ("Voici ce que tu avais mis : \n")
        valeur = jp[cle]
        print (cle, valeur)
        choix = raw_input(u"{} \n".format(cle)).decode(sys.stdin.encoding)
        jp[cle] = choix
        nom = True
    elif cle == "plantation":
        cle2 = raw_input("Que veux tu modifier dans plantation ?(date, creuser, engrais, planter, recouvrir, arroser)")
        print ("Voici ce que tu avais mis : \n")
        valeur = jp[cle][cle2]
        print (cle2, valeur)
        choix = raw_input(u"{} \n".format(cle2)).decode(sys.stdin.encoding)
        jp[cle][cle2] = choix
    else:
        print ("Voici ce que tu avais mis : \n")
        valeur = jp[cle]
        print (cle, valeur)
        choix = raw_input(u"{} \n".format(cle)).decode(sys.stdin.encoding)
        jp[cle] = choix
    json.dump(jp, codecs.open("../datas/plants/{}.json".format(plante_name), 'w', 'utf-8'))
    plante.close()
    if nom == True:
        old = os.path.join(directory, valeur + ".json")
        new = os.path.join(directory, choix + ".json")
        os.rename(old, new)

if __name__ == "__main__":
    choix()
    answer = raw_input("Continuer ? <n/o> (n: non / o: oui) ")
    while answer != 'n':
        if answer == 'o':
            choix()
        answer = raw_input("Continuer ? <n/o> (n: non / o: oui) ")