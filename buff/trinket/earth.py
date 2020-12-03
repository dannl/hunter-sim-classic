from buff import LastingBuff


class Earth(LastingBuff):

    def __init__(self):
        super().__init__('earth', 2*60, 20)

    def perform_impl(self,rotation, engine, char_state):
        char_state.ap += 280

    def timeout(self, rotation, engine, char_state):
        char_state.ap -= 280
