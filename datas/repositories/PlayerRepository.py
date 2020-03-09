from datas.models.Flower import Flower
from datas.models.Garden import Garden
from datas.models.Player import Player
from utils.config_reader import ConfigReader


class PlayerRepository:
    """
    Manage the player
    Create the player, the garden and flower

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

    def __init__(self, player=Player(), config_reader: ConfigReader = ConfigReader(), garden=None):
        self.player = player
        if garden is None:
            self.garden = Garden(Flower(config_reader=config_reader), config_reader)
        else:
            self.garden = garden

    def action_water(self):
        """
        When the player sprinkles plant, his xp is updated
        """
        self.player.xp += 5
        self.garden.flower.make_update()

    def action_new_plant(self):
        """
        When the player plant a new plant, his xp is updated
        """
        self.player.xp += 20
        self.garden.flower.make_update()

    def action_hoe(self):
        """
        When the player hoes a plant, his xp is updated
        :return:
        """
        self.player.xp += 10
        self.garden.flower.make_update()

    def xp_percent_to_next_level(self):
        """
        Enough XP for the next level
        """
        return self.player.xp / self.player.total_xp_needed_for_next_level() * 100
