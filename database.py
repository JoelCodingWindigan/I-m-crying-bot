import sqlite3

'''
for reference:
try:
    with Database(filename.sqlite) as db:
        db.execute("SELECT ...", (karni_id,))
        db.commit()
except sqlite3.Error as error:
    pass
'''

class Database:

    def __init__(self, dbfile: str):
        self._conn = sqlite3.connect(dbfile)
        self._cursor = self._conn.cursor()
        self._create_table()
    
    def _create_table(self):
        #to create user_counts table
        self.execute('''CREATE TABLE IF NOT EXISTS Crying (user_id TEXT PRIMARY, KEY, count INTEGER DEFAULT 0)''')


    #user as foreign key
    #don't remember the syntax is it where FOREIGN = PRIMARY OR WHERE PRIMARY = FOREIGN in this case, clarify with Justin
    #actually realistically not sure if we need to call this function, database is serving only as backup. We can call from hashmap directly
    def print_count(self, user):
        self.execute('SELECT count FROM Crying WHERE user = ?', (user_id,))
        result = self.fetchone()
        #fetchone will return a tuple our tuple will contain only one element, count, we can access by indexing with [0]
        if result is not None:
            return result[0]
        else:
            return 0
    
    #same deal here don't remember the syntax
    #replaces value, incorporate into the count_message function of HelloDiscordBot
    def increment_count(self, user, count):
        self.execute('INSERT OR REPLACE INTO Crying (user_id, count) VALUES (?,?)', (user, count))
        self.commit()


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self) -> sqlite3.Connection:
        return self._conn

    @property
    def cursor(self) -> sqlite3.Cursor:
        return self._cursor

    def commit(self) -> None:
        self.connection.commit()

    def close(self, commit=True) -> None:
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql, params=()) -> None:
        self.cursor.execute(sql, params)

    #from my understanding retrives the result of the most reset query
    def fetchone(self) -> tuple:
        return self.cursor.fetchone()

    def fetchall(self) -> list[tuple]:
        return self.cursor.fetchall()