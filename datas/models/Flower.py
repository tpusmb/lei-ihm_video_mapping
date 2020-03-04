from datetime import datetime
from enum import Enum

import config


class Mood(Enum):
    STANDING = "standing"
    HAPPY = "happy"
    ANGRY = "angry"
    SAD = "sad"


class Flower:
    MIN_RANK = 1
    MAX_RANK = 5

    def __init__(self, rank: int = 1, planted_at=datetime.today()):
        self.mood = Mood.STANDING  # based on the last time the plant was looked after
        self.rank = rank
        self.planted_at = planted_at
        self.updated_at = datetime.today()

        self.TIME_HAPPY = config.MOOD_TIME_HAPPY
        self.TIME_STANDING = config.MOOD_TIME_STANDING + self.TIME_HAPPY
        self.TIME_ANGRY = config.MOOD_TIME_ANGRY + self.TIME_STANDING
        self.TIME_SAD = config.MOOD_TIME_SAD + self.TIME_ANGRY

    @property
    def mood(self):
        time = (datetime.today() - self.updated_at).seconds
        time_happy = 0.0 <= time <= self.TIME_HAPPY
        time_standing = self.TIME_HAPPY <= time <= self.TIME_STANDING
        time_angry = self.TIME_STANDING <= time <= self.TIME_ANGRY

        if time_happy:
            return Mood.HAPPY
        elif time_standing:
            return Mood.STANDING
        elif time_angry:
            return Mood.ANGRY
        else:
            return Mood.SAD

    @mood.setter
    def mood(self, mood: Mood):
        if mood == Mood.HAPPY:
            self.make_update()
        self.__mood = mood

    @property
    def rank(self):
        return self.__rank

    @rank.setter
    def rank(self, value):
        if self.MIN_RANK <= value <= self.MAX_RANK:
            self.__rank = value
        else:
            raise ValueError

    def is_last_rank(self):
        return self.rank == self.MAX_RANK

    def make_update(self):
        self.updated_at = datetime.today()
