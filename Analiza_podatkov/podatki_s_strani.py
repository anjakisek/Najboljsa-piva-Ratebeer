import re
import requests
import os
import orodja

st_strani = 60
lokacija = '../../'

def shrani_html1():
    '''Shrani html posameznih strani na listi piv in ustvari tekstovne datoteke'''
    for stran in range(1, st_strani):
        url = "https://www.ratebeer.com/beer-ratings/4/{}/".format(str(stran))
        r = requests.get(url)
        orodja.shrani_datoteko('{}html1/stran{}.txt'.format(lokacija, str(stran)), str(r.text.encode('utf8')))


iskanje = re.compile(r'<a style="font-size:20px; font-weight:bold;" href="(?P<naslov>.*?/)\d*?/"'
                     r'>(?P<ime>.*?)</a> <span class="uas"'
                     r'>(?P<ocena>.*?)</span> &nbsp;<div >.*?',
                     flags=re.DOTALL)


def poisci_v_html1():
    '''V html datotekah poišče ime piva, oceno in povezavo do nadaljnih informacij,
    shrani csv datoteko s temi podatki ter seznam naslovov.'''
    seznam_url = []
    seznam_slovarjev = []
    for stran in range (1, st_strani):
        tekst = orodja.preberi('{}html1/stran{}.txt'.format(lokacija, str(stran)))
        for podatki in re.finditer(iskanje, tekst):
            seznam_url.append(podatki.group('naslov'))
            seznam_slovarjev.append(podatki.groupdict())

    orodja.shrani_seznam('../seznam_url.txt', seznam_url)
    #orodja.shrani_csv(seznam_slovarjev, ['ime', 'ocena', 'naslov'] , 'ocene.csv')





iskanje2 = re.compile(r'<h1 itemprop="name">(?P<ime>.*?)</h1>.*?'
                      r'<big>.*?rewed.*?">(?P<pivovarna>\w.*?)<.*?>.*?'
                      r'Style:.*?">(?P<stil>\w.*?)</a>.*?'
                      r'<br>(?P<mesto>.*?),.*?(?P<drzava>\w*?)(\s)*?</div>.*?'
                      r'>EST. CALORIES</abbr>: <big style="color: #777;">(?P<kalorije>\d{3,4})</strong>.*?'
                      r'<abbr title="Alcohol By Volume".*?><strong>(?P<alkohol>.*?)</strong>',
                      flags = re.DOTALL)


iskanje_naslov = re.compile(r'<link.*?http://www.ratebeer.com/beer(?P<naslov>.*?)"/>',flags = re.DOTALL)
iskanje_pivovarna = re.compile(r'<big>.*?rewed.*?">(?P<pivovarna>\w.*?)<.*?>',flags = re.DOTALL)
iskanje_stil = re.compile(r'Style:.*?">(?P<stil>\w.*?)</a>.*?', flags = re.DOTALL)
iskanje_lokacija = re.compile(r'Style:.*?<br>(?P<mesto>.*?),.*?(?P<drzava>\w*?)(\s)*?</div>.*?', flags = re.DOTALL)
iskanje_kalorije = re.compile(r'>EST. CALORIES</abbr>: <big style="color: #777;">(?P<kalorije>\d{3,4})</strong>.*?',flags = re.DOTALL)
iskanje_alkohol = re.compile(r'<abbr title="Alcohol By Volume".*?><strong>(?P<alkohol>.*?)</strong>',
                      flags = re.DOTALL)
iskanje_kozarec = re.compile(r'Serve in .*?(?P<kozarec><a href="/ShowGlassware.*?</a>)</div>',flags = re.DOTALL)



iskanje_kozarci = re.compile(r'<link.*?http://www.ratebeer.com/beer(?P<naslov>.*?)"/>.*?'
                             r'Serve in .*?(?P<kozarec><a href="/ShowGlassware.*?</a>)</div>',
                             flags = re.DOTALL)

def olepsaj_kozarce(info):
    besedilo = info.groupdict()
    isci = re.compile(r'.*?modal:open">(?P<kozarec>.*?)</a>.*?', flags = re.DOTALL)
    seznam = []
    for i in re.finditer(isci, str(besedilo)):
        seznam.append(i.group('kozarec'))
    besedilo['kozarec'] = seznam
    return besedilo



def olepsaj(podatki):
    info = podatki.groupdict()
    info['mesto'] = olepsaj_lokacijo(info['mesto'])
    info['kalorije'] = int(info['kalorije'])
    info['alkohol'] = float(olepsaj_alkohol(info['alkohol']))
    return info


def olepsaj_alkohol(besedilo):
    return besedilo[:len(besedilo) - 1]

def olepsaj_lokacijo(besedilo):
    if besedilo[0] == '<':
        isci = re.compile('<a.*?>(?P<mesto>.*?)<.*?>')
        for i in re.finditer(isci, besedilo):
            return i.group('mesto')


def proba():
    for i in range(1, 885):
        besedilo = orodja.preberi('{}html2/stran{}.txt'.format(lokacija, i))
        for glazek in re.finditer(iskanje2, besedilo):
            print(glazek.groupdict())




def shrani_html2():
    naslovi = orodja.preberi('../seznam_url.txt').split('\n')
    for i in range(0, len(naslovi) - 1):
        naslov = naslovi[i]
        url = 'https://www.ratebeer.com{}'.format(naslov)
        besedilo = requests.get(url)
        orodja.shrani_datoteko('{}html2/stran{}.txt'.format(lokacija, str(i + 1)), str(besedilo.text.encode('utf8')))

pivo = []
kozarci = []

def shrani_drugo_tabelo():
    '''Za posamezno pivo obišče spletno stran in shrani podatke: naslov, pivovarno, mesto, državo, stil, kalorije in vsebnost alkohola.'''
    for i in range(1, 886):
        besedilo = orodja.preberi('{}html2/stran{}.txt'.format(lokacija, i))
        for glazek in re.finditer(iskanje2, besedilo):
            print(glazek.groupdict())
            pivo.append(olepsaj(glazek))
    orodja.shrani_csv(pivo, ['naslov', 'pivovarna', 'mesto', 'drzava', 'stil', 'alkohol', 'kalorije'], 'pivo_csv')

seznam_kozarci = []

def shrani_tabelo_kozarci():
    for i in range(1, 886):
        besedilo = orodja.preberi('{}html2/stran{}.txt'.format(lokacija, i))
        for glaz in re.finditer(iskanje_kozarci, besedilo):
            kozarci.append(olepsaj_kozarce(glaz))
    for pivce in kozarci:
        for kozarec in pivce.pop('kozarec'):
            seznam_kozarci.append({'naslov': pivce['naslov'], 'kozarec': kozarec})
    orodja.shrani_csv(seznam_kozarci, ['naslov', 'kozarec'], 'kozarci.csv')












