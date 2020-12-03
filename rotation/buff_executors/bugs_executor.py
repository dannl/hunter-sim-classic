from buff.trigger import Trigger
from buff.trinket.bugs import Bugs
from rotation.executors import Executor


class BugsExecutor(Executor):

    def __init__(self):
        super().__init__(Bugs())

    def attempt_cast_impl(self, rotation, engine, char_state):
        priority = engine.current_priority()
        if self.spell.next_available > priority:
            return False
        rotation.add_trigger('all', Trigger(self.spell, 0.8))
        return True