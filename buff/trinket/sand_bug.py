from buff.ticker import Ticker
from event.tick import Tick
from buff import LastingBuff


class SandBug(LastingBuff, Ticker):

    def __init__(self):
        super().__init__('sand_bug', 2 * 60,  20)
        self.ap = 0

    def perform_impl(self,rotation, engine, char_state):
        char_state.ap += 65
        self.ap = 65
        current_priority = engine.current_priority()
        engine.append(Tick(self, engine, char_state, current_priority + 2))

    def timeout(self,rotation, engine, char_state):
        char_state.ap -= self.ap

    def tick(self, engine, char_state):
        current_priority = engine.current_priority()
        char_state.ap += 65
        self.ap += 65
        if current_priority + 2 < self.start + self.duration:
            engine.append(Tick(self, engine, char_state, current_priority + 2))
