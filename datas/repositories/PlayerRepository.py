from datas.models.Flower import Flower, Mood
from datas.models.Player import Player


class PlayerRepository:
    """
    Example:
    >>> p = PlayerRepository()
    >>> assert p.player.xp == 0
    >>> assert p.player.level == 0
    >>> assert p.xp_percent_to_next_level() == 0
    >>> p.action_hoe()
    >>> assert p.player.xp == 10
    >>> assert p.player.level == 0
    >>> assert p.xp_percent_to_next_level() == 1/3 * 100
    >>> p.action_new_plant()
    >>> assert p.player.xp == 0
    >>> assert p.player.level == 1
    >>> assert p.xp_percent_to_next_level() == 0
    """

    def __init__(self, player=Player(), garden=None):
        self.player = player
        self.garden = garden

    def action_water(self):
        self.player.xp += 5
        self.garden.flower.make_update()

    def action_new_plant(self):
        self.player.xp += 20
        self.garden.flower.make_update()

    def action_hoe(self):
        self.player.xp += 10
        self.garden.flower.make_update()

    def xp_percent_to_next_level(self):
        return self.player.xp / self.player.total_xp_needed_for_next_level() * 100
