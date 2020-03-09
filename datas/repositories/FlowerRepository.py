import matplotlib.pyplot as plt

from datas.models.Flower import Flower, Mood
from utils.utils import fig2opencv_img


class FlowerRepository:
    CHANGE_FLOWER_RANK_MINUTE = 5  # Minute

    def __init__(self, flower: Flower):
        self.flower = flower

    def change_rank(self):
        if not self.flower.is_last_rank():
            self.flower.rank += 1

    def mood_plot(self):
        """
        Plot the mood history of the flower
        :return: (ndarray) Plot made by matplotlib
        """
        fig, ax = plt.subplots()
        y_labels = [Mood.ANGRY.value, Mood.SAD.value, Mood.STANDING.value, Mood.HAPPY.value]
        score = [y_labels.index(m) for m in self.flower.saved_moods]
        xi = list(range(len(self.flower.saved_moods)))
        yi = list(range(len(y_labels)))
        ax.set_xticks(xi)
        ax.set_yticks(yi)
        ax.set_ylim(0, len(y_labels) - 1)
        ax.set_yticklabels(y_labels)
        ax.plot(score)
        return fig2opencv_img(fig)
