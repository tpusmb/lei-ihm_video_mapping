import numpy as np

from datas.models.Flower import Flower
from datas.models.Garden import Garden
from datas.models.Player import Player
from utils.config_reader import ConfigReader
from utils.img_utils import draw_text_onto_image


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

    def __init__(self, player=Player(), config_reader: ConfigReader = ConfigReader(), garden=None):
        self.player = player
        if garden is None:
            self.garden = Garden(Flower(config_reader=config_reader), config_reader)
        else:
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

    def xp_bar_draw(self):
        """
        Creat an image 1080x700 with a color rectangle represent the player xp
        :param xp_in_percent: (int) Xp of the player in %
        :return: (ndarray) an 1080x700 image
        """
        xp_in_percent = self.xp_percent_to_next_level()
        max_width = 1080
        height = 700
        width = int((xp_in_percent * max_width) // 100)
        img = np.zeros((height, max_width, 3), np.uint8)

        x = np.ones((height, width, 3))
        x[:, :, 0:3] = np.random.randint(0, 200, (3,))
        img[:, 0:width] = x
        return draw_text_onto_image(img, "{}%".format(int(xp_in_percent)), width // 2, height // 2, 3, (255, 255, 255))
