import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from datas.models.Flower import Flower, Mood
from datas.models.Garden import Garden
from datas.models.Player import Player
from utils.config_reader import ConfigReader
from utils.img_utils import draw_text_onto_image
from utils.utils import fig2opencv_img


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

    def mood_plot(self):
        """
        Plot the mood history of the flower
        :return: (ndarray) Plot made by matplotlib
        """
        # Remove the toolbar
        mpl.rcParams['toolbar'] = 'None'
        # Set the font of the graph
        font = {'weight': 'bold', 'size': 40}
        mpl.rc('font', **font)
        fig, ax = plt.subplots()
        fig.set_size_inches(18, 10)
        y_labels = [Mood.ANGRY, Mood.SAD, Mood.STANDING, Mood.HAPPY]
        score = [y_labels.index(m) for m in self.garden.flower.saved_moods]
        xi = list(range(len(self.garden.flower.saved_moods)))
        yi = list(range(len(y_labels)))
        ax.set_xticks(xi)
        ax.set_yticks(yi)
        ax.set_ylim(0, len(y_labels) - 1)
        ax.set_yticklabels(y_labels)
        ax.tick_params('y', pad=-40)
        ax.plot(score, linewidth=10)
        return fig2opencv_img(fig)
