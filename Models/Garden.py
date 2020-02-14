from Models import Flower


class Garden:

    def __init__(self, flower: Flower):
        self.flower = flower
        self.temperature = 0.0
        self.humidity = 0.0

    def get_flower(self): return self.flower

    def get_temperature(self): return self.temperature

    def get_humidity(self): return self.humidity

    def set_flower(self, flower: Flower): self.flower = flower

    def set_temperature(self, temperature): self.temperature = temperature

    def set_humidity(self, humidity): self.humidity = humidity
