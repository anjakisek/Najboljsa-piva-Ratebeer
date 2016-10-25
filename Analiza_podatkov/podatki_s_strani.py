import re
import requests
import os
import orodja

st_strani = 40
lokacija = '../../'

def shrani_html1():
    '''Shrani html posameznih strani na listi piv in ustvari tekstovne datoteke'''
    for stran in range(1, st_strani):
        url = "https://www.ratebeer.com/beer-ratings/4/{}/".format(str(stran))
        r = requests.get(url)
        orodja.shrani_datoteko('{}stran{}.txt'.format(lokacija, str(stran)), str(r.text.encode("utf-8")))


iskanje = re.compile(r'<a style="font-size:20px; font-weight:bold;" href="(?P<naslov>.*?)"'
                     r'>(?P<ime>.*?)</a> <span class="uas"'
                     r'>(?P<ocena>.*?)</span> &nbsp;<div >.*?',
                     flags=re.DOTALL)


def poisci_v_html1():
    '''V html datotekah poišče ime piva, oceno in povezavo do nadaljnih informacij,
    shrani csv datoteko s temi podatki ter seznam naslovov.'''
    seznam_url = []
    seznam_slovarjev = []
    for stran in range (1, st_strani):
        tekst = orodja.preberi('{}stran{}.txt'.format(lokacija, str(stran)))
        for podatki in re.finditer(iskanje, tekst):
            seznam_url.append(podatki.group('naslov'))
            seznam_slovarjev.append(podatki.groupdict())

    orodja.shrani_seznam('../seznam_url.txt', seznam_url)
    orodja.shrani_csv(seznam_slovarjev, ['ime', 'ocena', 'naslov'] , 'ocene.csv')






iskanje2 = re.compile(r'rel="canonical"><span itemprop="name">(?P<ime>.*?)<span></a>.*?'
                      r'Brewed by.*?<span itemprop="name">(?P<pivovarna>.*?);</span></a>.*?'
                      r'Style:.*?>(?P<stil>.*?);</a>.*?'
                      r'<br>(?P<Lokacija>.*?)</div>.*?'
                      r'>EST. CALORIES</abbr>: <big style="color: #777;">(?P<kalorije>\d{3,4})</strong>.*?'
                      r'<abbr title="Alcohol By Volume">ABV</abbr>: <big style="color: #777;"><strong>(?P<alkohol>.*?)</strong>',
                      #r'(rel="modal:open">(?P<kozarec>.*?)</a>, <div id="modal")*',
                      flags = re.DOTALL)


pivo = []

def shrani_drugo_tabelo():
    '''Za posamezno pivo obišče spletno stran in shrani podatke: ime, pivovarno, stil, kalorije in vsebnost alkohola.'''
    naslovi = orodja.preberi('../seznam_url.txt')
    for naslov in naslovi.split('\n'):
        url = 'https://www.ratebeer.com{}'.format(naslov)
        besedilo = requests.get(url)
        for pivce in re.finditer(iskanje2, besedilo.text):
            print(pivce.groupdict())
            pivo.append(pivce.groupdict())
    orodja.shrani_csv(pivo, ['ime', 'pivovarna', 'stil', 'kalorije', 'alkohol'], 'pivo_csv')

def olepsaj(info):
    info['pivovarna'] = olepsaj_lokacijo(info['pivovarna'])
    info['kaloije'] = int(info['kaloije'])
    info['alkohol'] = float(olepsaj_alkohol(info['alkohol']))


def olepsaj_alkohol(besedilo):
    return besedilo[:len(besedilo) - 1]

def olepsaj_lokacijo(besedilo):
    niz = besedilo[::-1]
    while niz[0] == ' ':
        niz = niz[1:]
    return niz[::-1]







