from rotation.executors import Executor
from rotation.rotation import Rotation


class CastExecutor(Executor):

    def __init__(self, spell):
        """
        :param Rotation rotation:
        :param spell:
        """
        super().__init__(spell)

    def attempt_cast_impl(self, rotation, engine, char_state):
        if rotation.is_casting():
            return False
        if self.spell.trigger_gcd and rotation.in_gcd:
            return False
        current_priority = engine.current_priority()
        if self.spell.next_available <= current_priority:
            return True
