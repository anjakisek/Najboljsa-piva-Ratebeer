import re
import requests
import os
import orodja

st_strani = 11
lokacija = 'C:/Users/Anja/Documents/Programiranje1/Projekt-ratebeer/'
#lokacija =

def shrani_html1():
    for stran in range(1, st_strani):
        url = "https://www.ratebeer.com/beer-ratings/4/{}/".format(str(stran))
        r = requests.get(url)
        orodja.shrani_datoteko('{}stran{}.txt'.format(lokacija, str(stran)), str(r.text.encode("utf-8")))



