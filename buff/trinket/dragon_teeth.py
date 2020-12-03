from buff import Buff


class DragonTeeth(Buff):

    def __init__(self):
        super().__init__('dragon_teeth', 0)

    def equip(self,engine, char_state):
        char_state.ap += 56

    def dequip(self,engine, char_state):
        char_state.ap -= 56
