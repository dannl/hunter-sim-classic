import abc


class Ticker:

    @abc.abstractmethod
    def tick(self, engine, char_state):
        pass
