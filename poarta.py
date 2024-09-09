#gestionare fisier csv
import os
import csv
import shutil
from database import Database

class PoartaFisier:
    def __init__(self, directory='intrari', backup_directory='backup_intrari'):
        self.directory = directory
        self.backup_directory = backup_directory

        # folder backup
        if not os.path.exists(self.backup_directory):
            os.makedirs(self.backup_directory)

    def process_files(self):
        db = Database()

        #verifica fisierele din folder intrari


        for filename in os.listdir(self.directory):
            if filename.endswith('.csv'):
                poarta_name = filename.split('.')[0]  # Eextrage numele portii din numele fisierului
                #citeste fisier csv
                file_path = os.path.join(self.directory, filename)
                with open(file_path, mode='r') as file:
                    csv_reader = csv.reader(file)
                    for row in csv_reader:
                        if len(row) == 3:  # id sens ora
                            id_persoana, ora, sens = row

                            #salvez intrarea in baza
                            db.cursor.execute('''
                                INSERT INTO access (id_persoana, ora, sens, poarta)
                                VALUES (?, ?, ?, ?)
                            ''', (id_persoana, ora, sens, poarta_name))
                            db.connection.commit()
                            shutil.move(file_path, os.path.join(self.backup_directory, filename))
                            #muta fisier procesat in folder backup ><><>.
        db.close()

#Test
# if __name__ == "__main__":
#     poarta = PoartaFisier()
#     poarta.process_files()
