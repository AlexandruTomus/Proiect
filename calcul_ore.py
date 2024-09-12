import sqlite3
from datetime import datetime, timedelta

class CalculOre:
    def __init__(self, db_name="access_system.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def get_ore_lucrate(self):
        #Obtin toate intrarile si iesirile pentru ziua curenta
        data_azi = datetime.now().strftime('%Y-%m-%d')
        self.cursor.execute('''
            SELECT id_persoana, ora, sens FROM access
            WHERE DATE(ora) = ?
            ORDER BY id_persoana, ora ASC
        ''', (data_azi,))
        accesari = self.cursor.fetchall()

        ore_lucrate = {}
        in_progress = {}

        for acces in accesari:
            id_persoana, ora, sens = acces
            ora = datetime.strptime(ora, '%Y-%m-%d %H:%M:%S')

            if sens == 'intrare':
                in_progress[id_persoana] = ora
            elif sens == 'iesire' and id_persoana in in_progress:
                intrare_ora = in_progress.pop(id_persoana)
                durata = ora - intrare_ora
                ore_lucrate[id_persoana] = ore_lucrate.get(id_persoana, timedelta()) + durata

        return ore_lucrate
