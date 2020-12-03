from buff.trinket.earth import Earth
from rotation.executors import Executor


class EarthExecutor(Executor):

    def __init__(self, spell):
        super().__init__(spell)

    def attempt_cast_impl(self, rotation, engine, char_state):
        priority = engine.current_priority()
        if self.spell.next_available > priority:
            return False
        trinkets = rotation.current_trinket
        if 'bugs' in trinkets:
            bugs = rotation.get_trinket('bugs')
            return 0 < bugs.next_available - engine.current_priority() <= 3*60 - 10
        return True