from buff import Buff


class BlackHand(Buff):

    def __init__(self):
        super().__init__('black_hand', 0)

    def equip(self, engine, char_state):
        char_state.crit += 0.02

    def dequip(self, engine, char_state):
        char_state.crit -= 0.02
