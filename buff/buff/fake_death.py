import config
from buff import Buff
import random

from event.fake_death_result import FakeDeathResult
from event.user_action import UserAction


class FakeDeath(Buff):

    def __init__(self):
        super().__init__('fake_death', 30)

    def perform(self, rotation, engine, char_state):
        rotation.auto.next_available = config.FAKE_DEATH_DURATION + rotation.auto.calculate_next_available(engine.current_priority() + config.FAKE_DEATH_DURATION, char_state)
        rotation.aim.next_available = max(config.FAKE_DEATH_DURATION + engine.current_priority(),
                                          rotation.aim.next_available)
        rotation.multi.next_available = max(config.FAKE_DEATH_DURATION + engine.current_priority(),
                                            rotation.multi.next_available)
        if random.random() > 0.17 + config.FAKE_DEATH_EXT_PERCENT:
            engine.append(FakeDeathResult(rotation, engine.current_priority() + config.FAKE_DEATH_DURATION))
        else:
            engine.append(FakeDeathResult(rotation, engine.current_priority() + config.FAKE_DEATH_DURATION, False))
        engine.append(UserAction(rotation, engine.current_priority() + config.FAKE_DEATH_DURATION))
        engine.append(UserAction(rotation, rotation.auto.next_available))
        engine.append(UserAction(rotation, rotation.multi.next_available))
        self.next_available = engine.current_priority() + self.cd

class FakeDeathTrigger:

    def __init__(self):
        self.buff = FakeDeath()
        self.trigger_count = 0

    def trigger(self, rotation, engine, char_state):
        if self.buff.next_available > engine.current_priority():
            return False
        # if self.trigger_count > 0:
        #     return False
        if len(rotation.trinket_groups) <= 0:
            return False
        current_trinket = rotation.current_trinket
        for trinket in current_trinket:
            trinket = rotation.get_trinket(trinket)
            if trinket and ((trinket.next_available <= engine.current_priority() and trinket.cd > 0) or trinket.on_going):
                return False
        before_triggers = rotation.before_dmg_triggers
        for v in before_triggers.values():
            for i in v:
                if i.buff.on_going:
                    return False
        after_triggers = rotation.after_dmg_triggers
        for v in after_triggers.values():
            for i in v:
                if i.buff.on_going:
                    return False
        if rotation.aim.next_available - engine.current_priority() < 0.1:
            self.buff.perform(rotation,engine,char_state)
            self.trigger_count = 1
            return True
