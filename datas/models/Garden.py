from datas.models.Flower import Flower
from parrot_sensor.captor_data import CaptorData
from utils.config_reader import ConfigReader


class Garden:
    """
    Garden Model, which represents the garden
    We can have lots of information about the garden, such as the temperature and humidity of the garden
    """

    def __init__(self, flower: Flower, config_reader: ConfigReader = ConfigReader()):
        self.flower = flower
        self.captor_data = CaptorData(config_reader=config_reader)
        self.target_temperature = config_reader.Plant.getfloat("target_temperature", 17)
        self.target_humidity = config_reader.Plant.getfloat("target_humidity", 20)
        self.temperature = 0
        self.humidity = 0
        self.refresh_data()

    def refresh_data(self):
        """
        Update garden and humidity from the captor data
        """
        self.temperature, self.humidity = self.captor_data.get_sensor_data()

    def compute_flower_rank(self):
        diff_temperature = abs(self.temperature - self.target_temperature)
        diff_humidity = abs(self.humidity - self.target_humidity)
        rank = Flower.MAX_RANK - diff_temperature / 3 + diff_humidity / 3
        return max(rank, Flower.MIN_RANK)
