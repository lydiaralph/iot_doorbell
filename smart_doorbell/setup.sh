#!/usr/bin/env bash

sudo pip3 install pip --upgrade
sudo pip3 install gpiozero
sudo pip3 install picamera
sudo pip3 install colour
sudo pip3 install -U pytest

# Trying to install portaudio!
#sudo apt-get install libasound-dev
#sudo apt-get install portaudio19-dev
#sudo apt-get install libportaudio2
#sudo pip3 install pyaudio

# Use instead of pyaudio
sudo pip3 install simpleaudio

sudo pip3 install SpeechRecognition==3.8.1
sudo pip3 install soundex==1.1.3

sudo pip3 install twitter

# Until fix is merged...
# sudo pip3 install python-twitter --upgrade
sudo pip3 install https://github.com/bear/python-twitter/archive/v3.5.tar.gz


pip3 install mock