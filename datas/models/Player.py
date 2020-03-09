class Player:
    """
    Player Model, which represents the user of our system

    Example:
    >>> p = Player()
    >>> assert p.name == "LEI"
    >>> assert p.level == 0
    >>> assert p.xp == 0
    >>> assert p.total_xp_needed_for_next_level() == 30

    XP is retained through level up
    >>> p.xp += 50
    >>> assert p.level == 1
    >>> assert p.xp == 20
    >>> assert p.total_xp_needed_for_next_level() == 40

    multiple level up in a single time is supported
    >>> p.xp += 100
    >>> assert p.level == 3
    >>> assert p.xp == 30
    >>> assert p.total_xp_needed_for_next_level() == 60
    """
    MIN_XP_LEVEL_1 = 30
    STEP_LEVEL = 10  # used to calculate xp necessary needed for each level

    def __init__(self, name: str = "LEI"):
        self.name = name
        self.level = 0
        self.xp = 0

    @property
    def xp(self): return self.__xp

    @xp.setter
    def xp(self, value: int):
        """
        Set the player xp, and raise the level of the player when the XP is satisfied
        :param value: The xp value
        :return: player's xp
        """
        self.__xp = value
        while self.xp >= self.total_xp_needed_for_next_level():
            self.__xp = self.xp - self.total_xp_needed_for_next_level()
            self.level += 1

    def total_xp_needed_for_next_level(self):
        return self.MIN_XP_LEVEL_1 + self.STEP_LEVEL * self.level
