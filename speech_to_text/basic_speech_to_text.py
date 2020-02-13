"""
File to manage the speech to text for our plant.
"""
import struct
from contextlib import suppress
from time import time
from typing import Union

import pyaudio
import speech_recognition as sr
import pvporcupine


def is_wake_up_word_said(input_device_index=13, sensitivity=0.5, keyword='hey pico', timeout=10):
    keyword_file_path = [pvporcupine.KEYWORD_FILE_PATHS[keyword]]
    num_keywords = len(keyword_file_path)

    porcupine = pvporcupine.create(
        library_path=pvporcupine.LIBRARY_PATH,
        model_file_path=pvporcupine.MODEL_FILE_PATH,
        keyword_file_paths=keyword_file_path,
        sensitivities=[sensitivity] * num_keywords)

    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length,
        input_device_index=input_device_index)

    start = time()
    keyword_said = False
    while not keyword_said and time() - start < timeout:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        if porcupine.process(pcm):
            keyword_said = True
    audio_stream.close()
    porcupine.delete()
    return keyword_said


def is_keyword_said(keyword="ok", noise_level: int = None) -> bool:
    """
    Function called to check if the keyword is said
    Work offline to preserve privacy at home

    This function is DEPRECATED

    :param: keyword the word to be said only to start (SHOULD BE CAREFULLY CHOSEN/TESTED)
    :param: noise_level the level of ambient noise used to detect the end of a phrase
    :return: Is the keyword said or not
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        if noise_level:
            r.energy_threshold = noise_level
        else:
            r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    text = None
    with suppress(sr.UnknownValueError, sr.RequestError):
        text = r.recognize_sphinx(audio)
    return keyword in text if text else False


def speech_to_text(noise_level: int = None) -> Union[None, str]:
    """
    Function called to listen and convert to text the answer of the user.
    Note that the user have to talk in french.
    :param: noise_level the level of ambient noise used to detect the end of a phrase
    :return: The answer of the user
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        if noise_level:
            r.energy_threshold = noise_level
        else:
            r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    with suppress(sr.UnknownValueError, sr.RequestError):
        # Call the google voice recognizer
        return r.recognize_google(audio, language="fr-FR")


if __name__ == "__main__":
    print(speech_to_text())
