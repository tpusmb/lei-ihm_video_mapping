from datetime import date
from enum import Enum


class Mood(Enum):
    STANDING = "standing"
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"


class Flower:

    def __init__(self, level, mood: Mood, planted_at=date.today()):
        self.mood = mood  # based on the last time the plant was looked after
        self.level = level
        self.planted_at = planted_at
        self.updated_at = date.today()
