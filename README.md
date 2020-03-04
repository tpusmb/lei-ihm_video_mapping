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
    sudo apt install python3-pip
    sudo apt install python3-tk
    sudo apt install cmake
 
Prepare your virtualenv:

    virtualenv -p python3 venv
    . venv/bin/activate
    pip install -r requirements.txt   

If you want to exit your virtualenv:

    deactivate

Then install requirements

    pip install -r requirements.txt

You need to setup the speech to text
    
    ## For linux
    pip install -r speech_to_text/linux-requirements.txt
    
    ## For windows
    pip install -r speech_to_text/win-requirements.txt


## Creat a mapping

First you need to map your video projector with the flower pot. To do this you need to run this command

    python app.py

When the mapping his done you can test by running the test script.

    python test_video_projection.py
