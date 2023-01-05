import threading


class BatchJob(threading.Thread):
    def __init__(self, method, interval: float, method_args: list = [], daemon: bool = True, *args, **kwargs):
        self.method = method
        self.method_args = method_args
        self.event = threading.Event()
        self.interval = interval
        super(BatchJob, self).__init__(target=method, daemon=daemon, *args, **kwargs)

    def run(self):
        while not self.event.wait(self.interval):
            self.method(*self.method_args)
