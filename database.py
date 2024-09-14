import sqlite3

class Database:
    def __init__(self, db_name="access_system.db"):
        #se conecteaza
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        #tabela utilizatori
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                company TEXT NOT NULL,
                id_manager INTEGER NOT NULL
            )
        ''')

        #tabela pentru acces+relatia cu tabela users
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS access (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_persoana INTEGER NOT NULL,
                ora TEXT NOT NULL,
                sens TEXT NOT NULL,
                poarta TEXT NOT NULL,
                FOREIGN KEY (id_persoana) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        self.connection.commit()

    def close(self):
        self.connection.close()
