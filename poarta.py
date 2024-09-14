import sqlite3
import os
import csv
import shutil

class PoartaFisier:
    def __init__(self, db_name="access_system.db", intrari_directory="intrari", backup_directory="backup_intrari"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.intrari_directory = intrari_directory
        self.backup_directory = backup_directory

        # Asigura-te ca tabelele exista
        self.create_tables()

    def create_tables(self):
        # Cream tabela pentru utilizatori
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Nume TEXT NOT NULL,
                Prenume TEXT NOT NULL,
                Companie TEXT NOT NULL,
                IdManager INTEGER
            );
        ''')

        # Cream tabela pentru inregistrarile de acces
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS access (
                id_persoana INTEGER,
                ora TEXT,
                sens TEXT,
                poarta TEXT
            );
        ''')

    def inregistreaza_utilizator(self, nume, prenume, companie, id_manager):
        # Inseram un utilizator nou in tabela users
        self.cursor.execute('''
            INSERT INTO users (Nume, Prenume, Companie, IdManager)
            VALUES (?, ?, ?, ?)
        ''', (nume, prenume, companie, id_manager))
        self.connection.commit()
        print(f"Utilizatorul {nume} {prenume} a fost inregistrat cu succes!")

    def process_files(self):
        print("Incepem procesarea fisierelor...")
        files = [f for f in os.listdir(self.intrari_directory) if os.path.isfile(os.path.join(self.intrari_directory, f))]
        print(f"Fisiere gasite: {files}")

        for filename in files:
            file_path = os.path.join(self.intrari_directory, filename)

            with open(file_path, newline='') as csvfile:
                csv_reader = csv.reader(csvfile)
                for row in csv_reader:
                    # Asteptam formatul: id_persoana, ora, sens
                    print(f"Inseram in baza de date: {row}")
                    self.cursor.execute('''
                        INSERT INTO access (id_persoana, ora, sens, poarta)
                        VALUES (?, ?, ?, ?)
                    ''', (row[0], row[1], row[2], filename))
            self.connection.commit()

            # Mutam fisierul in backup dupa procesare
            shutil.move(file_path, os.path.join(self.backup_directory, filename))
            print(f"Mutam fisierul {filename} in backup.")

    def close(self):
        self.connection.close()

# Testam functionalitatea
if __name__ == "__main__":
    poarta = PoartaFisier()

    # Exemplu de inregistrare utilizator
    poarta.inregistreaza_utilizator("Popescu", "Ion", "TechCorp", 1)

    # Procesam fisierele din folderul intrari
    poarta.process_files()

    poarta.close()
