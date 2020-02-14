from datas.models.Flower import Flower, Mood
from datas.models.Player import Player


class PlayerRepository:

    def __init__(self, player=Player(), flower=Flower(Mood.STANDING)):
        self.player = player
        self.flower = flower

    def action_water(self):
        self.player.xp += 5
        self.flower.make_update()

    def action_dig(self):
        self.player.xp += 10
        self.flower.make_update()

    def action_place_bulb(self):
        self.player.xp += 5
        self.flower.make_update()

    def action_reseal(self):
        self.player.xp += 10
        self.flower.make_update()
