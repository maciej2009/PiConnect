# coding=utf-8
# !/usr/bin/python
# module: PiConnect.py

# TODO: Dodac swieta
# TODO: Dodac mozlwiosc wlaczenia przyciskiem
# TODO: Dodac regule, jezeli czujka ruchu wykrywa obecnosc domownika



import time
from datetime import datetime
from datetime import timedelta
import ConfigParser
import logging
import MySQLdb
# import webiopi
# from webiopi.devices.sensor.onewiretemp import DS18B20

class Parametry:
    def __init__(self):
        self.conf = ConfigParser.RawConfigParser()
        self.conf.read("PiConnect.conf")

         # DB
        self.db_server = self.conf.get('DB', 'db_server')
        self.db_name = self.conf.get('DB', 'db_name')
        self.db_username = self.conf.get('DB', 'db_username')
        self.db_password = self.conf.get('DB', 'db_password')
        self.db_timeinterval = float(self.conf.get('DB', 'db_timeinterval'))
        self.db_delay = float(self.conf.get('DB', 'db_delay'))

        # General
        self.temp_timeinterval = float(self.conf.get('General', 'temp_timeinterval'))
        self.log_loginglevel = self.conf.get('General', 'logginglevel')
        self.okresgrzewczy = bool(int(self.conf.get('General', 'okresgrzewczy')))

        # Czujniki
        self.czuj_zew = self.conf.get('Czujniki', 'czuj_zew')
        self.czuj_co_zas = self.conf.get('Czujniki', 'czuj_co_zas')
        self.czuj_co_return = self.conf.get('Czujniki', 'czuj_co_return')
        self.czuj_buf_top = self.conf.get('Czujniki', 'czuj_buf_top')
        self.czuj_buf_mid = self.conf.get('Czujniki', 'czuj_buf_mid')
        self.czuj_buf_low = self.conf.get('Czujniki', 'czuj_buf_low')
        self.czuj_wew_01 = self.conf.get('Czujniki', 'czuj_wew_01')
        self.czuj_wew_02 = self.conf.get('Czujniki', 'czuj_wew_02')
        self.czuj_wew_03 = self.conf.get('Czujniki', 'czuj_wew_03')
        self.czuj_wew_04 = self.conf.get('Czujniki', 'czuj_wew_04')
        self.czuj_wew_05 = self.conf.get('Czujniki', 'czuj_wew_05')
        self.czuj_wew_06 = self.conf.get('Czujniki', 'czuj_wew_06')
        self.czuj_wew_07 = self.conf.get('Czujniki', 'czuj_wew_07')
        self.czuj_wew_08 = self.conf.get('Czujniki', 'czuj_wew_08')
        self.czuj_wew_09 = self.conf.get('Czujniki', 'czuj_wew_09')
        self.czuj_wew_10 = self.conf.get('Czujniki', 'czuj_wew_10')
        self.czuj_cwu = self.conf.get('Czujniki', 'czuj_cwu')
        self.czuj_cwu_cyr = self.conf.get('Czujniki', 'czuj_cwu_cyr')

        # Styczniki

        self.st_taryfa = int(self.conf.get('Styczniki', 'st_taryfa'))
        self.st_co_pompa = int(self.conf.get('Styczniki', 'st_co_pompa'))
        self.st_co_zawor_otw = int(self.conf.get('Styczniki', 'st_co_zawor_otw'))
        self.st_co_zawor_zam = int(self.conf.get('Styczniki', 'st_co_zawor_zam'))
        self.st_grzalka_1 = int(self.conf.get('Styczniki', 'st_grzalka_1'))
        self.st_grzalka_2 = int(self.conf.get('Styczniki', 'st_grzalka_2'))
        self.st_grzalka_3 = int(self.conf.get('Styczniki', 'st_grzalka_3'))
        self.st_cwu_pompa_cyr = int(self.conf.get('Styczniki', 'st_cwu_pompa_cyr'))

         # CWU
        self.cwu_okno_1_start = self.conf.get('CWU', 'cwu_okno_1_start')
        self.cwu_okno_1_stop = self.conf.get('CWU', 'cwu_okno_1_stop')
        self.cwu_okno_1_days = self.conf.get('CWU', 'cwu_okno_1_days')
        self.cwu_okno_1_temp = int(self.conf.get('CWU', 'cwu_okno_1_temp'))
        self.cwu_okno_1_hist = int(self.conf.get('CWU', 'cwu_okno_1_hist'))
        self.cwu_okno_2_start = self.conf.get('CWU', 'cwu_okno_2_start')
        self.cwu_okno_2_stop = self.conf.get('CWU', 'cwu_okno_2_stop')
        self.cwu_okno_2_days = self.conf.get('CWU', 'cwu_okno_2_days')
        self.cwu_okno_2_temp = int(self.conf.get('CWU', 'cwu_okno_2_temp'))
        self.cwu_okno_2_hist = int(self.conf.get('CWU', 'cwu_okno_2_hist'))
        self.cwu_okno_3_start = self.conf.get('CWU', 'cwu_okno_3_start')
        self.cwu_okno_3_stop = self.conf.get('CWU', 'cwu_okno_3_stop')
        self.cwu_okno_3_days = self.conf.get('CWU', 'cwu_okno_3_days')
        self.cwu_okno_3_temp = int(self.conf.get('CWU', 'cwu_okno_3_temp'))
        self.cwu_okno_3_hist = int(self.conf.get('CWU', 'cwu_okno_3_hist'))
        self.cwu_okno_4_start = self.conf.get('CWU', 'cwu_okno_4_start')
        self.cwu_okno_4_stop = self.conf.get('CWU', 'cwu_okno_4_stop')
        self.cwu_okno_4_days = self.conf.get('CWU', 'cwu_okno_4_days')
        self.cwu_okno_4_temp = int(self.conf.get('CWU', 'cwu_okno_4_temp'))
        self.cwu_okno_4_hist = int(self.conf.get('CWU', 'cwu_okno_4_hist'))
        self.cwu_okno_5_start = self.conf.get('CWU', 'cwu_okno_5_start')
        self.cwu_okno_5_stop = self.conf.get('CWU', 'cwu_okno_5_stop')
        self.cwu_okno_5_days = self.conf.get('CWU', 'cwu_okno_5_days')
        self.cwu_okno_5_temp = int(self.conf.get('CWU', 'cwu_okno_5_temp'))
        self.cwu_okno_5_hist = int(self.conf.get('CWU', 'cwu_okno_5_hist'))
        self.cwu_okno_6_start = self.conf.get('CWU', 'cwu_okno_6_start')
        self.cwu_okno_6_stop = self.conf.get('CWU', 'cwu_okno_6_stop')
        self.cwu_okno_6_days = self.conf.get('CWU', 'cwu_okno_6_days')
        self.cwu_okno_6_temp = int(self.conf.get('CWU', 'cwu_okno_6_temp'))
        self.cwu_okno_6_hist = int(self.conf.get('CWU', 'cwu_okno_6_hist'))

         # CO

        self.co_okno_1_start = self.conf.get('CO', 'co_okno_1_start')
        self.co_okno_1_stop = self.conf.get('CO', 'co_okno_1_stop')
        self.co_okno_1_days = self.conf.get('CO', 'co_okno_1_days')
        self.co_okno_1_temp = int(self.conf.get('CO', 'co_okno_1_temp'))
        self.co_okno_1_hist = int(self.conf.get('CO', 'co_okno_1_hist'))
        self.co_okno_2_start = self.conf.get('CO', 'co_okno_2_start')
        self.co_okno_2_stop = self.conf.get('CO', 'co_okno_2_stop')
        self.co_okno_2_days = self.conf.get('CO', 'co_okno_2_days')
        self.co_okno_2_temp = int(self.conf.get('CO', 'co_okno_2_temp'))
        self.co_okno_2_hist = int(self.conf.get('CO', 'co_okno_2_hist'))
        self.co_okno_3_start = self.conf.get('CO', 'co_okno_3_start')
        self.co_okno_3_stop = self.conf.get('CO', 'co_okno_3_stop')
        self.co_okno_3_days = self.conf.get('CO', 'co_okno_3_days')
        self.co_okno_3_temp = int(self.conf.get('CO', 'co_okno_3_temp'))
        self.co_okno_3_hist = int(self.conf.get('CO', 'co_okno_3_hist'))
        self.co_okno_4_start = self.conf.get('CO', 'co_okno_4_start')
        self.co_okno_4_stop = self.conf.get('CO', 'co_okno_4_stop')
        self.co_okno_4_days = self.conf.get('CO', 'co_okno_4_days')
        self.co_okno_4_temp = int(self.conf.get('CO', 'co_okno_4_temp'))
        self.co_okno_4_hist = int(self.conf.get('CO', 'co_okno_4_hist'))
        self.co_okno_5_start = self.conf.get('CO', 'co_okno_5_start')
        self.co_okno_5_stop = self.conf.get('CO', 'co_okno_5_stop')
        self.co_okno_5_days = self.conf.get('CO', 'co_okno_5_days')
        self.co_okno_5_temp = int(self.conf.get('CO', 'co_okno_5_temp'))
        self.co_okno_5_hist = int(self.conf.get('CO', 'co_okno_5_hist'))
        self.co_okno_6_start = self.conf.get('CO', 'co_okno_6_start')
        self.co_okno_6_stop = self.conf.get('CO', 'co_okno_6_stop')
        self.co_okno_6_days = self.conf.get('CO', 'co_okno_6_days')
        self.co_okno_6_temp = int(self.conf.get('CO', 'co_okno_6_temp'))
        self.co_okno_6_hist = int(self.conf.get('CO', 'co_okno_6_hist'))

        # Taryfy
        self.taryfa1_cena = float(self.conf.get('Taryfy', 'taryfa1_cena'))
        self.taryfa2_cena = float(self.conf.get('Taryfy', 'taryfa2_cena'))

        self.taryfa2_1_dni = self.conf.get('Taryfy', 'taryfa2_1_dni')
        self.taryfa2_1_godz_start = self.conf.get('Taryfy', 'taryfa2_1_godz_start')
        self.taryfa2_1_godz_stop = self.conf.get('Taryfy', 'taryfa2_1_godz_stop')

        self.taryfa2_2_dni = self.conf.get('Taryfy', 'taryfa2_2_dni')
        self.taryfa2_2_godz_start = self.conf.get('Taryfy', 'taryfa2_2_godz_start')
        self.taryfa2_2_godz_stop = self.conf.get('Taryfy', 'taryfa2_2_godz_stop')

        self.taryfa2_3_dni = self.conf.get('Taryfy', 'taryfa2_3_dni')
        self.taryfa2_3_godz_start = self.conf.get('Taryfy', 'taryfa2_3_godz_start')
        self.taryfa2_3_godz_stop = self.conf.get('Taryfy', 'taryfa2_3_godz_stop')

        self.taryfa2_4_dni = self.conf.get('Taryfy', 'taryfa2_4_dni')
        self.taryfa2_4_godz_start = self.conf.get('Taryfy', 'taryfa2_4_godz_start')
        self.taryfa2_4_godz_stop = self.conf.get('Taryfy', 'taryfa2_4_godz_stop')

        self.taryfa2_5_dni = self.conf.get('Taryfy', 'taryfa2_5_dni')
        self.taryfa2_5_godz_start = self.conf.get('Taryfy', 'taryfa2_5_godz_start')
        self.taryfa2_5_godz_stop = self.conf.get('Taryfy', 'taryfa2_5_godz_stop')

        self.taryfa2_6_dni = self.conf.get('Taryfy', 'taryfa2_6_dni')
        self.taryfa2_6_godz_start = self.conf.get('Taryfy', 'taryfa2_6_godz_start')
        self.taryfa2_6_godz_stop = self.conf.get('Taryfy', 'taryfa2_6_godz_stop')

        # Piec
        self.poziom1 = int(self.conf.get('Piec', 'poziom1'))
        self.poziom2 = int(self.conf.get('Piec', 'poziom2'))
        self.poziom3 = int(self.conf.get('Piec', 'poziom3'))
        self.poziom4 = int(self.conf.get('Piec', 'poziom4'))
        self.poziom5 = int(self.conf.get('Piec', 'poziom5'))
        self.poziom6 = int(self.conf.get('Piec', 'poziom6'))

        # Pomieszczenia
        self.pom1_temp = int(self.conf.get('Pomieszczenia', 'pom1_temp'))
        self.pom1_hist = float(self.conf.get('Pomieszczenia', 'pom1_hist'))

    def read_all(self):

        self.__init__()


        """
        global par
        par = {
            # DB
            'db_server' : conf.get('DB', 'db_server'),
            'db_name' :conf.get('DB', 'db_name'),
            'db_username' : conf.get('DB', 'db_username'),
            'db_password' : conf.get('DB', 'db_password'),
            'db_timeinterval': float(conf.get('DB', 'db_timeinterval')),
            'db_delay': float(conf.get('DB', 'db_delay')),

            # General
            'temp_timeinterval': float(conf.get('General', 'temp_timeinterval')),
            'log_loginglevel' : conf.get('General', 'logginglevel'),
            'okresgrzewczy' : bool(int(conf.get('General', 'okresgrzewczy'))),

            # Czujniki
            'czuj_zew' : conf.get('Czujniki', 'czuj_zew'),
            'czuj_co_zas' : conf.get('Czujniki', 'czuj_co_zas'),
            'czuj_co_return' : conf.get('Czujniki', 'czuj_co_return'),
            'czuj_buf_top' : conf.get('Czujniki', 'czuj_buf_top'),
            'czuj_buf_mid' : conf.get('Czujniki', 'czuj_buf_mid'),
            'czuj_buf_low' : conf.get('Czujniki', 'czuj_buf_low'),
            'czuj_wew_01' : conf.get('Czujniki', 'czuj_wew_01'),
            'czuj_wew_02' : conf.get('Czujniki', 'czuj_wew_02'),
            'czuj_wew_03' : conf.get('Czujniki', 'czuj_wew_03'),
            'czuj_wew_04' : conf.get('Czujniki', 'czuj_wew_04'),
            'czuj_wew_05' : conf.get('Czujniki', 'czuj_wew_05'),
            'czuj_wew_06' : conf.get('Czujniki', 'czuj_wew_06'),
            'czuj_wew_07' : conf.get('Czujniki', 'czuj_wew_07'),
            'czuj_wew_08' : conf.get('Czujniki', 'czuj_wew_08'),
            'czuj_wew_09' : conf.get('Czujniki', 'czuj_wew_09'),
            'czuj_wew_10' : conf.get('Czujniki', 'czuj_wew_10'),
            'czuj_cwu' : conf.get('Czujniki', 'czuj_cwu'),
            'czuj_cwu_cyr' : conf.get('Czujniki', 'czuj_cwu_cyr'),

            # Styczniki

            'st_taryfa' : int(conf.get('Styczniki', 'st_taryfa')),
            'st_co_pompa' : int(conf.get('Styczniki', 'st_co_pompa')),
            'st_co_zawor_otw' : int(conf.get('Styczniki', 'st_co_zawor_otw')),
            'st_co_zawor_zam' : int(conf.get('Styczniki', 'st_co_zawor_zam')),
            'st_grzalka_1' : int(conf.get('Styczniki', 'st_grzalka_1')),
            'st_grzalka_2' : int(conf.get('Styczniki', 'st_grzalka_2')),
            'st_grzalka_3' : int(conf.get('Styczniki', 'st_grzalka_3')),
            'st_cwu_pompa_cyr' : int(conf.get('Styczniki', 'st_cwu_pompa_cyr')),

             # CWU
            'cwu_okno_1_start' : conf.get('CWU', 'cwu_okno_1_start'),
            'cwu_okno_1_stop' : conf.get('CWU', 'cwu_okno_1_stop'),
            'cwu_okno_1_days' : conf.get('CWU', 'cwu_okno_1_days'),
            'cwu_okno_1_temp' : int(conf.get('CWU', 'cwu_okno_1_temp')),
            'cwu_okno_1_hist' : int(conf.get('CWU', 'cwu_okno_1_hist')),
            'cwu_okno_2_start' : conf.get('CWU', 'cwu_okno_2_start'),
            'cwu_okno_2_stop' : conf.get('CWU', 'cwu_okno_2_stop'),
            'cwu_okno_2_days' : conf.get('CWU', 'cwu_okno_2_days'),
            'cwu_okno_2_temp' : int(conf.get('CWU', 'cwu_okno_2_temp')),
            'cwu_okno_2_hist' : int(conf.get('CWU', 'cwu_okno_2_hist')),
            'cwu_okno_3_start' : conf.get('CWU', 'cwu_okno_3_start'),
            'cwu_okno_3_stop' : conf.get('CWU', 'cwu_okno_3_stop'),
            'cwu_okno_3_days' : conf.get('CWU', 'cwu_okno_3_days'),
            'cwu_okno_3_temp' : int(conf.get('CWU', 'cwu_okno_3_temp')),
            'cwu_okno_3_hist' : int(conf.get('CWU', 'cwu_okno_3_hist')),
            'cwu_okno_4_start' : conf.get('CWU', 'cwu_okno_4_start'),
            'cwu_okno_4_stop' : conf.get('CWU', 'cwu_okno_4_stop'),
            'cwu_okno_4_days' : conf.get('CWU', 'cwu_okno_4_days'),
            'cwu_okno_4_temp' : int(conf.get('CWU', 'cwu_okno_4_temp')),
            'cwu_okno_4_hist' : int(conf.get('CWU', 'cwu_okno_4_hist')),
            'cwu_okno_5_start' : conf.get('CWU', 'cwu_okno_5_start'),
            'cwu_okno_5_stop' : conf.get('CWU', 'cwu_okno_5_stop'),
            'cwu_okno_5_days' : conf.get('CWU', 'cwu_okno_5_days'),
            'cwu_okno_5_temp' : int(conf.get('CWU', 'cwu_okno_5_temp')),
            'cwu_okno_5_hist' : int(conf.get('CWU', 'cwu_okno_5_hist')),
            'cwu_okno_6_start' : conf.get('CWU', 'cwu_okno_6_start'),
            'cwu_okno_6_stop' : conf.get('CWU', 'cwu_okno_6_stop'),
            'cwu_okno_6_days' : conf.get('CWU', 'cwu_okno_6_days'),
            'cwu_okno_6_temp' : int(conf.get('CWU', 'cwu_okno_6_temp')),
            'cwu_okno_6_hist' : int(conf.get('CWU', 'cwu_okno_6_hist')),

             # CO

            'co_okno_1_start' : conf.get('CO', 'co_okno_1_start'),
            'co_okno_1_stop' : conf.get('CO', 'co_okno_1_stop'),
            'co_okno_1_days' : conf.get('CO', 'co_okno_1_days'),
            'co_okno_1_temp' : int(conf.get('CO', 'co_okno_1_temp')),
            'co_okno_1_hist' : int(conf.get('CO', 'co_okno_1_hist')),
            'co_okno_2_start' : conf.get('CO', 'co_okno_2_start'),
            'co_okno_2_stop' : conf.get('CO', 'co_okno_2_stop'),
            'co_okno_2_days' : conf.get('CO', 'co_okno_2_days'),
            'co_okno_2_temp' : int(conf.get('CO', 'co_okno_2_temp')),
            'co_okno_2_hist' : int(conf.get('CO', 'co_okno_2_hist')),
            'co_okno_3_start' : conf.get('CO', 'co_okno_3_start'),
            'co_okno_3_stop' : conf.get('CO', 'co_okno_3_stop'),
            'co_okno_3_days' : conf.get('CO', 'co_okno_3_days'),
            'co_okno_3_temp' : int(conf.get('CO', 'co_okno_3_temp')),
            'co_okno_3_hist' : int(conf.get('CO', 'co_okno_3_hist')),
            'co_okno_4_start' : conf.get('CO', 'co_okno_4_start'),
            'co_okno_4_stop' : conf.get('CO', 'co_okno_4_stop'),
            'co_okno_4_days' : conf.get('CO', 'co_okno_4_days'),
            'co_okno_4_temp' : int(conf.get('CO', 'co_okno_4_temp')),
            'co_okno_4_hist' : int(conf.get('CO', 'co_okno_4_hist')),
            'co_okno_5_start' : conf.get('CO', 'co_okno_5_start'),
            'co_okno_5_stop' : conf.get('CO', 'co_okno_5_stop'),
            'co_okno_5_days' : conf.get('CO', 'co_okno_5_days'),
            'co_okno_5_temp' : int(conf.get('CO', 'co_okno_5_temp')),
            'co_okno_5_hist' : int(conf.get('CO', 'co_okno_5_hist')),
            'co_okno_6_start' : conf.get('CO', 'co_okno_6_start'),
            'co_okno_6_stop' : conf.get('CO', 'co_okno_6_stop'),
            'co_okno_6_days' : conf.get('CO', 'co_okno_6_days'),
            'co_okno_6_temp' : int(conf.get('CO', 'co_okno_6_temp')),
            'co_okno_6_hist' : int(conf.get('CO', 'co_okno_6_hist')),

            # Taryfy
            'taryfa1_cena' : float(conf.get('Taryfy', 'taryfa1_cena')),
            'taryfa2_cena' : float(conf.get('Taryfy', 'taryfa2_cena')),

            'taryfa2_1_dni' : conf.get('Taryfy', 'taryfa2_1_dni'),
            'taryfa2_1_godz_start' : conf.get('Taryfy', 'taryfa2_1_godz_start'),
            'taryfa2_1_godz_stop' : conf.get('Taryfy', 'taryfa2_1_godz_stop'),

            'taryfa2_2_dni' : conf.get('Taryfy', 'taryfa2_2_dni'),
            'taryfa2_2_godz_start' : conf.get('Taryfy', 'taryfa2_2_godz_start'),
            'taryfa2_2_godz_stop' : conf.get('Taryfy', 'taryfa2_2_godz_stop'),

            'taryfa2_3_dni' : conf.get('Taryfy', 'taryfa2_3_dni'),
            'taryfa2_3_godz_start' : conf.get('Taryfy', 'taryfa2_3_godz_start'),
            'taryfa2_3_godz_stop' : conf.get('Taryfy', 'taryfa2_3_godz_stop'),

            'taryfa2_4_dni' : conf.get('Taryfy', 'taryfa2_4_dni'),
            'taryfa2_4_godz_start' : conf.get('Taryfy', 'taryfa2_4_godz_start'),
            'taryfa2_4_godz_stop' : conf.get('Taryfy', 'taryfa2_4_godz_stop'),

            'taryfa2_5_dni' : conf.get('Taryfy', 'taryfa2_5_dni'),
            'taryfa2_5_godz_start' : conf.get('Taryfy', 'taryfa2_5_godz_start'),
            'taryfa2_5_godz_stop' : conf.get('Taryfy', 'taryfa2_5_godz_stop'),

            'taryfa2_6_dni' : conf.get('Taryfy', 'taryfa2_6_dni'),
            'taryfa2_6_godz_start' : conf.get('Taryfy', 'taryfa2_6_godz_start'),
            'taryfa2_6_godz_stop' : conf.get('Taryfy', 'taryfa2_6_godz_stop'),

            # Piec
            'poziom1' : int(conf.get('Piec', 'poziom1')),
            'poziom2' : int(conf.get('Piec', 'poziom2')),
            'poziom3' : int(conf.get('Piec', 'poziom3')),
            'poziom4' : int(conf.get('Piec', 'poziom4')),
            'poziom5' : int(conf.get('Piec', 'poziom5')),
            'poziom6' : int(conf.get('Piec', 'poziom6')),

            # Pomieszczenia
            'pom1_temp' : int(conf.get('Pomieszczenia', 'pom1_temp')),
            'pom1_hist' : float(conf.get('Pomieszczenia', 'pom1_hist'))
            }

        """
        logging.basicConfig(filename='PiConnect.log', level='DEBUG', format='%(levelname)s: %(asctime)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S %a', filemode = 'w')

        """
        for (char,n) in sorted(par.items()):
            # logging.info("[CONF] - Odczytano z pliku konfiguracyjnego parametr: %s = %s" % (char, n))
            # print "Odczytano z pliku konfiguracyjnego parametr: %s = %s" % (char, n)
            pass

        return par
        """

class Stycznik():

    def __init__(self, stycz = None):
        self.log = Log()
        self.stycz = stycz

        self.wlaczony = False

    def on(self):
        # Rpi: gpio.digitalWrite(stycz, gpio.HIGH)
        if self.wlaczony == False:
            self.log.debug("Stycznik nr %s został włączony" % self.stycz, 'STYCZNIK')
        self.wlaczony = True

    def off (self):
        # Rpi: gpio.digitalWrite(stycz, gpio.LOW)
        if self.wlaczony == True:
            self.log.debug("Stycznik nr %s został włączony" % self.stycz, 'STYCZNIK')
        self.wlaczony = False

    def reset_all(self):
        # Rpi: gpio = webiopi.GPIO
        par = Parametry()

        if par.st_taryfa not in ['0'," ",""]:
            # Rpi: gpio.setFunction(par['st_taryfa'], gpio.OUT)
            # Rpi: gpio.digitalWrite(par['st_taryfa'], gpio.LOW)
            # print "Reset stycznika nr %s: st_taryfa" % par['st_taryfa']
            pass

        if par.st_co_pompa not in ['0'," ",""]:
            # Rpi: gpio.setFunction(par['st_co_pompa'], gpio.OUT)
            # Rpi: gpio.digitalWrite(par['st_co_pompa'], gpio.LOW)
            # print "Reset stycznika nr %s: st_co_pompa" % par['st_co_pompa']
            pass

        if par.st_co_zawor_otw not in ['0'," ",""]:
            # Rpi: gpio.setFunction(par['st_co_zawor_otw'], gpio.OUT)
            # Rpi: gpio.digitalWrite(par['st_co_zawor_otw'], gpio.LOW)
            # pr    int "Reset stycznika nr %s: st_co_zawor_otw" % par['st_co_zawor_otw']
            pass

        if par.st_co_zawor_zam not in ['0'," ",""]:
            # Rpi: gpio.setFunction(par['st_co_zawor_zam'], gpio.OUT)
            # Rpi: gpio.digitalWrite(par['st_co_zawor_zam'], gpio.LOW)
            #print "Reset stycznika nr %s: st_co_zawor_zam" % par['st_co_zawor_zam']
            pass

        if par.st_grzalka_1 not in ['0'," ",""]:
            # Rpi: gpio.setFunction(par['st_grzalka_1'], gpio.OUT)
            # Rpi: gpio.digitalWrite(par['st_grzalka_1'], gpio.LOW)
            #print "Reset stycznika nr %s: st_grzalka_1" % par['st_grzalka_1']
            pass

        if par.st_grzalka_2 not in ['0'," ",""]:
            # Rpi: gpio.setFunction(par['st_grzalka_2'], gpio.OUT)
            # Rpi: gpio.digitalWrite(par['st_grzalka_2'], gpio.LOW)
            #print "Reset stycznika nr %s: st_grzalka_2" % par['st_grzalka_2']
            pass

        if par.st_grzalka_3 not in ['0'," ",""]:
            # Rpi: gpio.setFunction(par['st_grzalka_3'], gpio.OUT)
            # Rpi: gpio.digitalWrite(par['st_grzalka_3'], gpio.LOW)
            #print "Reset stycznika nr %s: st_grzalka_3" % par['st_grzalka_3']
            pass

        if par.st_cwu_pompa_cyr not in ['0'," ",""]:
            # Rpi: gpio.setFunction(par['st_cwu_pompa_cyr'], gpio.OUT)
            # Rpi: gpio.digitalWrite(par['st_cwu_pompa_cyr'], gpio.LOW)
            #print "Reset stycznika nr %s: st_cwu_pompa_cyr" % par['st_cwu_pompa_cyr']
            pass
        self.log.debug('Zresetowano konfigurację wszystkich styczników', 'STYCZNIK')

class DB():
    def __init__(self):
        self.par = Parametry()
        self.log = Log()
        #self.par.read_all()

    def db_init(self):
        try:

            time.sleep(self.par.db_delay)

            self.conn = MySQLdb.connect(host=self.par.db_server, user=self.par.db_username, passwd=self.par.db_password, db=self.par.db_name)

            self.log.info('[DB] - Odczytano z pliku konfiguracyjnego definicję połączenia DB: host= %s, user=%s, passwd=%s, db=%s' % (self.par.db_server, self.par.db_username, self.par.db_password, self.par.db_name),'DB')
            self.log.info('[DB] - Podłączono do bazy danych DB: host= %s, user=%s, passwd=%s, db=%s' % (self.par.db_server, self.par. db_username, self.par.db_password, self.par.db_name), 'DB')


        except:
            # TBD: check_SQL_connection()
            #	print 'Blad polaczenia z DB'
            self.log.error('[DB] - Blad podlaczenia do bazy danych: host= %s, user=%s, passwd=%s, db=%s' %
                          (self.par.db_name, self.par.db_username, self.par.db_password, self.par.db_name), 'DB')

            pass

    def zapis_temp(self):

        temp = Temp()
        # temp.read_all()

        piec = Piec()

        # conn.open
        """
        conn.begin()

        tbl_temperatury = conn.cursor()

        sql = "" INSERT INTO temperatury VALUES ('%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "" % \
                            (datetime.strftime(datetime.today(),'%Y-%m-%d %H:%M:%S'),
                            temp.czuj_zew,
                            temp.czuj_co_zas,
                            temp.czuj_co_return,
                            temp.czuj_buf_top,
                            temp.czuj_buf_mid,
                            temp.czuj_buf_low,
                            temp.czuj_wew_01,
                            temp.czuj_wew_02,
                            temp.czuj_wew_03,
                            temp.czuj_wew_04,
                            temp.czuj_wew_05,
                            temp.czuj_wew_06,
                            temp.czuj_wew_07,
                            temp.czuj_wew_08,
                            temp.czuj_wew_09,
                            temp.czuj_wew_10,
                            temp.czuj_cwu,
                            temp.czuj_cwu_cyr,
                            piec.moc,
                            piec.poziom,
                            piec.taryfa_nr,
                            0,
                            0
                        )
        # print sql

        tbl_temperatury.execute(sql)
        conn.commit()
        """


class Piec():

        def __init__(self):

            self.par = Parametry()

            self.st_blokada_grzania = Stycznik(self.par.st_taryfa)

            self.st_grzalka_1 = Stycznik(self.par.st_grzalka_1)
            self.st_grzalka_2 = Stycznik(self.par.st_grzalka_2)
            self.st_grzalka_3 = Stycznik(self.par.st_grzalka_3)



            self.moc = 0
            self.taryfa_nr = 1
            self.poziom = 0
            self.podgrzewam_CWU = False            # Czy grzeje dla CWU?
            self.podgrzewam_CO = False             # Czy grzeje dla CO?

        def on (self, zrodlo, temp_pieca, okno_start, okno_stop, temp_co_cwu, histereza_co_cwu,  poziom = 1):   # źródło = CWU, CO lub dogrzanie do temp. min po wyjściu z petli.

            zmieniono = False

            tmp_podgrzewam_CO = self.podgrzewam_CO
            tmp_podgrzewam_CWU = self.podgrzewam_CWU


            """
            if self.taryfa2
                self.taryfa_nr = 2
            elif taryfa2()[0]==False:
                self.taryfa_nr = 1
            """

            # Wyłaczenie pieca CO jeżeli ma grzać SWU i na odwrót
            if zrodlo == 'CWU' and tmp_podgrzewam_CO is True:
                self.off('CO',temp_pieca,okno_start, okno_stop,temp_co_cwu, histereza_co_cwu)

            if zrodlo == 'CO' and tmp_podgrzewam_CWU is True:
                self.off('CWU',temp_pieca,okno_start, okno_stop,temp_co_cwu, histereza_co_cwu)

            # wyłacenie pieca jeżeli poziom ma ulec zmianie i piec działa
            if self.poziom > 0 and poziom <> self.poziom:
                self.off(zrodlo, temp_pieca,okno_start, okno_stop,temp_co_cwu, histereza_co_cwu)

            # odczytaj ponownie self...... bo piec.off() mógł je zmienić.
            tmp_podgrzewam_CO = self.podgrzewam_CO
            tmp_podgrzewam_CWU = self.podgrzewam_CWU


            # jeżeli coś się zmieniło to przestaw styczniki i zaloguj zmiany
            if zrodlo == 'CWU' and tmp_podgrzewam_CWU is False:
                zmieniono = True
                self.podgrzewam_CWU = True

            if zrodlo == 'CO' and tmp_podgrzewam_CO is False:
                zmieniono = True
                self.podgrzewam_CO = True


            ##### może dodać jeszcze zmieniono = true jeżeli nastapi zmiana poziomów
            ##### if self.poziom != poziom:
            #####   zmieniono = True



            if zmieniono is True:               # jeżeli nastapiła jakaś zmiana

                if poziom == 1:            # 3kW
                    self.st_grzalka_1.on()
                    self.st_grzalka_2.off()
                    self.st_grzalka_3.off()
                    self.moc = 3

                elif poziom == 2:           # 6kW
                    self.st_grzalka_1.off()
                    self.st_grzalka_2.on()
                    self.st_grzalka_3.off()
                    self.moc = 6

                elif poziom == 3:           # 9kW
                    self.st_grzalka_1.off()
                    self.st_grzalka_2.off()
                    self.st_grzalka_3.on()
                    self.moc = 9

                elif poziom == 4:           # 12kW
                    self.st_grzalka_1.on()
                    self.st_grzalka_2.off()
                    self.st_grzalka_3.on()
                    self.moc = 12

                elif poziom == 5:           # 15kW
                    self.st_grzalka_1.off()
                    self.st_grzalka_2.on()
                    self.st_grzalka_3.on()
                    self.moc = 15

                elif poziom == 6:           # 18kW
                    self.st_grzalka_1.on()
                    self.st_grzalka_2.on()
                    self.st_grzalka_3.on()
                    self.moc = 18


                logging.info("[PIEC][%s] - Włączono grzanie na poziomie %s z mocą %s kW. Okno: %s - %s. Okres grzewczy: %s. Temp zbiornika: %s. Temp zadana: %s. Histereza: +/- %s." % (
                                    zrodlo, poziom, self.moc, okno_start, okno_stop, self.par.okresgrzewczy, temp_pieca, temp_co_cwu, histereza_co_cwu))
                print "[PIEC][%s] - Włączono grzanie na poziomie %s z mocą %s kW. Okno: %s - %s. Okres grzewczy: %s. Temp zbiornika: %s. Temp zadana: %s. Histereza: +/- %s." % (
                                    zrodlo, poziom, self.moc, okno_start, okno_stop, self.par.okresgrzewczy, temp_pieca, temp_co_cwu, histereza_co_cwu)
                
                
                """
                if self.poziom != poziom:   # zapis do tabeli "piec" jezeli nastapiła zmiana poziomu

                    #try:
                    # conn.open
                    conn.begin()

                    if self.poziom == 0 or self.poziom == None:        # gdy właczamy piec, a nie zmieniamy wartość poziomu
                        tbl_piec_start = conn.cursor()
                        self.czas_start = datetime.today()

                        str = '''INSERT INTO piec VALUES('%s', '%s','0000-00-00 00:00:00',0,%s,%s,%s,%s,0,%s)''' % (zrodlo, datetime.strftime(self.czas_start,'%Y-%m-%d %H:%M:%S'), poziom, self.moc, self.taryfa_nr, self.taryfa_pln, self.taryfa_okno)
                        print str
                        tbl_piec_start.execute(str)
                    else:
                        tbl_piec_stop = conn.cursor()
                        il_godzin1 = datetime.today()- self.czas_start
                        il_godzin = round(il_godzin1.total_seconds()/60/60,10)

                        str = ""UPDATE piec SET piec_czas_stop = '%s', piec_il_godzin = '%s', piec_taryfa_wartosc = ROUND (piec_moc * piec_taryfa_pln * '%s',2) WHERE piec_czas_start = '%s'"" % (datetime.strftime(datetime.today(),'%Y-%m-%d %H:%M:%S'),round(il_godzin,3),il_godzin, datetime.strftime(self.czas_start,'%Y-%m-%d %H:%M:%S'))
                        print str
                        tbl_piec_stop.execute(str)

                        tbl_piec_start = conn.cursor()
                        self.czas_start = datetime.today()
                        str = '''INSERT INTO piec VALUES('%s', '%s','0000-00-00 00:00:00',0,%s,%s,%s,%s,0,%s)''' % (zrodlo,datetime.strftime(self.czas_start,'%Y-%m-%d %H:%M:%S'), poziom, self.moc, self.taryfa_nr, self.taryfa_pln, self.taryfa_okno)
                        print str
                        tbl_piec_start.execute(str)

                    conn.commit()

                self.poziom = poziom
                """

        def off(self, zrodlo, temp_pieca, okno_start, okno_stop, temp_co_cwu, histereza_co_cwu):

            wylacz_wszystkie_grzalki = False

            if self.podgrzewam_CWU is True:
                if zrodlo == 'CWU':
                    # print "######################  wyłaczam podgrzewanie pieca dla CWU"

                    logging.info("[PIEC][CWU] - Wyłączono grzanie. Okno: %s - %s. Okres grzewczy: %s. Temp zbiornika: %s. Temp zadana: %s. Histereza: +/- %s." % (
                                    okno_start, okno_stop, self.par.okresgrzewczy, temp_pieca, temp_co_cwu, histereza_co_cwu))
                    print "[PIEC][CWU] - Wyłączono grzanie. Okno: %s - %s. Okres grzewczy: %s. Temp zbiornika: %s. Temp zadana: %s. Histereza: +/- %s." % (
                                    okno_start, okno_stop, self.par.okresgrzewczy, temp_pieca, temp_co_cwu, histereza_co_cwu)

                    self.podgrzewam_CWU = False
                    wylacz_wszystkie_grzalki = True

            if self.podgrzewam_CO is True:
                if zrodlo == 'CO':
                    logging.info("[PIEC][CO] - Wyłączono grzanie na poziomie. Okno: %s - %s. Okres grzewczy: %s. Temp zbiornika: %s. Temp zadana: %s. Histereza: +/- %s." % (
                                    okno_start, okno_stop, self.par.okresgrzewczy, temp_pieca, temp_co_cwu, histereza_co_cwu))
                    print "[PIEC][CO] - Wyłączono grzanie na poziomie. Okno: %s - %s. Okres grzewczy: %s. Temp zbiornika: %s. Temp zadana: %s. Histereza: +/- %s." % (
                                    okno_start, okno_stop, self.par.okresgrzewczy, temp_pieca, temp_co_cwu, histereza_co_cwu)
                    self.podgrzewam_CO = False
                    wylacz_wszystkie_grzalki = True


            if wylacz_wszystkie_grzalki is True:
                st_grzalka_1 = Stycznik(self.par.st_grzalka_1)
                st_grzalka_2 = Stycznik(self.par.st_grzalka_2)
                st_grzalka_3 = Stycznik(self.par.st_grzalka_3)

                st_grzalka_1.off()
                st_grzalka_2.off()
                st_grzalka_3.off()

                self.moc = 0
                self.poziom = 0

                # logging.info("[PIEC] - Wyłączono piec dla ogrzewania %s." % zrodlo)
                #print ("[PIEC][%s] - Wyłączono piec." % (zrodlo, zrodlo))

                # conn.open
                """
                conn.begin()

                tbl_piec_stop = conn.cursor()
                il_godzin1 = datetime.today()-self.czas_start
                il_godzin = round(il_godzin1.total_seconds()/60/60,4)

                str = ""UPDATE piec SET piec_czas_stop = '%s', piec_il_godzin = '%s', piec_taryfa_wartosc = ROUND (piec_moc * piec_taryfa_pln * '%s',2) WHERE piec_czas_start = '%s'"" % (datetime.strftime(datetime.today(),'%Y-%m-%d %H:%M:%S'), round(il_godzin,3), il_godzin, datetime.strftime(self.czas_start,'%Y-%m-%d %H:%M:%S'))
                print str
                tbl_piec_stop.execute(str)
                # print u"Piec wyłączony"
                conn.commit()
                """
                return True             # zwróć prawdę jeżeli wyłączono

        def zwieksz_moc (self, zrodlo):

            akt_poziom = self.poziom
            akt_moc = self.moc

            if self.poziom == 0:
                self.on(zrodlo, 1)
                self.moc = 3
            elif self.poziom == 1:
                self.on(zrodlo, 2)
                self.moc = 6
            elif self.poziom == 2:
                self.on(zrodlo, 3)
                self.moc = 9
            elif self.poziom == 3:
                self.on(zrodlo, 4)
                self.moc = 12
            elif self.poziom == 4:
                self.on(zrodlo, 5)
                self.moc = 15
            elif self.poziom == 5:
                self.on(zrodlo, 6)
                self.moc = 18

            if akt_poziom < 6:
                logging.info("[PIEC][%s] - Zwiększono poziom z %s na %s (z %s kW na %s kW)" % (zrodlo, akt_poziom, self.poziom, akt_moc, self.moc))
            else:
                logging.info("[PIEC][%s] - Nie można już zwiększyć poziomu pracy pieca" % zrodlo)
                pass

        def zmniejsz_moc (self, zrodlo):

            akt_poziom = self.poziom
            akt_moc = self.moc

            if self.poziom == 0:
                pass
            elif self.poziom == 1:
                self.off()
            elif self.poziom == 2:
                self.on(zrodlo,1)
            elif self.poziom == 3:
                self.on(zrodlo, 2)
            elif self.poziom == 4:
                self.on(zrodlo, 3)
            elif self.poziom == 5:
                self.on(zrodlo, 4)
            elif self.poziom == 6:
                self.on(zrodlo,5)


            if akt_poziom >= 2 and akt_poziom <= 6:
                logging.info("[PIEC][%s] - Zmniejszam poziom z %s na %s (z %s kW na %s kW)" % (zrodlo, akt_poziom, self.poziom, akt_moc, self.moc))
            else:
                logging.info("[PIEC][%s] - Nie można już zmniejszyć poziomu grzania" % zrodlo)

        def status (self):
            if self.poziom != 0 and self.poziom != None:
                return True
            else:
                return False
            # print "Piec działa na %s kW" % (self.moc)
            # logging.info("[PIEC] - Piec działa na poziomie %s z mocą %s kW" %(self.poziom, self.moc))

        def taryfa2(self):

            dzien = {0: 'NI', 1: 'PO', 2: 'WT', 3: 'SR', 4: 'CZ', 5: 'PI', 6: 'SO'}

            # nt = aktualny czas = nowtime
            czas = time.localtime()
            czas = time.strftime("%H:%M", czas)

            # ndow = NowDayOfWeek = aktualny dzien tygodnia
            dtyg1 = time.localtime()
            dtyg2 = time.strftime("%w", dtyg1)
            dt = dzien[int(dtyg2)]

            if dt in self.par.taryfa2_1_dni and czas  >= self.par.taryfa2_1_godz_start and czas < self.par.taryfa2_1_godz_stop:
                self.taryfa_nr = 2
                self.taryfa_okno = 1
                self.taryfa_pln = self.par.taryfa2_cena

            elif dt in self.par.taryfa2_2_dni and czas  >= self.par.taryfa2_2_godz_start and czas < self.par.taryfa2_2_godz_stop:
                self.taryfa_nr = 2
                self.taryfa_okno = 2
                self.taryfa_pln = self.par.taryfa2_cena

            elif dt in self.par.taryfa2_3_dni and czas  >= self.par.taryfa2_3_godz_start and czas < self.par.taryfa2_3_godz_stop:
                self.taryfa_nr = 2
                self.taryfa_okno = 3
                self.taryfa_pln = self.par.taryfa2_cena

            elif dt in self.par.taryfa2_4_dni and czas  >= self.par.taryfa2_4_godz_start and czas < self.par.taryfa2_4_godz_stop:
                self.taryfa_nr = 2
                self.taryfa_okno = 4
                self.taryfa_pln = self.par.taryfa2_cena

            elif dt in self.par.taryfa2_5_dni and czas  >= self.par.taryfa2_5_godz_start and czas < self.par.taryfa2_5_godz_stop:
                self.taryfa_nr = 2
                self.taryfa_okno = 5
                self.taryfa_pln = self.par.taryfa2_cena

            elif dt in self.par.taryfa2_6_dni and czas  >= self.par.taryfa2_6_godz_start and czas < self.par.taryfa2_6_godz_stop:
                self.taryfa_nr = 2
                self.taryfa_okno = 6
                self.taryfa_pln = self.par.taryfa2_cena

            else:
                self.taryfa_nr = 1
                self.taryfa_okno = 0
                self.taryfa_pln = self.par.taryfa1_cena

class Log():
    def __init__(self):
        self.par = Parametry()
        self.log = logging

        self.log.basicConfig(filename='PiConnect.log', level=self.par.log_loginglevel, format='%(levelname)s: %(asctime)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S %a', filemode='w')
        # self.log.info("[LOG] - Ustawiono poziom logowania: LoggingLevel = %s" % self.par.log_loginglevel)

    def debug(self, text, modul = 'XXX'):
        str = '[%s] - %s' % (modul,text)
        self.log.debug(str)
        print '[DEBUG]' + str

    def info(self, text, modul = 'XXX'):
        str = '[%s] - %s' % (modul,text)
        self.log.info(str)
        print '[INFO]' + str

    def error(self, text, modul = 'XXX'):
        str = '[%s] - %s' % (modul,text)
        self.log.error(str)
        print '[ERROR]' + str

    def warning(self, text, modul = 'XXX'):
        str = '[%s] - %s' % (modul,text)
        self.log.warning(str)
        print '[WARNING]' + str

class Temp():
    def __init__(self):
        self.par = Parametry()

        self.czuj_zew = self.read(self.par.czuj_zew)
        self.czuj_co_zas = self.read(self.par.czuj_co_zas)
        self.czuj_co_return = self.read(self.par.czuj_co_return)
        self.czuj_buf_top = self.read(self.par.czuj_buf_top)
        self.czuj_buf_mid = self.read(self.par.czuj_buf_mid)
        self.czuj_buf_low = self.read(self.par.czuj_buf_low)
        self.czuj_wew_01 = self.read(self.par.czuj_wew_01)
        self.czuj_wew_02 = self.read(self.par.czuj_wew_02)
        self.czuj_wew_03 = self.read(self.par.czuj_wew_03)
        self.czuj_wew_04 = self.read(self.par.czuj_wew_04)
        self.czuj_wew_05 = self.read(self.par.czuj_wew_05)
        self.czuj_wew_06 = self.read(self.par.czuj_wew_06)
        self.czuj_wew_07 = self.read(self.par.czuj_wew_07)
        self.czuj_wew_08 = self.read(self.par.czuj_wew_08)
        self.czuj_wew_09 = self.read(self.par.czuj_wew_09)
        self.czuj_wew_10 = self.read(self.par.czuj_wew_10)
        self.czuj_cwu = self.read(self.par.czuj_cwu)
        self.czuj_cwu_cyr = self.read(self.par.czuj_cwu_cyr)


    def read(self, czujnik):
        # Odczyt temperatury z czujnika o ID
        # device = DS18B20(czujnik)
        # return float(device.getCelsius())
        t = 21
        return t


    def read_all(self):

        self.czuj_zew = self.read(self.par.czuj_zew)
        self.czuj_co_zas = self.read(self.par.czuj_co_zas)
        self.czuj_co_return = self.read(self.par.czuj_co_return)
        self.czuj_buf_top = self.read(self.par.czuj_buf_top)
        self.czuj_buf_mid = self.read(self.par.czuj_buf_mid)
        self.czuj_buf_low = self.read(self.par.czuj_buf_low)
        self.czuj_wew_01 = self.read(self.par.czuj_wew_01)
        self.czuj_wew_02 = self.read(self.par.czuj_wew_02)
        self.czuj_wew_03 = self.read(self.par.czuj_wew_03)
        self.czuj_wew_04 = self.read(self.par.czuj_wew_04)
        self.czuj_wew_05 = self.read(self.par.czuj_wew_05)
        self.czuj_wew_06 = self.read(self.par.czuj_wew_06)
        self.czuj_wew_07 = self.read(self.par.czuj_wew_07)
        self.czuj_wew_08 = self.read(self.par.czuj_wew_08)
        self.czuj_wew_09 = self.read(self.par.czuj_wew_09)
        self.czuj_wew_10 = self.read(self.par.czuj_wew_10)
        self.czuj_cwu = self.read(self.par.czuj_cwu)
        self.czuj_cwu_cyr = self.read(self.par.czuj_cwu_cyr)

class cwu_okno():

    def __init__(self):
        self.par = Parametry()


        self.status = False
        self.okno = None
        self.okno_start = None
        self.okno_stop = None
        self.temp = 0
        self.histereza = 0
        pass

    def __call__(self, *args, **kwargs):
        dzien = {0: 'NI', 1: 'PO', 2: 'WT', 3: 'SR', 4: 'CZ', 5: 'PI', 6: 'SO'}

        # nt = aktualny czas = nowtime
        czas = time.localtime()
        czas = time.strftime("%H:%M", czas)

        # ndow = NowDayOfWeek = aktualny dzien tygodnia
        dtyg1 = time.localtime()
        dtyg2 = time.strftime("%w", dtyg1)
        dt = dzien[int(dtyg2)]

        if dt in self.par.cwu_okno_1_days and czas  >= self.par.cwu_okno_1_start and czas <= self.par.cwu_okno_1_stop:
            self.status = True
            self.okno = 1
            self.okno_start = self.par.cwu_okno_1_start
            self.okno_stop = self.par.cwu_okno_1_stop
            self.temp = self.par.cwu_okno_1_temp
            self.histereza = self.par.cwu_okno_1_hist

            #return (True,1,par['cwu_okno_1_start'],par['cwu_okno_1_stop'],par['cwu_okno_1_temp'])
        elif dt in self.par.cwu_okno_2_days and czas  >= self.par.cwu_okno_2_start and czas <= self.par.cwu_okno_2_stop:
            self.status = True
            self.okno = 2
            self.okno_start = self.par.cwu_okno_2_start
            self.okno_stop = self.par.cwu_okno_2_stop
            self.temp = self.par.cwu_okno_2_temp
            self.histereza = self.par.cwu_okno_2_hist
            #return (True,2,par['cwu_okno_2_start'],par['cwu_okno_2_stop'],par['cwu_okno_2_temp'])

        elif dt in self.par.cwu_okno_3_days and czas  >= self.par.cwu_okno_3_start and czas <= self.par.cwu_okno_3_stop:
            self.status = True
            self.okno = 3
            self.okno_start = self.par.cwu_okno_3_start
            self.okno_stop = self.par.cwu_okno_3_stop
            self.temp = self.par.cwu_okno_3_temp
            self.histereza = self.par.cwu_okno_3_hist

            # return (True,3,par['cwu_okno_3_start'],par['cwu_okno_3_stop'],par['cwu_okno_3_temp'])
        elif dt in self.par.cwu_okno_4_days and czas  >= self.par.cwu_okno_4_start and czas <= self.par.cwu_okno_4_stop:
            self.status = True
            self.okno = 4
            self.okno_start = self.par.cwu_okno_4_start
            self.okno_stop = self.par.cwu_okno_4_stop
            self.temp = self.par.cwu_okno_4_temp
            self.histereza = self.par.cwu_okno_4_hist

            # return (True,4,par['cwu_okno_4_start'],par['cwu_okno_4_stop'],par['cwu_okno_4_temp'])
        elif dt in self.par.cwu_okno_5_days and czas  >= self.par.cwu_okno_5_start and czas <= self.par.cwu_okno_5_stop:
            self.status = True
            self.okno = 5
            self.okno_start = self.par.cwu_okno_5_start
            self.okno_stop = self.par.cwu_okno_5_stop
            self.temp = self.par.cwu_okno_5_temp
            self.histereza = self.par.cwu_okno_5_hist

            # return (True,5,par['cwu_okno_5_start'],par['cwu_okno_5_stop'],par['cwu_okno_5_temp'])
        elif dt in self.par.cwu_okno_6_days and czas  >= self.par.cwu_okno_6_start and czas <= self.par.cwu_okno_6_stop:
            self.status = True
            self.okno = 6
            self.okno_start = self.par.cwu_okno_6_start
            self.okno_stop = self.par.cwu_okno_6_stop
            self.temp = self.par.cwu_okno_6_temp
            self.histereza = self.par.cwu_okno_6_hist

            # return (True,6,par['cwu_okno_6_start,par['cwu_okno_6_stop'],par['cwu_okno_6_temp'])
        else:
            self.status = False
            self.okno = None
            self.okno_start = None
            self.okno_stop = None
            self.temp = None
            self.histereza = 0

            # return (False)

class co_okno():
    def __init__(self):

        self.par = Parametry()


        self.status = False
        self.okno = None
        self.okno_start = None
        self.okno_stop = None
        self.temp = None
        self.histereza = None
        pass

    def __call__(self, *args, **kwargs):
        dzien = {0: 'NI', 1: 'PO', 2: 'WT', 3: 'SR', 4: 'CZ', 5: 'PI', 6: 'SO'}

        # nt = aktualny czas = nowtime
        czas = time.localtime()
        czas = time.strftime("%H:%M", czas)

        # ndow = NowDayOfWeek = aktualny dzien tygodnia
        dtyg1 = time.localtime()
        dtyg2 = time.strftime("%w", dtyg1)
        dt = dzien[int(dtyg2)]

        if dt in self.par.co_okno_1_days and czas  >= self.par.co_okno_1_start and czas <= self.par.co_okno_1_stop:
            self.status = True
            self.okno = 1
            self.okno_start = self.par.co_okno_1_start
            self.okno_stop = self.par.co_okno_1_stop
            self.temp = self.par.co_okno_1_temp
            self.histereza = self.par.co_okno_1_hist

            #return (True,1,par['co_okno_1_start,par['co_okno_1_stop,par['co_okno_1_temp)
        elif dt in self.par.co_okno_2_days and czas  >= self.par.co_okno_2_start and czas <= self.par.co_okno_2_stop:
            self.status = True
            self.okno = 2
            self.okno_start = self.par.co_okno_2_start
            self.okno_stop = self.par.co_okno_2_stop
            self.temp = self.par.co_okno_2_temp
            self.histereza = self.par.co_okno_2_hist

            #return (True,2,par['co_okno_2_start,par['co_okno_2_stop,par['co_okno_2_temp)
        elif dt in self.par.co_okno_3_days and czas  >= self.par.co_okno_3_start and czas <= self.par.co_okno_3_stop:
            self.status = True
            self.okno = 3
            self.okno_start = self.par.co_okno_3_start
            self.okno_stop = self.par.co_okno_3_stop
            self.temp = self.par.co_okno_3_temp
            self.histereza = self.par.co_okno_3_hist

            # return (True,3,par['co_okno_3_start,par['co_okno_3_stop,par['co_okno_3_temp)
        elif dt in self.par.co_okno_4_days and czas  >= self.par.co_okno_4_start and czas <= self.par.co_okno_4_stop:
            self.status = True
            self.okno = 4
            self.okno_start = self.par.co_okno_4_start
            self.okno_stop = self.par.co_okno_4_stop
            self.temp = self.par.co_okno_4_temp
            self.histereza = self.par.co_okno_4_hist

            # return (True,4,par['co_okno_4_start,par['co_okno_4_stop,par['co_okno_4_temp)
        elif dt in self.par.co_okno_5_days and czas  >= self.par.co_okno_5_start and czas <= self.par.co_okno_5_stop:
            self.status = True
            self.okno = 5
            self.okno_start = self.par.co_okno_5_start
            self.okno_stop = self.par.co_okno_5_stop
            self.temp = self.par.co_okno_5_temp
            self.histereza = self.par.co_okno_5_hist

            # return (True,5,par['co_okno_5_start,par['co_okno_5_stop,par['co_okno_5_temp)
        elif dt in self.par.co_okno_6_days and czas  >= self.par.co_okno_6_start and czas <= self.par.co_okno_6_stop:
            self.status = True
            self.okno = 6
            self.okno_start = self.par.co_okno_6_start
            self.okno_stop = self.par.co_okno_6_stop
            self.temp = self.par.co_okno_6_temp
            self.histereza = self.par.co_okno_6_hist

            # return (True,6,par['co_okno_6_start,par['co_okno_6_stop,par['co_okno_6_temp)
        else:
            self.status = False
            self.okno = None
            self.okno_start = None
            self.okno_stop = None
            self.temp = None
            self.histereza = None









class Zawor_Trojdrogowy():
    def __init__(self):
        pass
        self.temp_zasilania_zadana = 21

class Pompa_CO():

    def __init__(self, piec_temp = 0):
        self.par = Parametry()
        self.par.read_all()
        self.temp = Temp()
        self.zaw_troj = Zawor_Trojdrogowy()
        self.log = Log()


        self.stycz_pompa = Stycznik(self.par.st_co_pompa)

        self.wlaczona = False
        self.print_blokada_pompy_CO = False

    def sprawdz_czy_wlaczyc(self, temp_zasilania):

        if self.temp.czuj_buf_mid >= temp_zasilania:    # jeżeli temperatura zbiornika jest wyższa od żądanej temp zasilania CO

            if (self.par.pom1_temp - self.par.pom1_hist) > self.temp.czuj_wew_01:

                if self.wlaczona == False:
                    self.log.info("Włączam pompę CO. Temperatura pomieszczenia %s jest mniejsza od temp. zadanej %s" % (self.temp.czuj_wew_01, self.par.pom1_temp),'CO POMPA')
                    self.on()

                if self.wlaczona == True:
                    self.log.info("Wyłączam pompę CO. Temperatura pomieszczenia %s jest większa od temp. zadanej %s" % (self.temp.czuj_wew_01, self.par.pom1_temp), 'CO POMPA')
                    self.off()

            else:
                if self.wlaczona == True:
                    self.log.info("Wyłączam pompę CO. Temperatura pomieszczenia %s jest większa od temp. zadanej %s" % (self.temp.czuj_wew_01, self.par.pom1_temp), 'CO POMPA')
                    self.off()

            self.print_blokada_pompy_CO = False
        else:                                           # jeżeli temperatura zbiornika jest NIZSZA od żądanej temp zasilania CO

            if self.print_blokada_pompy_CO == False:
                self.log.info("Nie mogę włączyć pompy CO. Temperatura bufora %s jest za niska by uzyskać temp. zasilania %s" % (temp.czuj_buf_mid, self.temp_zasilania),'CO POMPA')
                self.print_blokada_pompy_CO = True

            self.off()

    def on(self):
        #self.on
        if self.wlaczona ==False:
            self.stycz_pompa.on()
            self.log.info("Pompa CO została włączona",'CO POMPA')


        self.wlaczona = True

    def off(self):
        #self.off
        if self.wlaczona == True:
            self.stycz_pompa.off()
            self.log.info("Pompa CO została wyłączona",'CO POMPA')


        self.wlaczona = False

class Pomieszczenia():
    def __init__(self):
        pass

def setup():
    ##################### POCZĄTEK SETUP() ########################
    log = Log()

    par = Parametry()
    par.read_all()


    sty = Stycznik()
    sty.reset_all()

    # TODO: DELETE: db = DB()
    # TODO: DELETE: db.db_init()


    ##################### KONIEC SETUP() ########################




def loop():

    par = Parametry()
    temp = Temp()
    temp.read_all()
    db = DB()
    piec = Piec()
    cwu = cwu_okno()
    co = co_okno()
    pompa_co = Pompa_CO()
    zaw = Zawor_Trojdrogowy()

    pompa_CO = Pompa_CO(temp.czuj_buf_mid)



    licznik_db = 1      # licznik dla zapisu temperatur do db
    licznik_tmp = 1     # licznik dla odczytu temperatur
    licznik_par = 1     # licznik dla automatycznego ponownego odczytu parametrów (ustawione na sztywno co godzinę)

    petla = True         # wyrzucić w Rpi

    while petla is True:

        if licznik_par % 1 == 0:         # ponowny, cykliczny odczyt parametrów z pliku konfiguracyjnego co godzinę
            # Odczyt temperatur
            par = Parametry()
            par.read_all()

            licznik_par = 0

        cwu.__call__()
        co.__call__()


        # print "#### Okres grzewczy = ",self.par.okresgrzewczy
        # print "#### Oknco CWU = ", cwu.status
        # print "#### Piec - poziom = ", piec.poziom
        # TODO: histereza temperatury pieca

        # # # # # # #   G Ł Ó W N A          P Ę T L A              P I E C A  -  start

        if par.okresgrzewczy is False:       # jeżeli okres grzewczy=Nie to grzejemy tylko piec na potrzeby CWU

            if piec.podgrzewam_CWU is False:
                if cwu.status is True:              # jeżeli jest okno CWU

                    if temp.czuj_buf_mid  <=  cwu.temp - cwu.histereza/2:  # jeżeli temperatura w środku BUFORA jest niższa od zadanej
                        #logging.info ("[CWU] - Włączam ogrzewnie CWU. Przycyzna: temp bufora %s < %s. Okres grzewczy: %s. Okno: %s -> %s." % (temp.czuj_buf_mid, cwu.temp - cwu.histereza/2, self.par.okresgrzewczy, cwu.okno_start, cwu.okno_stop))
                        #print "[CWU] - Włączam ogrzewnie CWU. Przycyzna: temp bufora %s < %s. Okres grzewczy: %s. Okno: %s -> %s." % (temp.czuj_buf_mid, cwu.temp - cwu.histereza/2, self.par.okresgrzewczy, cwu.okno_start, cwu.okno_stop)
                        piec.on('CWU',temp.czuj_buf_mid, cwu.okno_start, cwu.okno_stop, cwu.temp, cwu.histereza, 1)

                    if temp.czuj_buf_mid  > cwu.temp + cwu.histereza/2:  # jeżeli temperatura w środku BUFORA jest wyższa od zadanej
                        #logging.info ("[CWU] - Wyłączam ogrzewanie CWU. Przycyzna: temp bufora %s > %s. Okres grzewczy: %s. Okno: %s -> %s." % (temp.czuj_buf_mid, cwu.temp + cwu.histereza/2, self.par.okresgrzewczy, cwu.okno_start, cwu.okno_stop))
                        #print "[CWU] - Wyłączam ogrzewanie CWU. Przycyzna: temp bufora %s > %s. Okres grzewczy: %s. Okno: %s -> %s." % (temp.czuj_buf_mid, cwu.temp + cwu.histereza/2, self.par.okresgrzewczy, cwu.okno_start, cwu.okno_stop)
                        piec.off('CWU',temp.czuj_buf_mid,cwu.okno_start, cwu.okno_stop,cwu.temp, cwu.histereza)

                else:
                    if piec.status is True:
                        #logging.info ("[CWU] - Wyłączam ogrzewanie CWU. Przycyzna: koniec okna nr %s. Okres grzewczy: %s. Okno: %s -> %s." % (cwu.okno, self.par.okresgrzewczy, cwu.okno_start, cwu.okno_stop))
                        piec.off('CWU',temp.czuj_buf_mid,cwu.okno_start, cwu.okno_stop,cwu.temp, cwu.histereza)

        elif par.okresgrzewczy is True:      # jeżeli okres grzewczy = Tak - trzeba skombinować okna i temperatury

            if cwu.status is True: # jeżeli jest okno CWU

                if temp.czuj_buf_mid  <=  cwu.temp - cwu.histereza/2:  # jeżeli temperatura w środku BUFORA jest niższa od zadanej
                    #logging.info ("[CWU] - Włączam ogrzewnie CWU. Przycyzna: temp bufora %s < %s. Okres grzewczy: %s. Okno: %s -> %s." % (temp.czuj_buf_mid, cwu.temp - cwu.histereza/2, self.par.okresgrzewczy, cwu.okno_start, cwu.okno_stop))
                    #print "[CWU] - Włączam ogrzewnie CWU. Przycyzna: temp bufora %s < %s. Okres grzewczy: %s. Okno: %s -> %s." % (temp.czuj_buf_mid, cwu.temp - cwu.histereza/2, self.par.okresgrzewczy, cwu.okno_start, cwu.okno_stop)
                    piec.on('CWU',temp.czuj_buf_mid, cwu.okno_start, cwu.okno_stop, cwu.temp, cwu.histereza, 1)

                if temp.czuj_buf_mid  > cwu.temp + cwu.histereza/2:  # jeżeli temperatura w środku BUFORA jest wyższa od zadanej
                    #logging.info ("[CWU] - Wyłączam ogrzewanie CWU. Przycyzna: temp bufora %s > %s. Okres grzewczy: %s. Okno: %s -> %s." % (temp.czuj_buf_mid, cwu.temp + cwu.histereza/2, self.par.okresgrzewczy, cwu.okno_start, cwu.okno_stop))
                    #print "[CWU] - Wyłączam ogrzewanie CWU. Przycyzna: temp bufora %s > %s. Okres grzewczy: %s. Okno: %s -> %s." % (temp.czuj_buf_mid, cwu.temp + cwu.histereza/2, self.par.okresgrzewczy, cwu.okno_start, cwu.okno_stop)
                    piec.off('CWU',temp.czuj_buf_mid,cwu.okno_start, cwu.okno_stop,cwu.temp, cwu.histereza)

            if cwu.status is False and piec.podgrzewam_CWU is True:
                if piec.status() is True:
                    #logging.info ("[CWU] - Wyłączam ogrzewanie CWU. Przycyzna: koniec okna nr %s. Okres grzewczy: %s. Okno: %s -> %s." % (cwu.okno, self.par.okresgrzewczy, cwu.okno_start, cwu.okno_stop))
                    #print "[CWU] - Wyłączam ogrzewanie CWU. Przycyzna: koniec okna nr %s. Okres grzewczy: %s. Okno: %s -> %s." % (cwu.okno, self.par.okresgrzewczy, cwu.okno_start, cwu.okno_stop)
                    piec.off('CWU',temp.czuj_buf_mid,cwu.okno_start, cwu.okno_stop,cwu.temp, cwu.histereza)

            if piec.podgrzewam_CWU is False:
                if co.status is True:        # jeżeli jest okno CO
                    if temp.czuj_buf_mid  <=  co.temp - co.histereza/2:  # jeżeli temperatura w środku BUFORA jest niższa od zadanej
                        #logging.info ("[CO] - Włączam ogrzewnie CO. Przycyzna: temp bufora %s < %s. Okres grzewczy: %s. Okno: %s -> %s." % (temp.czuj_buf_mid, co.temp - co.histereza/2, self.par.okresgrzewczy, co.okno_start, co.okno_stop))
                        #print "[CO] - Włączam ogrzewnie CO. Przycyzna: temp bufora %s < %s. Okres grzewczy: %s. Okno: %s -> %s." % (temp.czuj_buf_mid, co.temp - co.histereza/2, self.par.okresgrzewczy, co.okno_start, co.okno_stop)
                        piec.on('CO',temp.czuj_buf_mid, co.okno_start, co.okno_stop, co.temp, co.histereza)

                    if temp.czuj_buf_mid  > co.temp + co.histereza/2:  # jeżeli temperatura w środku BUFORA jest wyższa od zadanej
                        #logging.info ("[CO] - Wyłączam ogrzewanie CO. Przycyzna: temp bufora %s > %s. Okres grzewczy: %s. Okno: %s -> %s." % (temp.czuj_buf_mid, co.temp + co.histereza/2, self.par.okresgrzewczy, co.okno_start, co.okno_stop))
                        #print "[CO] - Wyłączam ogrzewanie CO. Przycyzna: temp bufora %s > %s. Okres grzewczy: %s. Okno: %s -> %s." % (temp.czuj_buf_mid, co.temp + co.histereza/2, self.par.okresgrzewczy, co.okno_start, co.okno_stop)
                        piec.off('CO',temp.czuj_buf_mid,co.okno_start, co.okno_stop, co.temp, co.histereza)

            if co.status is False and piec.podgrzewam_CO is True:
                if piec.status is True:
                    #logging.info ("[CO] - Wyłączam ogrzewanie CO. Przycyzna: koniec okna nr %s. Okres grzewczy: %s. Okno: %s -> %s." % (co.okno, self.par.okresgrzewczy, co.okno_start, co.okno_stop))
                    #print "[CO] - Wyłączam ogrzewanie CO. Przycyzna: koniec okna nr %s. Okres grzewczy: %s. Okno: %s -> %s." % (co.okno, self.par.okresgrzewczy, co.okno_start, co.okno_stop)
                    piec.off('CO',temp.czuj_buf_mid,co.okno_start, co.okno_stop, co.temp, co.histereza)

        ######## P I E C A    - stop      # # # # # # #   G Ł Ó W N A          P Ę T L A





        if licznik_tmp % par.temp_timeinterval == 0:
            # Odczyt temperatur
            par.read_all()
            temp.read_all()
            licznik_tmp = 0
            # piec.zwieksz_moc('CWU')

        if licznik_db % par.db_timeinterval == 0:

            #print 'Zapisanano do bazy danych: %s' % licznik_db
            db.zapis_temp()
            licznik_db = 0


        pompa_co.sprawdz_czy_wlaczyc(zaw.temp_zasilania_zadana)



        time.sleep(1)
        licznik_db = licznik_db +1
        licznik_tmp = licznik_tmp + 1
        licznik_par = licznik_par + 1


    ############################### KONIEC LOOP #####################################



setup()


loop()


"""
def destroy():
    ########################################################################################################################
    # Zerowanie przekaznikow
    ########################################################################################################################
    gpio = webiopi.GPIO  # Helper for LOW/HIGH values
    #gpio.setFunction(stycznik_blokada_grzania, gpio.OUT)
    gpio.digitalWrite(stycznik_blokada_grzania, gpio.LOW)
    logging.info("PiConnect zostal zamkniety")
    conn.close

    """