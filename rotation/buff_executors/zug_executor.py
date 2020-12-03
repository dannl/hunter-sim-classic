from buff.trinket.zug import Zug
from rotation.executors import Executor


class ZugExecutor(Executor):

    def __init__(self):
        super().__init__(Zug())

    def attempt_cast_impl(self, rotation, engine, char_state):
        priority = engine.current_priority()
        if self.spell.next_available > priority:
            return False
        if rotation.in_gcd:
            return False
        if priority + 4 < rotation.aim.next_available and priority + 8.4 < rotation.multi.next_available: # 考虑到gcd的影响， 在gcd结束的时候再触发
            return True
        return False