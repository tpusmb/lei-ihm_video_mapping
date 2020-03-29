"""
Script used to choose the right mic sensibility
"""
from contextlib import suppress

import speech_recognition as sr

# noinspection PyUnresolvedReferences
import detect_mic_to_use  # Display mics indexes

mic_index = int(input("Enter mic index please\n"))
print("DON'T SPEAK PLEASE (for 10 seconds)")

r = sr.Recognizer()
with sr.Microphone(device_index=mic_index) as source:
    r.adjust_for_ambient_noise(source, duration=10)
    print(f"energy threshold detected: {r.energy_threshold}", flush=True)
    print("You can speak normally to test", flush=True)
    audio = r.listen(source, phrase_time_limit=5, timeout=10)
    print("Sending audio to Google for detection", flush=True)

try:
    # Call the google voice recognizer
    print(f'We heard you say: {r.recognize_google(audio, language="fr-FR")}')
except (sr.UnknownValueError, sr.RequestError) as err:
    print(f"An error occurred, did you choose the right mic index ?")
