from abc import abstractmethod


class Event:

    def __init__(self, event_type, priority):
        self.event_type = event_type
        self.priority = priority


    @abstractmethod
    def act(self):
        pass

    def __gt__(self, other):
        return self.priority > other.priority

    def __lt__(self, other):
        return self.priority < other.priority

    def __ge__(self, other):
        return not self.__lt__(other)

    def __le__(self, other):
        return not self.__gt__(other)

    def __eq__(self, other):
        return self.priority == other.priority