from datetime import datetime
from enum import Enum


class Mood(Enum):
    STANDING = "standing"
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"


class Flower:
    MIN_RANK = 1
    MAX_RANK = 5

    def __init__(self, mood: Mood, rank: int = 1, planted_at=datetime.today()):
        self.mood = mood  # based on the last time the plant was looked after
        self.rank = rank
        self.planted_at = planted_at
        self.updated_at = datetime.today()

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
