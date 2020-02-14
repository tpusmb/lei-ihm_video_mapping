from datas.models.Player import Player


class PlayerRepository:

    def __init__(self, player: Player = Player()):
        self.player = player

    def action_water(self): self.player.xp += 5

    def action_dig(self): self.player.xp += 10

    def action_place_bulb(self): self.player.xp += 5

    def action_reseal(self): self.player.xp += 10
