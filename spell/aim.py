from config import *
from spell import DmgSpell
import random


class Aim(DmgSpell):

    def __init__(self):
        super().__init__('aim', 6)

    def perform(self, char_state):
        if USE_EXPECTED_DMG:
            return self.expected_perform(char_state), False
        rap = char_state.ap
        crit = char_state.crit
        is_crit = random.random() < crit
        w_dmg = char_state.weapon.rand_dmg()
        w_speed = char_state.weapon.speed
        result = (w_dmg + rap / 14 * 2.8 + 600) * 1.05 + ARROW_DMG * w_speed
        if is_crit:
            return result * CRIT_DMG_PERCENT, is_crit
        else:
            return result, is_crit

    def expected_perform(self, char_state):
        rap = char_state.ap
        w_dmg = char_state.weapon.avr_dmg()
        w_speed = char_state.weapon.speed
        result = (w_dmg + rap / 14 * 2.8 + 600) * 1.05 + ARROW_DMG * w_speed
        return result

    def calculate_finish_time(self, char_state, current_priority):
        haste = char_state.haste_at(current_priority)
        duration = 3.5 / haste
        return current_priority + duration
