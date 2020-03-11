"""
Script used to choose the right mic sensibility
"""
from contextlib import suppress

import speech_recognition as sr

import detect_mic_to_use  # Display mics indexes
mic_index = int(input("enter mic index please"))
print("DON'T SPEAK PLEASE (for 10 seconds)")

r = sr.Recognizer()
with sr.Microphone(device_index=mic_index) as source:
    r.adjust_for_ambient_noise(source, duration=10)
    print(f"energy threshold detected: {r.energy_threshold}", flush=True)
    print("You can speak normally to test", flush=True)
    audio = r.listen(source, phrase_time_limit=5)

with suppress(sr.UnknownValueError, sr.RequestError):
    # Call the google voice recognizer
    print(r.recognize_google(audio, language="fr-FR"))
