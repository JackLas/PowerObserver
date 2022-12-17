import utils
import os
from threading import Timer

class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

class Timing:
    def __init__(self, db, dump_delay):
        self.start_time = utils.time_now()
        self.dump_delay = dump_delay
        self.db = db
        self.last_uptime = self.db.get_time_dump(self.start_time)
        self.__dump_time()

        self.repeater = RepeatTimer(self.dump_delay, self.__dump_time)
        self.repeater.start()

    def __del__(self):
        self.repeater.cancel()

    def get_start_time(self):
        return self.start_time

    def get_stop_time(self):
        return self.last_uptime

    def get_uptime(self):
        return utils.time_now() - self.start_time

    def get_downtime(self):
        return self.start_time - self.last_uptime

    def __dump_time(self):
        self.db.set_time_dump(utils.time_now())