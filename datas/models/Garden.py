from datas.models.Flower import Flower


class Garden:

    def __init__(self, flower: Flower):
        self.flower = flower
        self.temperature = 0.0
        self.humidity = 0.0
