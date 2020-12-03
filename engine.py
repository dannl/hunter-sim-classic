from heapq import *


class Engine:

    def __init__(self):
        self.__queue = []
        self.__current_prio = 0

    def current_priority(self):
        return self.__current_prio

    def append(self, event):
        heappush(self.__queue, (event.priority, event))

    def get_queue(self):
        return self.__queue

    def clear(self):
        self.__queue.clear()

    def run(self):
        while self.__queue:
            _, event = heappop(self.__queue)
            self.set_current_priority(event)
            event.act()

    def set_current_priority(self, event):
        if event.priority < self.__current_prio:
            raise Exception(
                "loop error, engine at : {0} but event {1} at {2}".format(self.__current_prio,
                                                                          event, event.priority))
        self.__current_prio = event.priority

    def has_future_timeout(self, buff_name):
        item = None
        for e in self.__queue:
            if e[1].event_type == 'buff_time_out':
                if e[1].buff and e[1].buff.name == buff_name:
                    item = e
                    break
        return item is not None

    def timeout_all(self):
        for e in self.__queue:
            if e[1].event_type == 'buff_time_out':
                e[1].priority = self.current_priority()
                e[1].act_force()
