from buff import Buff, LastingBuff


class DragonKiller(LastingBuff):

    def __init__(self):
        super().__init__('dragon_killer', 2 * 60, 20)

    def equip(self,engine, char_state):
        char_state.ap += 64

    def dequip(self,engine, char_state):
        char_state.ap -= 64

    def perform_impl(self,rotation, engine, char_state):
        char_state.ap += 260

    def timeout(self, rotation, engine, char_state):
        char_state.ap -= 260


