import utils
import os
from threading import Timer

class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

class Timing:
    def __init__(self, dump_delay, dump_file):
        self.start_time = utils.time_now()
        self.dump_delay = dump_delay
        self.dump_file = dump_file
        self.last_uptime = self.start_time

        if not os.path.exists(dump_file):
            print(f"Create file: {dump_file}")
            file = open(dump_file, 'x')
            file.close()
            self.__dump_time()
        else:
            try:
                with open(self.dump_file, "r") as dump:
                    line = dump.readline()
                    if line:
                        self.last_uptime = int(line)
            except: # in case if file is corrupted
                print(f"[WARN] {dump_file} is corrputed") 
                if os.path.exists(dump_file):
                    os.remove(dump_file)
                file = open(dump_file, 'x')
                file.close()
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
        with open(self.dump_file, "w") as dump:
            dump.write(str(utils.time_now()))
            os.sync()