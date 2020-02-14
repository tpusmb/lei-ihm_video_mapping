class Player:
    LEVEL_1 = 30
    STEP_LEVEL = 10

    def __init__(self, name: str = "LEI"):
        self.name = name
        self.level = 0
        self.xp = 0

    @property
    def xp(self): return self.xp

    @xp.setter
    def xp(self, value):
        self.xp = value
        if self.LEVEL_1 + self.STEP_LEVEL * self.level == self.xp:
            self.level += 1
            self.xp = 0
