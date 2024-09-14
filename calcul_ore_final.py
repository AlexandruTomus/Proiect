import sqlite3
from datetime import datetime, timedelta
import csv
import smtplib
from email.mime.text import MIMEText
import schedule
import time

print("A inceput sa ruleze")

class CalculOre:
    def __init__(self, db_name="access_system.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def get_ore_lucrate(self):
        # Obtine toate intrarile si iesirile din baza de date fara sa filtreze dupa data curenta
        self.cursor.execute('''
            SELECT id_persoana, ora, sens FROM access
            ORDER BY id_persoana, ora ASC
        ''')  

        accesari = self.cursor.fetchall()

        #verific date
        if not accesari:
            print("Nu exista date în baza de date.")
        else:
            print(f"Am găsit {len(accesari)} înregistrări.")

        ore_lucrate = {}
        in_progress = {}

        #formam perechi de intrare - iesire si calculeaza orele lucrate
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

    def close(self):
        self.connection.close()

#salvare chiulangii in csv si txt
def salvare_chiulangii(ore_lucrate, minim_ore=8):
    data_curenta = datetime.now().strftime('%Y-%m-%d')
    chiulangii = []

    #converteste orele din timedelta in ore intregi
    for id_persoana, durata in ore_lucrate.items():
        ore = durata.total_seconds() / 3600
        if ore < minim_ore:
            chiulangii.append((id_persoana, round(ore, 2)))

    #scriem lista in fisiere csv si txt
    if chiulangii:
        csv_file = f'backup_intrari/{data_curenta}_chiulangii.csv'
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'OreLucrate'])
            writer.writerows(chiulangii)

        txt_file = f'backup_intrari/{data_curenta}_chiulangii.txt'
        with open(txt_file, mode='w') as file:
            for id_persoana, ore in chiulangii:
                file.write(f'{id_persoana},{ore}\n')


def trimite_email(manager_email, subiect, mesaj):
    from_email = "gonpachirokamaboko239@gmail.com"
    password = "twkz ayoq mwai rupq"  #App Password

    msg = MIMEText(mesaj)
    msg['Subject'] = subiect
    msg['From'] = from_email
    msg['To'] = manager_email

    try:
        print(f"Incercam sa trimitem email catre {manager_email}...")
        with smtplib.SMTP('smtp.gmail.com', 587) as server:  # Serverul Gmail
            server.starttls()  # Începe o conexiune securizată
            server.login(from_email, password)  # Autentificare
            print("Autentificarea a reusit.")
            server.sendmail(from_email, manager_email, msg.as_string())  # Trimite email-ul
        print("Email trimis cu succes!")
    except Exception as e:
        print(f"Eroare la trimiterea email-ului: {e}")


#functie pentru rulare verificari
def ruleaza_verificare():
    print("Incepem verificarea orelor lucrate:")
    calcul_ore = CalculOre()
    ore_lucrate = calcul_ore.get_ore_lucrate()

    #salveaza angajati care nu au lucrat 8 ore
    salvare_chiulangii(ore_lucrate)
    print(f"Ore lucrate procesate: {ore_lucrate}")  #mesaj ca sa vedem ce date sunt procesate

   #trimitem catre manager
    for id_persoana, durata in ore_lucrate.items():
        ore = durata.total_seconds() / 3600
        print(f"Angajatul {id_persoana} a lucrat {round(ore, 2)} ore.")

        if ore < 8:
            print(f"Angajatul {id_persoana} a lucrat mai puțin de 8 ore. Pregatim emailul") 
            trimite_email("tomusalexandru12@gmail.com", 
                          "Angajatul nu a lucrat 8 ore", 
                          f"Angajatul {id_persoana} a lucrat doar {round(ore, 2)} ore astazi.")

    calcul_ore.close()
    print("Verificarea a fost finalizata.")



if __name__ == "__main__":
    ruleaza_verificare()

    schedule.every().day.at("20:00").do(ruleaza_verificare)

    # while True:
    #     schedule.run_pending()  # Verifica dacă este ora 20:00
    #     time.sleep(60)  

