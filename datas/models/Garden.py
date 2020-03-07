from datas.models.Flower import Flower
from parrot_sensor.captor_data import CaptorData
from utils.config_reader import ConfigReader


class Garden:

    def __init__(self, flower: Flower, config_reader: ConfigReader = ConfigReader()):
        self.flower = flower
        self.captor_data = CaptorData(config_reader)
        self.temperature = 0
        self.humidity = 0
        self.refresh_data()

    def refresh_data(self):
        self.temperature, self.humidity = self.captor_data.get_sensor_data()
