from buff import LastingBuff


class Bugs(LastingBuff):

    def __init__(self):
        super().__init__('bugs', 3 * 60, 30)
        self.minus_armor = 0

    def perform_impl(self,rotation, engine, char_state):
        # current = char_state.target_armor
        # if current > 0 and self.minus_armor < 1200:
        #     self.minus_armor += min(current, 200)
        #     char_state.target_armor -= min(current, 200)
        pass

    def timeout(self, rotation, engine, char_state):
        char_state.target_armor += self.minus_armor
        rotation.remove_trigger('all', self.name)

    def trigger(self, rotation, engine, char_state):
        current = char_state.target_armor
        if current > 0 and self.minus_armor < 1200:
            self.minus_armor += min(current, 200)
            char_state.target_armor -= min(current, 200)
        return True

