from event import Event


class End(Event):

    def __init__(self, engine,priority):
        super().__init__('end', priority)
        self.engine = engine

    def act(self):
        self.engine.timeout_all()
        self.engine.clear()

