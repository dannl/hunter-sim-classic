import abc

from config import CRIT_DMG_PERCENT

class Spell:

    def __init__(self, name, cd):
        self.name = name
        self.cd = cd
        self.next_available = 0


class BuffSpell(Spell):

    def __init__(self, name, cd):
        super().__init__(name, cd)


class EquipSpell(BuffSpell):

    def __init__(self, name, cd):
        super().__init__(name, cd)


class DmgSpell(Spell):

    def __init__(self, name, cd, trigger_gcd=True):
        super().__init__(name, cd)
        self.trigger_gcd = trigger_gcd

    def cast_done(self, engine, char_state):
        self.next_available = self.calculate_next_available(engine.current_priority(), char_state)
        result, is_crit = self.perform(char_state)
        armor = char_state.target_armor
        percent = 1 - (armor / (armor + 400 + 60 * 85))
        return result * percent, is_crit

    @abc.abstractmethod
    def perform(self, char_state):
        pass

    @abc.abstractmethod
    def expected_perform(self, char_state):
        pass

    def expected_dmg(self, char_state):
        crit = char_state.crit
        armor = char_state.target_armor
        percent = 1 - (armor / (armor + 400 + 60 * 85))
        dmg = self.expected_perform(char_state)
        dmg = dmg * percent
        dmg = (1 - crit) * dmg + crit * dmg * CRIT_DMG_PERCENT
        return dmg

    def calculate_finish_time(self, char_state, current_priority):
        return current_priority

    def calculate_next_available(self, priority, char_state):
        return priority + self.cd
