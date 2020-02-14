#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GNU AFFERO GENERAL PUBLIC LICENSE
    Version 3, 19 November 2007
"""
from NaoCreator.setting import Setting
from NaoSensor.plant import Plant


class Pot(object):
    def __init__(self, data):
        try:
            self.temperature = data["temperature"]
            self.timestamp = data["timestamp"]
            self.soil_moisture = data["soil_moisture"]
            self.light = data["light"]
            self.fertilizer = data["fertilizer"]
            self.nickname = data["nickname"]
        except KeyError as e:
            print(e)
            Setting.error("Uncomplete data given to Pot.__init__")

    def is_ideal_for_plant(self, plant):
        def between(min, max, val):
            return min <= val <= max

        soil_vals = plant.get_data(Plant.VALEURS_IDEALES)["soil_moisture"]
        light_vals = plant.get_data(Plant.VALEURS_IDEALES)["light"]
        temp_vals = plant.get_data(Plant.VALEURS_IDEALES)["temperature"]
        fert_vals = plant.get_data(Plant.VALEURS_IDEALES)["fertilizer"]

        return (between(soil_vals["min"], soil_vals["max"], self.soil_moisture) and
                between(light_vals["min"], light_vals["max"], self.light) and
                between(temp_vals["min"], temp_vals["max"], self.temperature) and
                between(fert_vals["min"], fert_vals["max"], self.fertilizer))


class Jardin(object):
    def __init__(self):
        self.pots = list()

    def reg_pot(self, pot):
        if pot in self.pots:
            Setting.error("Pot {} already in Jardin {}".format(pot, self))
            return False
        if (pot.timestamp, pot.nickname) in [(p.timestamp, p.nickname) for p in self.pots]:
            Setting.error("Pot {} has same timestamp & nickname than another Pot")
            return False

        self.pots += [pot]
        return True

    def nb_pots(self):
        return len(self.pots)
