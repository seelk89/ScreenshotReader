import threading


class WatchableVariable:
    def __init__(self):
        self.value = None
        self.lock = threading.Lock()

    def set_value(self, value):
        with self.lock:
            self.value = value

    def has_changed(self):
        with self.lock:
            return self.value is not None
