import os

class SubscribersHandler:
    def __init__(self, subsfile):
        self.subsfile = subsfile
        self.subs = list()

        if not os.path.exists(subsfile):
            open(subsfile, 'x')

        with open(subsfile) as subs:
            lines = subs.readlines()
            for line in lines:
                self.subs.append(int(line))

    def add_subscriber(self, sub):
        if sub in self.subs:
            return
        self.subs.append(sub)
        self.__dump_list()

    def remove_subscriber(self, sub):
        if sub not in self.subs:
            return
        self.subs.remove(sub)
        self.__dump_list()

    def get_list(self):
        return self.subs

    def is_subscriber(self, id):
        return id in self.subs

    def __dump_list(self):
        with open(self.subsfile, 'w') as subsfile:
            for sub in self.subs:
                subsfile.write(f"{sub}\n")
