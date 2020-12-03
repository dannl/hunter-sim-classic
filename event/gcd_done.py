from event import Event


class GCDDone(Event):

    def __init__(self, rotation, priority):
        super().__init__('gcd_done', priority)
        self.rotation = rotation

    def act(self):
        self.rotation.in_gcd = False
        self.rotation.perform()

