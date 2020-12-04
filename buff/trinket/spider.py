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
        # rotation.rapid.next_available = max(engine.current_priority() + 20, rotation.rapid.next_available)

    def trigger(self, rotation, engine, char_state):
        if self.next_available > engine.current_priority():
            return False
        if rotation.is_casting():
            return False
        trinkets = rotation.current_trinket
        if 'bugs' in trinkets:
            bugs = rotation.get_trinket('bugs')
            if not (0 < bugs.next_available - engine.current_priority() < 3*60 - 13):
                return False
        if 'zug' in trinkets:
            zug = rotation.get_trinket('zug')
            if not (0 < zug.next_available - engine.current_priority() < 3 * 60 - 0.43):
                return False
        if 'sand_bug' in trinkets:
            sand_bugs = rotation.get_trinket('sand_bug')
            if not (0 < sand_bugs.next_available - engine.current_priority() < 2 * 60 - 4):
                return False
        rotation.statistics.add_start(self.name, engine.current_priority())
        self.perform(rotation,engine, char_state)
        return True
