from buff import Buff


class Zug(Buff):

    def __init__(self):
        super().__init__('zug', 3 * 60)

    def perform(self, rotation, engine, char_state):
        rotation.multi.next_available = engine.current_priority()
        rotation.aim.next_available = engine.current_priority() + 0.01
        self.next_available = engine.current_priority() + self.cd
        rotation.statistics.add_end(self.name, engine.current_priority())