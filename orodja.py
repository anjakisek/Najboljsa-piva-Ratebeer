import re
import requests
import sys
import os

def shrani_datoteko(lokacija, besedilo):
    mapa = os.path.dirname(lokacija)
    if mapa:
        os.makedirs(mapa, exist_ok=True)
    with open(lokacija, 'w') as datoteka:
        datoteka.write(besedilo)
