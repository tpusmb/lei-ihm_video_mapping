# lei-ihm_video_mapping
Our lei IHM to config mapping

## Material list

TODO

## Installation

### General setup

For this project you will need a python3 version.

You will need the following package:
    
    sudo apt install python3
    sudo apt install virtualenv
    sudo apt install python3-dev python3-tk python-imaging-tk
    sudo apt install cmake
    sudo apt install python-pyaudio python3-pyaudio
 
Opencv optimisation lib
    
    sudo apt install libxmu-dev libxi-dev libglu1-mesa libglu1-mesa-dev
    sudo apt install libjpeg-dev libpng-dev libtiff-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev
    sudo apt install libopenblas-dev libatlas-base-dev liblapack-dev gfortran
    sudo apt install libhdf5-serial-dev libgtk-3-dev
 
Prepare your virtualenv:

    virtualenv -p python3 venv
    . venv/bin/activate
    pip install -r requirements.txt   

If you want to exit your virtualenv:    

    deactivate

Then install requirements

    pip install -r requirements.txt

### Speech recognition setup

A speech to text to control an IoT object

On Ubuntu, you need to run:

    sudo apt update && sudo apt install portaudio19-dev swig libpulse-dev libasound2-dev

Install pvporcupine for hot word recognition

    pip install pvporcupine

#### Py audio Linux

 You will need pyaudio. If you use a python version > 3.6 install with apt (pip not work for 3.7 python)

    sudo apt install python-pyaudio python3-pyaudio
    
    or this if fail
    
    sudo apt install portaudio19-dev
    sudo apt install python-all-dev python3-all-dev

#### Py audio Windows

To install Pyaudio you can use this [web site](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio).

Then do

    pip install <path to .whl>

#### Rasa

To install rasa just run

    pip install rasa


## Creat a mapping

First you need to map your video projector with the flower pot. To do this you need to run this command

    python configure_video_mapping.py

When the mapping his done you can test by running the test script.

    python test_video_projection.py
