import re
import requests
import os
import orodja

st_strani = 11
lokacija = 'C:/Users/Anja/Documents/Programiranje1/Projekt-ratebeer/'
#lokacija =

def shrani_html1():
    '''Shrani html posamezne strani na listi piv in ustvari tekstovne datoteke'''
    for stran in range(1, st_strani):
        url = "https://www.ratebeer.com/beer-ratings/4/{}/".format(str(stran))
        r = requests.get(url)
        orodja.shrani_datoteko('{}stran{}.txt'.format(lokacija, str(stran)), str(r.text.encode("utf-8")))

iskanje = re.compile(r'<a style="font-size:20px; font-weight:bold;" href="(?P<naslov>.*?)"'
                     r'>(?P<ime>.*?)</a> <span class="uas"'
                     r'>(?P<ocena>.*?)</span> &nbsp;<div >.*?',
                     flags=re.DOTALL)
def poisci_v_html1():
    '''V html datotekah poišče povezavo do več informacij, oceno ter ime piva'''
    seznam_url = []
    seznam_slovarjev = []
    for stran in range (1, st_strani):
        tekst = orodja.preberi('{}stran{}.txt'.format(lokacija, str(stran)))
        for podatki in re.finditer(iskanje, tekst):
            seznam_url.append(podatki.group('naslov'))
            seznam_slovarjev.append(podatki.groupdict())

    orodja.shrani_datoteko('{}seznam_url.txt'.format(lokacija), str(seznam_url))
    orodja.shrani_datoteko('{}seznam_slovarjev.txt'.format(lokacija), str(seznam_slovarjev))




