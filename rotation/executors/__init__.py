import abc

from spell import Spell


class Executor:

    def __init__(self, spell):
        self.spell = spell
        self.enabled = True

    def attempt_cast(self, rotation, engine, char_state):
        if not self.enabled:
            return None, None
        if self.attempt_cast_impl(rotation, engine, char_state):
            if isinstance(self.spell, Spell):
                return self.spell, None
            else:
                return None, self.spell
        else:
            return None, None

    @abc.abstractmethod
    def attempt_cast_impl(self, rotation, engine, char_state):
        pass