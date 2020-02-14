from datetime import date
from enum import Enum


class Mood(Enum):
    STANDING = "standing"
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"


class Flower:
    MIN_LEVEL = 1
    MAX_LEVEL = 5

    def __init__(self, mood: Mood, rank: int = 1, planted_at=date.today()):
        self.mood = mood  # based on the last time the plant was looked after
        self.rank = rank
        self.planted_at = planted_at
        self.updated_at = date.today()

    @property
    def rank(self):
        return self.rank

    @rank.setter
    def rank(self, value):
        if self.MIN_LEVEL <= value <= self.MAX_LEVEL:
            self.rank = value
        else:
            raise ValueError
