import sqlite3

class db_controller:

    def __init__(self, database_file):
        """"Connecting to Data Base and saving connection"""
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()


    def get_subs(self, status = True):
        """Getting all active subs"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM 'subs' WHERE 'status' = (?)", (status,)).fetchall()


    def sub_exists(self, user_id):
        """DataBase check for user.id"""
        with self.connection:
            result = self.cursor.execute("SELECT * FROM subs WHERE user_id = (?)", (user_id,)).fetchall()
            return bool(len(result))

    def add_sub(self, user_id, status = True):
        """Add new sub"""
        with self.connection:
            return self.cursor.execute("INSERT INTO 'subs' ('user_id', 'status') VALUES (?,?)", (user_id, status))


    def update_sub(self, user_id, status = True):
        """Updating sub status"""
        with self.connection:
            return self.cursor.execute("UPDATE 'subs' SET 'status' = (?) WHERE 'user_id' = (?)", (status, user_id))


    def close(self):
        """Closing DB connection"""
        self.connection.close()



