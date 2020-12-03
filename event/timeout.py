from event import Event


class BuffTimeOut(Event):

    def __init__(self, buff, rotation, engine, char_state, priority):
        super().__init__('buff_time_out', priority)
        self.buff = buff
        self.rotation = rotation
        self.engine = engine
        self.char_state = char_state

    def act(self):
        if not self.engine.has_future_timeout(self.buff.name):
            # self.buff.timeout(self.engine, self.char_state)
            # self.buff.on_going = False
            # self.rotation.statistics.add_end(self.buff.name, self.priority)
            self.act_force()

    def act_force(self):
        self.buff.timeout(self.rotation, self.engine, self.char_state)
        self.buff.on_going = False
        self.rotation.statistics.add_end(self.buff.name, self.priority)
