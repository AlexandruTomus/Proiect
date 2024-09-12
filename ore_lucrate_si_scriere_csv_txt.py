import csv
from datetime import datetime

def salvare_chiulangii(ore_lucrate, minim_ore=8):
    data_curenta = datetime.now().strftime('%Y-%m-%d')
    chiulangii = []

    # Convertim orele din timedelta în ore intregi
    for id_persoana, durata in ore_lucrate.items():
        ore = durata.total_seconds() / 3600
        if ore < minim_ore:
            #numele și managerul persoanei din baza
            chiulangii.append((id_persoana, round(ore, 2)))

    #lista in fisier csv si txt
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
