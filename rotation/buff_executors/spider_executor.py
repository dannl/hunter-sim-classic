from buff.buff.rapid import Rapid
from rotation.executors import Executor


class SpiderExecutor(Executor):

    def __init__(self, spell):
        super().__init__(spell)

    def attempt_cast_impl(self, rotation, engine, char_state):
        if self.spell.next_available > engine.current_priority():
            return False
        trinkets = rotation.current_trinket
        if 'bugs' in trinkets:
            bugs = rotation.get_trinket('bugs')
            return 0 < bugs.next_available - engine.current_priority() < 3*60 - 13
        if 'zug' in trinkets:
            zug = rotation.get_trinket('zug')
            return 0 < zug.next_available - engine.current_priority() < 3 * 60 - 0.43 - 2
        if 'sand_bug' in trinkets:
            sand_bugs = rotation.get_trinket('sand_bug')
            return 0 < sand_bugs.next_available - engine.current_priority() < 3 * 60 - 3
        return True
