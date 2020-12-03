from buff import Buff


class Dawn(Buff):

    def __init__(self):
        super().__init__('dawn', 0)

    def equip(self,engine, char_state):
        char_state.ap += 81

    def dequip(self,engine, char_state):
        char_state.ap -= 81
