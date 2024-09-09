import os
import csv 
import shutil
from database import Database

class PoartaFisier:
    def __init__(self, directory='intrari', backup_directory='backup_intrari'):
        self.directory=directory
        self.backup_directory=backup_directory

        #folder backup daca nu exista
        if not os.path.exists(self.backup_directory):
            os.makedirs(self.backup_directory)
