from rotation.executors import Executor


class AutoExecutor(Executor):

    def __init__(self, auto):
        super().__init__(auto)

    def attempt_cast_impl(self, rotation, engine, char_state):
        if rotation.is_casting():
            return False
        if self.spell.trigger_gcd and rotation.in_gcd:
            return False
        current_priority = engine.current_priority()
        if self.spell.next_available <= current_priority:
            return True
