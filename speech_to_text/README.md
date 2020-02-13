# speech_to_text
A speech to text to control an IoT object

>This project is launched with a python 3.6

> On Ubuntu, you need to run:  
> `sudo apt update && sudo apt-get install portaudio19-dev swig libpulse-dev libasound2-dev`   
> `pip install --upgrade pyaudio`

To run the underlying rasa server __look at [this documentation](plant_intent_recognizer/README.md)__

The start script is [voice_controller.py](voice_controller.py)

To use is_wake_up_word_said function, you need to figure out the index of your mic, to do that, you can run:
```python
import pyaudio
p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    print(p.get_device_info_by_index(i))
```

And choose the one with the `'name': 'default'`