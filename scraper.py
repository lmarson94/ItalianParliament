import urllib.request as urllib
from bs4 import BeautifulSoup
import pandas as pd
import collections
import numpy as np
import re
import time
import csv

onorevole = collections.OrderedDict()
partito = collections.OrderedDict()

link_nomi = "https://parlamento17.openpolis.it/lista-dei-parlamentari-in-carica/camera/nome/asc"
soup = BeautifulSoup(urllib.urlopen(link_nomi), "lxml")

for table_nomi in soup.findAll("table", class_='disegni-decreti column-table lazyload'):
    for row in table_nomi.find("tbody").findAll("tr"):
        th = row.find("th")
        nome = th.find('a').string
        onorevole[nome] = []

        p = re.search('\(.*\)', str(th))
        if p is not None:
            partito[nome] = p.group(0)[1:-1]
        else:
            partito[nome] = "nessuno"

w = csv.writer(open("partiti_camera.csv", "w"))
for key, val in partito.items():
    w.writerow([key, val])

exit()

file = 1
counter = 0
for page_number in range(1, 2945):
    openpolis = "https://parlamento17.openpolis.it/tutte-le-votazioni-in-parlamento/data/desc/page/" + str(page_number)
    soup = BeautifulSoup(urllib.urlopen(openpolis), "lxml")

    votazioni = soup.find("table", class_='disegni-decreti column-table').find("tbody")
    for row in votazioni.findAll("tr"):
        th = row.find("th")
        camera = th.find("span").string.split()[2][:-1]

        if camera == 'Camera':
            counter += 1
            print(counter)

            link = 'https://parlamento17.openpolis.it' + th.find("a")['href']

            soup2 = BeautifulSoup(urllib.urlopen(link), "lxml")

            try:
                table = soup2.find("table", class_='chart tablesorter').find("tbody")
            except:
                print("Error!!!!!")
                print(openpolis)
                print(link)
                counter -= 1
                continue

            for row in table.findAll("tr"):
                td = row.findAll('td')

                n = td[0]
                nome = n.find('a').string
                # partito = re.search('\(.*\)', str(td[0])).group(0)[1:-1]

                v = td[1].string
                if v == 'Favorevole':
                    voto = 1
                elif v == 'Contrario':
                    voto = 0
                else:
                    voto = 0.5

                if nome in onorevole:
                    onorevole[nome].append(voto)

            for nome in list(onorevole.keys()):
                if len(onorevole[nome]) < counter:
                    onorevole[nome].append(0.5)

            # store on file
            if np.shape(np.array(list(onorevole.values())))[1] % 2000 == 0:
                mp = pd.DataFrame(np.array(list(onorevole.values())))
                mp['Nome'] = list(onorevole.keys())

                cols = mp.columns.tolist()
                cols = cols[-1:] + cols[:-1]

                mp = mp[cols]

                lbl = 'camera' + str(file) + '.csv'
                mp.to_csv(lbl, index=False)

                file += 1

                time.sleep(10)


mp = pd.DataFrame(np.array(list(onorevole.values())))
mp['Nome'] = list(onorevole.keys())

cols = mp.columns.tolist()
cols = cols[-1:] + cols[:-1]

mp = mp[cols]

lbl = 'camera' + str(file) + '.csv'
mp.to_csv(lbl, index=False)


