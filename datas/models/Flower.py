from datetime import datetime
from enum import Enum

import matplotlib.pyplot as plt
import numpy as np

from utils.config_reader import ConfigReader
from utils.utils import fig2opencv_img


class Mood(Enum):
    """
    All moods of the plant
    """
    STANDING = "standing"
    HAPPY = "happy"
    ANGRY = "angry"
    SAD = "sad"


class Flower:
    """
    Flower model, which represents the flower on the pot
    """
    MIN_RANK = 1
    MAX_RANK = 5

    def __init__(self, rank: int = 1, planted_at=datetime.today(), config_reader=ConfigReader()):
        self.__mood = Mood.STANDING  # based on the last time the plant was looked after
        self.rank = rank
        self.planted_at = planted_at
        self.updated_at = datetime.today()

        self.saved_moods = [Mood.STANDING]  # to save previous moods

        try:
            mood_time_sad = config_reader.Plant.getfloat("mood_time_sad")
        except TypeError:
            mood_time_sad = np.inf

        self.TIME_HAPPY = config_reader.Plant.getfloat("mood_time_happy")
        self.TIME_STANDING = config_reader.Plant.getfloat("mood_time_standing") + self.TIME_HAPPY
        self.TIME_ANGRY = config_reader.Plant.getfloat("mood_time_angry") + self.TIME_STANDING
        self.TIME_SAD = mood_time_sad + self.TIME_ANGRY

    @property
    def mood(self):
        """
        Returns the current mood of the plant.
        We calculate it based on the last time the plant has been treated.
        :return: the mood of the flower
        """
        self.saved_moods.append(self.__mood)
        time = (datetime.today() - self.updated_at).seconds
        time_happy = 0.0 <= time <= self.TIME_HAPPY
        time_standing = self.TIME_HAPPY <= time <= self.TIME_STANDING
        time_angry = self.TIME_STANDING <= time <= self.TIME_ANGRY

        if time_happy:
            self.__mood = Mood.HAPPY
        elif time_standing:
            self.__mood = Mood.STANDING
        elif time_angry:
            self.__mood = Mood.ANGRY
        else:
            self.__mood = Mood.SAD
        return self.__mood

    @mood.setter
    def mood(self, mood: Mood):
        """
        Set the mood of the plant, and reset the last time the plant was treated
        :param mood: The new mood of the plant
        """
        self.saved_moods.append(self.mood.value)
        if mood == Mood.HAPPY:
            self.make_update()
        self.__mood = mood

    @property
    def rank(self):
        return self.__rank

    @rank.setter
    def rank(self, value):
        """
        Set the flower rank, only rank is in interval [MIN_RANK, MAX_RANK]
        :raise ValueError if rank value is not in interval [MIN_RANK, MAX_RANK]
        :param value: Rank value
        """
        if self.MIN_RANK <= value <= self.MAX_RANK:
            self.__rank = value
        else:
            raise ValueError

    def is_last_rank(self):
        return self.rank == self.MAX_RANK

    def make_update(self):
        """
        Refresh update_at field,
        """
        self.updated_at = datetime.today()
