#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
import time
from RPi import GPIO
import tweepy
import os
import picamera
import sys
import json
from PIL import Image

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}

def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()

def subscribe_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)

def action_wrapper(hermes, intentMessage, conf):
    current_session_id = intentMessage.session_id
    say(hermes,'OK. Allons-y. Dans 3 secondes.')
    time.sleep(1)
    say(hermes,'2.')
    time.sleep(1)
    say(hermes,'1. On ne bouge plus !')
    name = 'test'
    camera = picamera.PiCamera()
    camera.resolution = (1024, 768)
    camera.shutter_speed = 6000000
    camera.iso = 800
    camera.vflip = False
    time.sleep(1)
    camera.exposure_mode = 'night'
    camera.capture('/home/pi/cam/captions/' + name + '.jpg')
    time.sleep(0.5)
    say(hermes,'Merci. Je vais à présent développer la photo.')
    time.sleep(1)
    background = Image.open('/home/pi/cam/captions/' + name + '.jpg')
    foreground = Image.open('/home/pi/cam/imgs/watermark.png')
    background.paste(foreground, (0, 0), foreground)
    background.save('/home/pi/cam/captions/' + name + '.jpg', 'JPEG', subsampling=0, quality=100)
    time.sleep(0.5)
    say(hermes,'Et je vais à présent la publier sur notre compte twitter.')
    consumer_key = ''
    consumer_secret = ''
    access_token = ''
    access_token_secret = ''
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    imagePath = '/home/pi/cam/captions/' + name + '.jpg'
    status = 'Ceci est un test'
    api.update_with_media(imagePath, status)
    time.sleep(1)
    result_sentence = "On est bons. Merci beaucoup et à très vite !"
    hermes.publish_end_session(current_session_id, result_sentence)

def say(hermes, text):
    hermes.publish('hermes/tts/say', json.dumps({'text': text}))

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(14, GPIO.OUT)
    GPIO.output(14, GPIO.LOW)
    with Hermes("localhost:1883") as h:
        h.subscribe_intent("jumahe:take_picture", subscribe_intent_callback).start()
