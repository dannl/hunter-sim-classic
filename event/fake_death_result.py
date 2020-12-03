from event import Event


class FakeDeathResult(Event):

    def __init__(self, rotation, priority, result=True):
        super().__init__('fake_death', priority)
        self.rotation = rotation
        self.result = result

    def act(self):
        if self.result:
            self.rotation.switch_next_trinket_group()
        self.rotation.statistics.add_dmg('fake_death', '成功' if self.result else '失败', False, self.priority)