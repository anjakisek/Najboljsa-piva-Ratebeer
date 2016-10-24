import re
import requests
import sys
import os
import csv

def shrani_datoteko(lokacija, besedilo):
    imenik = os.path.dirname(lokacija)
    if imenik:
        os.makedirs(imenik, exist_ok=True)

    with open(lokacija, 'w') as datoteka:
        datoteka.write(besedilo)
        print('shranjeno')

def shrani_seznam(lokacija, seznam):
    imenik = os.path.dirname(lokacija)
    if imenik:
        os.makedirs(imenik, exist_ok=True)

    with open(lokacija, 'w') as datoteka:
        for element in seznam:

            datoteka.write(element + '\n')
        print('shranjeno')


def preberi(datoteka):
    '''vrne niz vsebine datoteke'''
    with open(datoteka) as fajl:
        besedilo = fajl.read()
        return besedilo

def shrani_csv(slovarji, imena_polj, ime_datoteke):
    '''Ustvari csv datoteko s slovarji'''
    with open('../{}'.format(ime_datoteke), 'w') as csv_dat:
        writer = csv.DictWriter(csv_dat, fieldnames=imena_polj)
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)
        print('shranjen csv')