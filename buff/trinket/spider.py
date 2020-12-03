from buff import LastingBuff


class Spider(LastingBuff):

    def __init__(self):
        super().__init__('spider', 2 * 60, 15)

    def equip(self, engine, char_state):
        char_state.crit += 0.01

    def dequip(self, engine, char_state):
        char_state.crit -= 0.01

    def timeout(self, rotation, engine, char_state):
        char_state.remove_haste(1.2)

    def perform_impl(self, rotation, engine, char_state):
        char_state.apply_haste(1.2, engine.current_priority(),
                               engine.current_priority() + self.duration)
        rotation.rapid.next_available = max(engine.current_priority() + 20, rotation.rapid.next_available)

