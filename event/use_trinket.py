from event import Event


class UseTrinket(Event):

    def act(self):
        self.trinket.perform()

    def __init__(self, trinket, priority):
        super().__init__('use_trinket', priority)
        self.trinket = trinket


