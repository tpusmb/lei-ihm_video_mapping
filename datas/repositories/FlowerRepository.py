import matplotlib as mpl
import matplotlib.pyplot as plt

from datas.models.Flower import Flower, Mood
from utils.utils import fig2opencv_img


class FlowerRepository:
    """
    Manage the flower
    """
    CHANGE_FLOWER_RANK_MINUTE = 5  # Minute

    def __init__(self, flower: Flower):
        self.flower = flower

    def change_rank(self):
        """
        Increment the rank of the plant, simply when the limit has not been reached
        """
        if not self.flower.is_last_rank():
            self.flower.rank += 1

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
        score = [y_labels.index(m) for m in self.saved_moods]
        xi = list(range(len(self.saved_moods)))
        yi = list(range(len(y_labels)))
        ax.set_xticks(xi)
        ax.set_yticks(yi)
        ax.set_ylim(0, len(y_labels) - 1)
        ax.set_yticklabels(y_labels)
        ax.tick_params('y', pad=-40)
        ax.plot(score, linewidth=10)
        return fig2opencv_img(fig)
