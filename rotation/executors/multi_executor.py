from rotation.executors import Executor


class MultiExecutor(Executor):

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
            # 到cd了,,
            aim = rotation.aim
            aim_available = aim.next_available
            aim_dmg = aim.expected_dmg(char_state)
            aim_time = aim.calculate_finish_time(char_state, aim_available) - aim_available
            aim_cd = aim.calculate_next_available(aim_available, char_state) - aim_available

            auto = rotation.auto
            auto_available = auto.next_available
            auto_dmg = auto.expected_dmg(char_state)
            auto_time = auto.calculate_finish_time(char_state, auto_available) - auto_available
            auto_cd = auto.calculate_next_available(auto_available, char_state) - auto_available

            aim_delta_by_auto = auto_available + auto_time - aim_available

            multi_dmg = self.spell.expected_dmg(char_state)
            multi_finish_by_gcd = 1.5 + current_priority
            multi_finish = self.spell.calculate_finish_time(char_state, current_priority)

            multi_cd = self.spell.cd

            delta = multi_finish_by_gcd - aim_available - aim_delta_by_auto

            lose_aim = aim_dmg * (delta / (aim_time + aim_cd))
            lose_auto_by_aim = auto_dmg * ((delta - auto_time) / (auto_time + auto_cd))
            lose_auto_by_multi = auto_dmg * (multi_finish - auto_available) / (auto_time + auto_cd)

            lose_multi = (aim_available - self.spell.next_available + aim_time) / (multi_finish_by_gcd - current_priority + multi_cd) * multi_dmg
            # print('lose multi: ', lose_multi, 'lose aim:',lose_aim, 'delta:', delta, 'lose auto by aim: ',
            #       lose_auto_by_aim, "aim delta by auto:", aim_delta_by_auto,
            #       'lose_auto_by_multi:', lose_auto_by_multi)
            return lose_multi > lose_aim + lose_auto_by_aim