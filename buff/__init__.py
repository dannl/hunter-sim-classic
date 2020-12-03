import abc
from event.timeout import BuffTimeOut


class Buff:

    def __init__(self, name, cd):
        self.name = name
        self.next_available = 0
        self.cd = cd
        self.on_going = False

    def equip(self, engine, char_state):
        current = engine.current_priority()
        if self.next_available - current < 30 and current > 0:
            self.next_available = current + 30

    def perform(self, rotation, engine, char_state):
        pass

    def dequip(self, engine,char_state):
        pass

    def trigger_other_delay(self, rotation, engine):
        # 看起来只有ap会相互影响..急速的已经处理了
        current_trinkets = rotation.current_trinket
        other = None
        for t in current_trinkets:
            if t != self.name:
                other = t
                break
        if self.name == 'zug':
            delay = 10
        elif self.name in ['earth','dragon_killer','sand_bug']:
            delay = 20
        else:
            delay = 0
        if delay > 0 and other and other in ['zug','earth','dragon_killer','sand_bug']:
            trinket = rotation.get_trinket(other)
            trinket.next_available = max(trinket.next_available, engine.current_priority() + delay)



class LastingBuff(Buff):

    def __init__(self, name, cd, duration):
        super().__init__(name, cd)
        self.duration = duration
        self.start = 0
        self.on_going = False

    def perform(self, rotation, engine, char_state):
        current = engine.current_priority()
        self.perform_impl(rotation, engine, char_state)
        self.on_going = True
        self.start = current
        if self.duration > 0:
            engine.append(BuffTimeOut(self, rotation, engine, char_state, current + self.duration))
        self.next_available = current + self.cd
        self.trigger_other_delay(rotation, engine)

    def trigger(self, rotation, engine, char_state):
        self.perform(rotation, engine, char_state)
        return True

    @abc.abstractmethod
    def perform_impl(self, rotation, engine, char_state):
        pass

    @abc.abstractmethod
    def timeout(self, rotation, engine, char_state):
        pass


