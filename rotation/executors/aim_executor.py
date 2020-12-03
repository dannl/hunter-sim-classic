from rotation.executors import Executor


class AimExecutor(Executor):

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
            auto = rotation.auto
            auto_available = auto.next_available
            auto_dmg = auto.expected_dmg(char_state)
            auto_cast_time = auto.calculate_finish_time(char_state, auto_available) - auto_available
            auto_cd = auto.calculate_next_available(auto_available, char_state) - auto_available

            aim_dmg = self.spell.expected_dmg(char_state)
            aim_available = self.spell.next_available
            aim_finish = self.spell.calculate_finish_time(char_state, aim_available)
            aim_cd = self.spell.cd

            delta = aim_finish - auto_available
            lose_auto = auto_dmg * (delta / (auto_cast_time + auto_cd))

            lose_aim = (auto_available - self.spell.next_available + auto_cast_time) / (aim_finish - current_priority + aim_cd) * aim_dmg

            return lose_aim > lose_auto

