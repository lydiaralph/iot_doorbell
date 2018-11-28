#!/usr/bin/env bash

sudo /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

brew install python3

sudo pip3 install pip --upgrade

## PI
sudo pip3 install gpiozero
sudo pip3 install picamera
sudo pip3 install colour

## AUDIO
# Trying to install portaudio!
#sudo apt-get install libasound-dev
#sudo apt-get install portaudio19-dev
#sudo apt-get install libportaudio2

brew install pyaudio
sudo pip3 install pyaudio

# Use instead of pyaudio
sudo pip3 install simpleaudio
sudo pip3 install SpeechRecognition==3.8.1
sudo pip3 install soundex==1.1.3

## TWITTER
sudo pip3 install twitter

# sudo pip3 install python-twitter --upgrade
# Until fix is merged...
sudo pip3 install git+git://github.com/bear/python-twitter.git@d33e051d7c5f92b8947ea029786c1632c9c9a478


## TESTING
sudo pip3 install -U pytest
sudo pip3 install unittest2
sudo pip3 install mock
