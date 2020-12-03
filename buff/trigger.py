
import random

class Trigger:

    def __init__(self, buff, percent):
        self.buff = buff
        self.percent = percent

    def trigger(self, rotation, engine, char_state):
        if random.random() < self.percent:
            return self.buff.trigger(rotation, engine, char_state)
