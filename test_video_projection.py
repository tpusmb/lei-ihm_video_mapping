from py_video_mapping import *
from scenario import Scenario
from datas.models.Flower import Flower
from datas.repositories.PlayerRepository import PlayerRepository
from datas.repositories.FlowerRepository import FlowerRepository

py_video_mapping = PyVideoMapping(PyVideoMapping.get_all_screens()[-1])
# py_video_mapping.set_blackout(0, True)
scenario = Scenario(py_video_mapping)

p = PlayerRepository()
p.player.xp += 30
p.player.xp += 40
p.player.xp += 50
p.player.xp += 60

scenario.display_plant_state(2, p.garden)
input("enter top stop")
scenario.display_plant_progression(FlowerRepository(Flower()))
input("enter top stop")
scenario.display_gardener_progression(p)
input("enter top stop")
scenario.display_karaoke()
input("enter top stop")
scenario.display_main_menu()
input("enter top stop")
scenario.display_sub_menu1()
input("enter top stop")
scenario.display_sub_menu2()
input("enter top stop")
scenario.display_action_creuser()
input("enter top stop")
scenario.display_action_placer_bulbe()
input("enter top stop")
scenario.display_action_reboucher_trou()
input("enter top stop")
scenario.display_action_arroser()
input("enter top stop")
scenario.display_good_feedback()
input("enter top stop")
scenario.display_bad_feedback()
input("enter top stop")
scenario.display_incomprehension_feedback()
input("enter top stop")
scenario.display_command_list()
input("enter top stop")

py_video_mapping.stop()
