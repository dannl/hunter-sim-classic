from event import Event


class Tick(Event):

    def __init__(self, ticker, engine, char_state, priority):
        super().__init__('tick', priority)
        self.ticker = ticker
        self.engine = engine
        self.char_state = char_state

    def act(self):
        self.ticker.tick(self.engine, self.char_state)
