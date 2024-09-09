from database import Database

class User:
    def __init__(self, first_name, last_name, company, id_manager):
        self.first_name = first_name
        self.last_name = last_name
        self.company = company
        self.id_manager = id_manager

    @staticmethod
    def register_user(first_name, last_name, company, id_manager):
        db = Database()
        db.cursor.execute('''
            INSERT INTO users (first_name, last_name, company, id_manager)
            VALUES (?, ?, ?, ?)
        ''', (first_name, last_name, company, id_manager))
        db.connection.commit()
        db.close()

# exemp inregistrare utilizator
if __name__ == "__main__":
    User.register_user("Alex", "Tomus", "CompanieBMW", 5)
