import Event
import threading


class EventManager:
    rlock = threading.RLock()

    _instance = None

    def __init__(self):
        self.list = dict()
        for variable in Event.Event:
            self.list.update({variable: []})
        pass

    @staticmethod
    def get_instance():
        with EventManager.rlock:
            if EventManager._instance is None:
                EventManager._instance = EventManager()
        return EventManager._instance

    def add_event(self, type, function, args=None):
        if args is None:
            args = []
        with EventManager.rlock:
            self.list[type].append({'function': function, 'args': args})

    def trigger_event(self, type, args=None):
        with EventManager.rlock:
            l = self.list[type]
            for t in l:
                if args is None:
                    args = {}
                list = args
                list["user"] = t["args"]
                t["function"](list)
