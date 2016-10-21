import re
import requests
import sys
import os

def shrani_datoteko(lokacija, besedilo):
    imenik = os.path.dirname(lokacija)
    if imenik:
        os.makedirs(imenik, exist_ok=True)

    with open(lokacija, 'w') as datoteka:
        datoteka.write(besedilo)
        print('shranjeno!')
