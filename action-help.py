#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io

def subscribe_intent_callback(hermes, intentMessage):
    action_wrapper(hermes, intentMessage)

def action_wrapper(hermes, intentMessage):
    result_sentence = "C'est très simple. Vous vous placez sous l'appareil qui est suspendu, vous regardez l'appareil, puis vous dites... Hey Snips, prends la photo."
    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, result_sentence)

if __name__ == "__main__":
    with Hermes("localhost:1883") as h:
        h.subscribe_intent("jumahe:help", subscribe_intent_callback).start()
