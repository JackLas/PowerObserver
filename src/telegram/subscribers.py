class SubscribersHandler:
    def __init__(self, db):
        self.db = db
        self.subs = list()

    def add_subscriber(self, sub):
        return self.db.add_subscriber(sub)

    def remove_subscriber(self, sub):
        return self.db.remove_subscriber(sub)

    def get_list(self):
        return self.db.get_subscribers()

    def is_subscriber(self, id):
        return self.db.is_subscriber(id)
