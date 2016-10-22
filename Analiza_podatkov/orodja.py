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
        print('shranjeno')


def preberi(datoteka):
    '''vrne niz html zapisa v datoteki'''
    with open(datoteka) as fajl:
        besedilo = fajl.read()
        return besedilo
