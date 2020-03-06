import json
import sys
import threading
from time import sleep, time
from typing import Callable, Dict, List

from speech_to_text.basic_speech_to_text import speech_to_text, is_wake_up_word_said
from speech_to_text.plant_intent_recognizer.detect_intent import Intent, RasaIntent
from utils.save_mapping import load

CALLBACK_INTENTS: Dict[Intent, List[Callable[[], None]]] = {}
CALLBACK_ON_ACTIVE: List[Callable[[], None]] = []
CALLBACK_ON_SLEEP: List[Callable[[], None]] = []


def register_function_for_active(f: Callable[[], None]):
    """Register a function to be called every time the voice controller switch to active mode"""
    print(f"Registering {f} for on active")
    CALLBACK_ON_ACTIVE.append(f)
    return f


def _trigger_function_on_active():
    """Trigger all function registered for when the voice controller switch to active mode"""
    for f in CALLBACK_ON_ACTIVE:
        f()


def register_function_for_sleep(f: Callable[[], None]):
    """Register a function to be called every time the voice controller switch to sleep mode"""
    print(f"Registering {f} for on sleep")
    CALLBACK_ON_SLEEP.append(f)
    return f


def _trigger_function_on_sleep():
    """Trigger all function registered for when the voice controller switch to sleep mode"""
    for f in CALLBACK_ON_SLEEP:
        f()


def register_function_for_intent(intent: Intent):
    """Register a function to be called every time an intent is detected by VoiceController"""

    def inner_decorator(f):
        def wrapped(*args, **kwargs):
            response = f(*args, **kwargs)
            return response

        print(f"Registering {f} for intent: {intent.value}")
        functions = CALLBACK_INTENTS.get(intent, [])
        functions.append(f)
        CALLBACK_INTENTS[intent] = functions
        return wrapped

    return inner_decorator


def _trigger_function_on_intent(intent: Intent):
    """Trigger all function registered for this intent"""
    if intent not in CALLBACK_INTENTS:
        return
    functions = CALLBACK_INTENTS[intent]
    for f in functions:
        f()


class VoiceController:

    def __init__(self, active_time_delay=10, noise_level=None, confidence_threshold=0.6, config_file=None):
        """
        :param active_time_delay time in seconds after the keyword was said before being not "active"
        :param noise_level allow to fine tune the ambient noise, leave empy for auto-tune with background listening
        """
        if config_file:
            config = load(config_file)
            rasa_config = config.get('rasa', {})
            url = rasa_config['url']
            headers = json.loads(rasa_config['headers'])
            self._rasa_intent = RasaIntent(url=url, headers=headers)
        else:
            self._rasa_intent = RasaIntent()
        self.active = False
        self._stop = False
        self.active_time_delay = active_time_delay
        self.last_active_time = None
        self.noise_level = noise_level
        self.confidence_threshold = confidence_threshold

        self._thread = threading.Thread(target=self.run, args=())
        self._thread.daemon = True  # Daemonize thread

    def set_mode_active(self):
        print("ACTIVE MODE", flush=True)
        self.active = True
        _trigger_function_on_active()

    def set_mode_sleep(self):
        print("SLEEP MODE", flush=True)
        self.active = False
        _trigger_function_on_sleep()

    def stop(self):
        """Stopping gracefully, might take a few seconds"""
        self._stop = True
        self._thread.join()

    def start(self):
        self._thread.start()  # Call run()

    def run(self):
        self._stop = False
        while not self._stop:
            if self.active:  # We actively listen to user command
                text = speech_to_text(self.noise_level)
                print(f"text: {text}", flush=True)
                if text:
                    intent, confidence = self._rasa_intent.detect_intent(text)
                    print(f"intent: {intent}\n with confidence: {confidence}", flush=True)
                    if confidence > self.confidence_threshold:
                        _trigger_function_on_intent(intent)
                        self.last_active_time = time()
                    else:
                        print(f"Low intent score for text: <{text}>", file=sys.stderr, flush=True)
                        intent = Intent.UNKNOWN_INTENT
                        _trigger_function_on_intent(intent)
                elif time() - self.last_active_time > self.active_time_delay:
                    self.set_mode_sleep()
            elif is_wake_up_word_said():
                self.set_mode_active()
                self.last_active_time = time()
            else:
                print("😴", end='', flush=True)  # Still in sleep mode


if __name__ == '__main__':
    """Example on how to use the register_function_for_intent wrapper"""


    @register_function_for_intent(intent=Intent.SALUTATION)
    def greeting():
        print("Hello !")


    @register_function_for_intent(intent=Intent.SALUTATION)
    def greeting2():
        print("Hello 2 !")


    @register_function_for_intent(intent=Intent.FIN)
    def goodbye():
        print("goodbye !")


    vc = VoiceController(config_file='../projetconfig.json')
    vc.start()
    print("I can continue to do stuff")
    sleep(60)
    print("Time to stop")
    vc.stop()
