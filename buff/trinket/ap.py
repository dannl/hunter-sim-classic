from buff import Buff


class Ap(Buff):

    def __init__(self):
        super().__init__('ap', 0)

    def equip(self,engine, char_state):
        char_state.ap += 48

    def dequip(self,engine, char_state):
        char_state.ap -= 48
