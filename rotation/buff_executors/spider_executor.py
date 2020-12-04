from buff.buff.rapid import Rapid
from config import SPIDER_RAPID
from rotation.executors import Executor


class SpiderExecutor(Executor):

    def __init__(self, spell):
        super().__init__(spell)

    def attempt_cast_impl(self, rotation, engine, char_state):
        if self.spell.next_available > engine.current_priority():
            return False
        another = rotation.another_trinket(self.spell.name)
        if 'bugs' == another:
            bugs = rotation.get_trinket('bugs')
            if not (0 < bugs.next_available - engine.current_priority() < 3*60 - 13):
                return False
        if 'zug' == another:
            zug = rotation.get_trinket('zug')
            return 0 < zug.next_available - engine.current_priority() < 3 * 60 - 0.43 - 2
        # if another in ['earth','dragon_killer']:
        #     # 让位给rapid.
        #     if rotation.rapid.next_available <= engine.current_priority() and not SPIDER_RAPID:
        #         return False
        return True
