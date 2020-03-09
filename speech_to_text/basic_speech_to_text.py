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


def is_wake_up_word_said(input_device_index=18, sensitivity=0.5, keyword='hey pico', timeout=10):
    keyword_file_path = [pvporcupine.KEYWORD_FILE_PATHS[keyword]]
    num_keywords = len(keyword_file_path)

    # Load the porcupine model
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


def speech_to_text(mic_index, noise_level: int = None) -> Union[None, str]:
    """
    Function called to listen and convert to text the answer of the user.
    Note that the user have to talk in french.
    :param: noise_level the level of ambient noise used to detect the end of a phrase
    :return: The answer of the user
    """
    r = sr.Recognizer()
    with sr.Microphone(device_index=mic_index) as source:
        if noise_level:
            r.energy_threshold = noise_level
        else:
            r.adjust_for_ambient_noise(source)
        audio = r.listen(source, phrase_time_limit=5)

    with suppress(sr.UnknownValueError, sr.RequestError):
        # Call the google voice recognizer
        return r.recognize_google(audio, language="fr-FR")


if __name__ == "__main__":
    mic_index = input('enter the mic index please')
    print(speech_to_text(mic_index))
