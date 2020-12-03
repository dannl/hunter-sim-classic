from event import Event


class UserAction(Event):

    def act(self):
        self.rotation.perform()

    def __init__(self, rotation, priority):
        super().__init__('user_action', priority)
        self.rotation = rotation



