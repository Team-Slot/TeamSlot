# Dummy class for database, to do
import sqlite3


class Database:
    def __init__(self):
        pass

    def getCal(self, userid):
        db = sqlite3.connect('teamslot.db')
        c = db.cursor()

        c.execute('''SELECT ical_url FROM users
                     WHERE id = ?''', (userid,))

        result = c.fetchone()[0]

        db.commit()
        db.close()

        return result

    def addUser(self, userid, calURL):
        db = sqlite3.connect('teamslot.db')
        c = db.cursor()

        c.execute('''INSERT OR REPLACE INTO users
                     VALUES(?, ?)''', (userid, calURL))

        db.commit()
        db.close()

    def updateUser(self, userid, newCalURL):
        db = sqlite3.connect('teamslot.db')
        c = db.cursor()

        c.execute('''INSERT OR REPLACE INTO users
                     VALUES(?, ?)''', (userid, newCalURL))

        db.commit()
        db.close()
