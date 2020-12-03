from event import Event
from event.user_action import UserAction


class CastDone(Event):

    def __init__(self, rotation, engine, char_state, spell, statistics, priority):
        super().__init__('cast_done', priority)
        self.rotation = rotation
        self.engine = engine
        self.char_state = char_state
        self.spell = spell
        self.statistics = statistics

    def act(self):
        dmg, is_crit = self.spell.cast_done(self.engine, self.char_state)
        self.statistics.add_dmg(self.spell.name, dmg, is_crit, self.priority)
        # self.statistics.add_end(self.spell.name, self.priority)
        self.engine.append(UserAction(self.rotation, self.engine.current_priority()))
        self.engine.append(UserAction(self.rotation, self.spell.next_available))
        self.rotation.set_casting(False)
        self.rotation.trigger(self.spell.name)
