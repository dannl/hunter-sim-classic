import random

import config


class Weapon:

    def __init__(self, min_d, max_d, speed):
        self.min_d = min_d
        self.max_d = max_d
        self.speed = speed

    def rand_dmg(self):
        if config.USE_AVERAGE:
            return self.avr_dmg()
        return random.randint(self.min_d, self.max_d)

    def avr_dmg(self):
        return (self.min_d + self.max_d) / 2


CJ = Weapon(124, 186, 3.4)
KL = Weapon(128, 238, 3.2)
SS = Weapon(89, 223, 2.7)
