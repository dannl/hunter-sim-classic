from rotation.executors import Executor


class LastingBuffExecutor(Executor):

    def __init__(self, spell):
        super().__init__(spell)

    def attempt_cast_impl(self, rotation, engine, char_state):
        return False