from datas.models.Flower import Flower
from py_video_mapping import *
from scenario import Scenario

py_video_mapping = PyVideoMapping(PyVideoMapping.get_all_screens()[-1])
scenario = Scenario(py_video_mapping)

scenario.display_plant_progression(Flower())
input("enter top stop")
scenario.display_karaoke()
input("enter top stop")
scenario.display_main_menu()
input("enter top stop")

py_video_mapping.stop()
