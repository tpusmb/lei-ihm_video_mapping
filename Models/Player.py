class Player:

    def __init__(self, name: str = "LEI"):
        self.name = name
        self.level = 0
        self.xp = 0

    def get_name(self): return self.name

    def get_level(self): return self.level

    def get_xp(self): return self.xp

    def set_name(self, name: str): self.name = name

    def set_level(self, level: int): self.level = level

    def set_xp(self, xp: int): self.xp = xp
