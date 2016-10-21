import re
import requests
import os
import orodja

def shrani_podatke():
    for stran in range(1, 11):
        url = 'https://www.ratebeer.com/beer-ratings/4/{}/'.format(str(stran))
        r = requests.get(url)
        orodja.shrani_datoteko('C:/Users/Anja/Documents/Programiranje1/Projekt-ratebeer/stran{}.txt'.format(str(stran)), str(r.text.encode("utf-8")))


