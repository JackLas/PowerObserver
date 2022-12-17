from abc import abstractmethod
import sqlite3

class Storage:
    @abstractmethod
    def dump_time(self):
        pass

    @abstractmethod
    def add_subscriber(self):
        pass

    @abstractmethod
    def remove_subscriber(self):
        pass

    @abstractmethod
    def get_subscribers(self):
        pass

    @abstractmethod
    def is_subscriber(self):
        pass

class Database(Storage):
    def __init__(self, filename):
        self.db = filename
        self.execute_against_database("CREATE TABLE IF NOT EXISTS subscribers (id string)")
        self.execute_against_database("CREATE TABLE IF NOT EXISTS timestamp (value integer)")

    def execute_against_database(self, sql, params = tuple()):
        connection = sqlite3.connect(self.db)
        cursor = connection.cursor()
        res = cursor.execute(sql, params).fetchall()
        connection.commit()
        connection.close()
        return res

    def add_time_dump(self, time):
        if len(self.execute_against_database("SELECT * FROM timestamp")) == 0:
            self.execute_against_database("INSERT INTO timestamp VALUES(?)", (time,))
            return
        self.execute_against_database("UPDATE timestamp SET value=?", (time,))

    def get_time_dump(self):
        values = self.execute_against_database("SELECT * FROM timestamp")
        return 0 if len(values) == 0 else values[0][0]

    def add_subscriber(self, id):
        if not self.is_subscriber(id):
            self.execute_against_database("INSERT INTO subscribers VALUES(?)", (id,))
        return self.is_subscriber(id)

    def remove_subscriber(self, id):
        self.execute_against_database("DELETE FROM subscribers WHERE id=?", (id,))
        return not self.is_subscriber(id)

    def get_subscribers(self):
        raw = self.execute_against_database("SELECT * FROM subscribers")
        return list(map(lambda item: item[0], raw))

    def is_subscriber(self, id):
        return len(self.execute_against_database("SELECT * FROM subscribers WHERE id = ?", (id,))) > 0