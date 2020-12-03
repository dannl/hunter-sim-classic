from buff import LastingBuff


class Weakness(LastingBuff):

    def __init__(self):
        super().__init__('weakness', 0, 7)
        self.has_effect = False

    def timeout(self,rotation, engine, char_state):
        char_state.ap -= 460

    def perform_impl(self,rotation, engine, char_state):
        if self.has_effect:
            char_state.ap -= 460
        self.has_effect = True
        char_state.ap += 460
