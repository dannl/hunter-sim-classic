from buff import Buff


class Warrior(Buff):

    def __init__(self):
        super().__init__('warrior', 0)

    def equip(self,engine, char_state):
        char_state.ap += 150

    def dequip(self,engine, char_state):
        char_state.ap -= 150
