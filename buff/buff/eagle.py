from buff import LastingBuff


class Eagle(LastingBuff):

    def __init__(self):
        super().__init__('eagle',0, 12)

    def timeout(self,rotation, engine, char_state):
        char_state.remove_haste(1.3)

    def perform_impl(self,rotation, engine, char_state):
        char_state.apply_haste(1.3, engine.current_priority(), engine.current_priority() + self.duration)
