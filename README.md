# lei-ihm_video_mapping
Our lei IHM to config mapping

## Material list

TODO

## 1) Installation

**Note** The speech recognition work only on Linux, Mac distribution. Because we use ``pvporcupine``

If you are on windows you can only use the video mapping application `py_video_mapping`

### General setup

For this project you will need a python3 version.

We code in python3.7 version.

You will need the following package:
    
    sudo apt install python3
    sudo apt install python3-dev python3-tk python-imaging-tk
    sudo apt install cmake
    sudo apt install python-pyaudio python3-pyaudio
    sudo apt install ffmpeg
 
Opencv optimisation lib
    
    sudo apt install libxmu-dev libxi-dev libglu1-mesa libglu1-mesa-dev
    sudo apt install libjpeg-dev libpng-dev libtiff-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev
    sudo apt install libopenblas-dev libatlas-base-dev liblapack-dev gfortran
    sudo apt install libhdf5-serial-dev libgtk-3-dev

Install pip and virtualenv:

    wget https://bootstrap.pypa.io/get-pip.py
    sudo python3 get-pip.py
    pip3 install virtualenv virtualenvwrapper

Prepare your virtualenv:

    python3 -m virtualenv venv
    . venv/bin/activate

If you want to exit your virtualenv:    

    deactivate

Then install requirements

    pip install --upgrade --force-reinstall -r requirements.txt

### Speech recognition setup

A speech to text to control an IoT object

On Ubuntu, you need to run:

    sudo apt update && sudo apt install portaudio19-dev swig libpulse-dev libasound2-dev

Install pvporcupine for hot word recognition

    pip install pvporcupine

#### Py audio

 You will need pyaudio. If you use a python version > 3.6 install with apt (pip not work for 3.7 python)

    sudo apt install python-pyaudio python3-pyaudio
    
    or this if fail
    
    sudo apt install portaudio19-dev
    sudo apt install python-all-dev python3-all-dev

#### Rasa

To install rasa just run

    pip install rasa


## 2) Creat a mapping

First you need to map your video projector with the flower pot. To do this you need to run this command

    python configure_video_mapping.py

When the mapping his done you can test by running the test script.

    python test_video_projection.py

## 3) Run rasa server

We do not use the full capacities of rasa but [only the NLU part](https://rasa.com/docs/rasa/nlu/using-nlu-only/)

To detect witch action do we use Rasa intent recognition. First you need to train the Rasa NLU model

    cd speech_to_text/plant_intent_recognizer && rasa train nlu

Then start the server

    rasa run --enable-api
    
To test if all work

    curl localhost:5005/model/parse -d '{"text":"hello"}'

## 4) run the garden (Only work on Linux and Mac)

Before to run the main script copy and rename the `config.ini.example` file to `config.ini`

**Note** and remember to replace all the parameters with the text `<To fill>`

The you can run the garden

    python main.py config.ini