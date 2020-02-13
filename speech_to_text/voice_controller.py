import threading
from time import sleep, time
from typing import Callable, Dict, List

from basic_speech_to_text import speech_to_text, is_keyword_said, is_wake_up_word_said
from plant_intent_recognizer.detect_intent import RasaIntent, Intent

CALLBACK_INTENTS: Dict[Intent, List[Callable[[], None]]] = {}


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

    def __init__(self, active_time_delay=10):
        """
        :param active_time_delay time in seconds after the keyword was said before being not "active"
        """
        self._rasa_intent = RasaIntent()
        self.active = False
        self._stop = False
        self.active_time_delay = active_time_delay
        self.last_active_time = None

        self._thread = threading.Thread(target=self.run, args=())
        self._thread.daemon = True  # Daemonize thread

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
                text = speech_to_text()
                print(f"text: {text}", flush=True)
                if text:
                    intent = self._rasa_intent.detect_intent(text)
                    print(f"intent: {intent}\n", flush=True)
                    _trigger_function_on_intent(intent)
                    self.last_active_time = time()
                elif time() - self.last_active_time > self.active_time_delay:
                    print("SLEEP MODE", flush=True)
                    self.active = False
            elif is_wake_up_word_said():
                print("ACTIVE MODE", flush=True)
                self.active = True
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


    vc = VoiceController()
    vc.start()
    print("I can continue to do stuff")
    sleep(60)
    print("Time to stop")
    vc.stop()
