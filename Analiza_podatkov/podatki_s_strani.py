import re
import requests
import os
import orodja

st_strani = 100
lokacija = '../../'


iskanje = re.compile(r'<a style="font-size:20px; font-weight:bold;" href="/beer(?P<naslov>.*?/)\d{3,11}/"'
                     r'>(?P<ime>.*?)</a> <span class="uas"',
                     flags=re.DOTALL)


iskanje2 = re.compile(r'<link.*?http://www.ratebeer.com/beer(?P<naslov>.*?)"/>.*?'
                      r'<big>.*?rewed.*?">(?P<pivovarna>\w.*?)<.*?>.*?'
                      r'Style:.*?">(?P<stil>\w.*?)</a>.*?'
                      r'<br>(?P<mesto>.*?),.*?(?P<drzava>\w*?)(\s)*?</div>.*?'
                      r'>WEIGHTED AVG:.*?<strong><span itemprop="ratingValue">(?P<ocena>\d\.?\d{0,3})</span>.*?'
                      #r'>EST. CALORIES</abbr>: <big style="color: #777;">(?P<kalorije>\d{2,4})</strong>.*?'
                      r'<abbr title="Alcohol By Volume".*?><strong>(?P<alkohol>.*?)</strong>',
                      flags = re.DOTALL)


iskanje_kozarci = re.compile(r'<link.*?http://www.ratebeer.com/beer(?P<naslov>.*?)"/>.*?'
                             r'Serve in .*?(?P<kozarec><a href="/ShowGlassware.*?</a>)</div>',
                             flags = re.DOTALL)


###############################################
def test():
    url = "https://www.ratebeer.com/beer-ratings/4/1/"
    r = requests.get(url)
    orodja.shrani_datoteko('stran1.txt'.format(lokacija), r.text)
    tekst = orodja.preberi('stran1.txt'.format(lokacija))
    for podatki in re.finditer(iskanje, tekst):
        print(podatki.group('ime'))
###################################################




def shrani_html1():
    '''Shrani html posameznih strani na listi piv in ustvari tekstovne datoteke'''
    for stran in range(1, st_strani):
        url = "https://www.ratebeer.com/beer-ratings/4/{}/".format(str(stran))
        r = requests.get(url)
        orodja.shrani_datoteko('{}html1/stran{}.txt'.format(lokacija, str(stran)), str(r.text.encode('utf8')))



def poisci_v_html1():
    '''V html datotekah poišče ime piva, oceno in povezavo do nadaljnih informacij,
    shrani csv datoteko s temi podatki ter seznam naslovov.'''
    seznam_url = []
    seznam_slovarjev = []
    seznam_porabljenih = []
    for stran in range (1, st_strani):
        tekst = orodja.preberi('{}html1/stran{}.txt'.format(lokacija, str(stran)))
        for podatki in re.finditer(iskanje, tekst):
            if podatki.group('ime') not in seznam_porabljenih:
                seznam_url.append(podatki.group('naslov'))
                seznam_slovarjev.append(podatki.groupdict())
                seznam_porabljenih.append(podatki.group('ime'))

    orodja.shrani_seznam('../seznam_url.txt', seznam_url)
    orodja.shrani_csv(seznam_slovarjev, ['ime', 'naslov'] , 'imena.csv')





def olepsaj(podatki):
    '''Preuredi obliko vrednosti v slovarju'''
    info = podatki.groupdict()
    info['mesto'] = olepsaj_lokacijo(info['mesto'])
    #info['kalorije'] = int(info['kalorije'])
    info['alkohol'] = olepsaj_alkohol(info['alkohol'])
    return info


def olepsaj_alkohol(besedilo):
    '''Pobriše znak %'''
    return besedilo[:len(besedilo) - 1]


def olepsaj_lokacijo(besedilo):
    '''Za mesta, ki imajo pred seboj linke, izloci mesto'''
    if besedilo[0] == '<':
        isci = re.compile('<a.*?>(?P<mesto>.*?)<.*?>')
        for i in re.finditer(isci, besedilo):
            return i.group('mesto')




def shrani_html2():
    '''Za posamezno pivo obisce spletno stran in shrani datoteke'''
    naslovi = orodja.preberi('../seznam_url.txt').split('\n')
    for i in range(0, len(naslovi) - 1):
        naslov = naslovi[i]
        url = 'https://www.ratebeer.com{}'.format(naslov)
        besedilo = requests.get(url)
        orodja.shrani_datoteko('{}html2/stran{}.txt'.format(lokacija, str(i + 1)), str(besedilo.text.encode('utf8')))






def shrani_drugo_tabelo():
    '''Za posamezno pivo prebere html2 in shrani csv: naslov, pivovarno, mesto, državo, stil, (kalorije) in vsebnost alkohola.'''
    pivo = []
    for i in range(1, 677):
        besedilo = orodja.preberi('{}html2/stran{}.txt'.format(lokacija, i))
        for glazek in re.finditer(iskanje2, besedilo):
            print(glazek.groupdict())
            pivo.append(olepsaj(glazek))
    orodja.shrani_csv(pivo, ['naslov', 'ocena', 'pivovarna', 'mesto', 'drzava', 'stil', 'alkohol'], 'pivo.csv')






def olepsaj_kozarce(info):
    '''Ponovni regex niza okoli kozarcev, vrne seznam'''
    besedilo = info.groupdict()
    isci = re.compile(r'.*?modal:open">(?P<kozarec>.*?)</a>.*?', flags = re.DOTALL)
    seznam = []
    for i in re.finditer(isci, str(besedilo)):
        seznam.append(i.group('kozarec'))
    besedilo['kozarec'] = seznam
    return besedilo




kozarci = []
seznam_kozarci = []

def shrani_tabelo_kozarci():
    '''Prebere html2 in shrani csv za naslov piva ter pripadajoce kozarce'''
    for i in range(1, 677):
        besedilo = orodja.preberi('{}html2/stran{}.txt'.format(lokacija, i))
        for glaz in re.finditer(iskanje_kozarci, besedilo):
            kozarci.append(olepsaj_kozarce(glaz))
    for pivce in kozarci:
        for kozarec in pivce.pop('kozarec'):
            seznam_kozarci.append({'naslov': pivce['naslov'], 'kozarec': kozarec})
    orodja.shrani_csv(seznam_kozarci, ['naslov', 'kozarec'], 'kozarci.csv')












