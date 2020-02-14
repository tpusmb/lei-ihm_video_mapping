import sys
from time import sleep
from typing import Callable, List

from py_video_mapping import *

from scenario import Scenario
from speech_to_text.plant_intent_recognizer.detect_intent import Intent
from speech_to_text.voice_controller import VoiceController, register_function_for_intent, register_function_for_active, \
    register_function_for_sleep

py_video_mapping = PyVideoMapping(PyVideoMapping.get_all_screens()[1])
scenario = Scenario(py_video_mapping)

NEXT_STEPS: List[Callable[[], None]] = []  # Global var to know what the next function should be


@register_function_for_active
@register_function_for_intent(intent=Intent.SALUTATION)
def display_main_menu():
    scenario.display_main_menu()


@register_function_for_sleep
def stop():
    scenario.blackout()


@register_function_for_intent(intent=Intent.FIN)
def display_karaoke():
    scenario.display_karaoke()
    sleep(30)
    vc.set_mode_sleep()
    scenario.blackout()


@register_function_for_intent(intent=Intent.PLANTER_UN_BULBE)
def start_planting_bulbe():
    global NEXT_STEPS
    NEXT_STEPS = [
        scenario.display_action_creuser,
        scenario.display_action_placer_bulbe,
        scenario.display_action_reboucher_trou,
        scenario.display_action_arroser,
        scenario.display_karaoke,
    ]
    play_next_step()


@register_function_for_intent(intent=Intent.SUIVRE_ETAT_PLANTE)
def entretenir_plante():
    scenario.display_sub_menu1()


@register_function_for_intent(intent=Intent.AFFICHER_PROGRES_DU_JARDINIER)
def progress():
    scenario.display_sub_menu2()


@register_function_for_intent(intent=Intent.AFFICHER_ETAT_PLANTE)
def plant_state():
    scenario.display_plant_state(0)


@register_function_for_intent(intent=Intent.ENTRETENIR_PLANTE)
def happy_plant():
    scenario.display_plant_progression("happy")


@register_function_for_intent(intent=Intent.UNKNOWN_INTENT)
def incomprehension_feedback():
    scenario.display_incomprehension_feedback()


@register_function_for_intent(intent=Intent.POSITIF)
def play_next_step():
    if NEXT_STEPS:
        f = NEXT_STEPS.pop(0)  # Call the first function and remove it from the FIFO
        f()
    else:
        print("Trying to call a next step but there is none", file=sys.stderr, flush=True)


vc = VoiceController(active_time_delay=180, noise_level=2000)
vc.start()
sleep(2)
scenario.display_good_feedback()
sleep(2)
stop()
print("ALL GOOD")
