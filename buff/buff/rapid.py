from buff import LastingBuff


class Rapid(LastingBuff):

    def __init__(self):
        super().__init__('rapid', 5 * 60, 15)

    def timeout(self,rotation, engine, char_state):
        char_state.remove_haste(1.4)

    def perform_impl(self, rotation, engine, char_state):
        char_state.apply_haste(1.4, engine.current_priority(),
                               engine.current_priority() + self.duration)

    def trigger(self, rotation, engine, char_state):
        if self.next_available > engine.current_priority():
            return False
        if rotation.is_casting():
            return False
        trinkets = rotation.current_trinket
        if 'bugs' in trinkets:
            bugs = rotation.get_trinket('bugs')
            if not (0 < bugs.next_available - engine.current_priority() < 3*60 - 14):
                return False
        if 'zug' in trinkets:
            zug = rotation.get_trinket('zug')
            if not (0 < zug.next_available - engine.current_priority() < 3 * 60 - 0.43):
                return False
        if 'sand_bug' in trinkets:
            sand_bugs = rotation.get_trinket('sand_bug')
            if not (0 < sand_bugs.next_available - engine.current_priority() < 2 * 60 - 4):
                return False
        triggers = rotation.after_dmg_triggers.get('auto')
        fake_death = None
        for t in triggers:
            if t.buff.name == 'fake_death':
                fake_death = t
        if fake_death and fake_death.trigger_count == 0 and len(rotation.trinket_groups) > 0:
            return False
        if 'spider' in trinkets:
            spider = rotation.get_trinket('spider')
            spider.next_available = engine.current_priority() + 20
        rotation.statistics.add_start(self.name, engine.current_priority())
        self.perform(rotation,engine, char_state)
        return True
