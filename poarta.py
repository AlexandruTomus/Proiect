import os
import csv
import shutil
from database import Database

class PoartaFisier:
    def __init__(self, directory='intrari', backup_directory='backup_intrari'):
        self.directory = directory
        self.backup_directory = backup_directory

        # Creăm folderul de backup dacă nu există deja
        if not os.path.exists(self.backup_directory):
            os.makedirs(self.backup_directory)

    def process_files(self):
        print("Incepe procesarea")
        db = Database()

        #verif toate fișierele din directorul de intrari
        files = os.listdir(self.directory)
        print(f"Fișiere găsite: {', '.join(files)}")


        for filename in files:
            if filename.endswith('.csv'):
                print(f"Procesam fisierul: {filename}")
                poarta_name = filename.split('.')[0]  #extrage numele portii din numele fisierului

                #citeste fisier in csv
                file_path = os.path.join(self.directory, filename)
                with open(file_path, mode='r') as file:
                    csv_reader = csv.reader(file)
                    for row in csv_reader:
                        if len(row) == 3:  # Asumăm că fiecare rând are: id, ora, sens
                            id_persoana, ora, sens = row
                            print(f"Inseram in baza de date: {row}")

                            #salv intrarea in db
                            db.cursor.execute('''
                                INSERT INTO access (id_persoana, ora, sens, poarta)
                                VALUES (?, ?, ?, ?)
                            ''', (id_persoana, ora, sens, poarta_name))
                            db.connection.commit()

                #muta fisier
                print(f"Mutam fisierul {filename} în backup.")
                shutil.move(file_path, os.path.join(self.backup_directory, filename))

        db.close()

# Testare
if __name__ == "__main__":
    poarta = PoartaFisier() 
    poarta.process_files()    
