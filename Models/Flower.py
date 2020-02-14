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

    def get_mood(self): return self.mood

    def get_level(self): return self.level

    def get_planted_at(self): return self.planted_at

    def get_updated_at(self): return self.updated_at

    def set_mood(self, mood: Mood): self.mood = mood

    def set_level(self, level): self.level = level

    def set_planted_at(self, planted_at: date): self.planted_at = planted_at

    def set_updated_at(self, updated_at): self.updated_at = updated_at
