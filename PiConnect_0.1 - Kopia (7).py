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
    conf = ConfigParser.RawConfigParser()
    conf.read("PiConnect.conf")

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
        'pom1_hist': float(conf.get('Pomieszczenia', 'pom1_hist')),
        'pom1_nazwa' : conf.get('Pomieszczenia', 'pom1_nazwa')
        }

    def __init__(self):
        pass

    def read_all(self):

        conf = ConfigParser.RawConfigParser()
        conf.read("PiConnect.conf")

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
            'pom1_hist': float(conf.get('Pomieszczenia', 'pom1_hist')),
            'pom1_nazwa' : conf.get('Pomieszczenia', 'pom1_nazwa')
            }

        logging.basicConfig(filename='PiConnect.log', level='DEBUG', format='%(levelname)s: %(asctime)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S %a', filemode = 'w')

        for (char,n) in sorted(par.items()):
            # Log().debug ("[CONF] - Odczytano z pliku konfiguracyjnego parametr: %s = %s" % (char, n), 'PARAMETRY')
            pass

        return par

class Stycznik():

    def __init__(self, stycz = None):

        self.stycz = stycz

        self.wlaczony = False

    def on(self):
        # Rpi: gpio.digitalWrite(stycz, gpio.HIGH)
        if self.wlaczony == False:
            Log().debug("Stycznik nr %s został włączony" % self.stycz, 'STYCZNIK')
        self.wlaczony = True

    def off (self):
        # Rpi: gpio.digitalWrite(stycz, gpio.LOW)
        if self.wlaczony == True:
            Log().debug("Stycznik nr %s został włączony" % self.stycz, 'STYCZNIK')
        self.wlaczony = False

    def reset_all(self):
        # Rpi: gpio = webiopi.GPIO


        if par['st_taryfa'] not in ['0'," ",""]:
            # Rpi: gpio.setFunction(par['st_taryfa'], gpio.OUT)
            # Rpi: gpio.digitalWrite(par['st_taryfa'], gpio.LOW)
            # print "Reset stycznika nr %s: st_taryfa" % par['st_taryfa']
            pass

        if par['st_co_pompa'] not in ['0'," ",""]:
            # Rpi: gpio.setFunction(par['st_co_pompa'], gpio.OUT)
            # Rpi: gpio.digitalWrite(par['st_co_pompa'], gpio.LOW)
            # print "Reset stycznika nr %s: st_co_pompa" % par['st_co_pompa']
            pass

        if par['st_co_zawor_otw'] not in ['0'," ",""]:
            # Rpi: gpio.setFunction(par['st_co_zawor_otw'], gpio.OUT)
            # Rpi: gpio.digitalWrite(par['st_co_zawor_otw'], gpio.LOW)
            # pr    int "Reset stycznika nr %s: st_co_zawor_otw" % par['st_co_zawor_otw']
            pass

        if par['st_co_zawor_zam'] not in ['0'," ",""]:
            # Rpi: gpio.setFunction(par['st_co_zawor_zam'], gpio.OUT)
            # Rpi: gpio.digitalWrite(par['st_co_zawor_zam'], gpio.LOW)
            #print "Reset stycznika nr %s: st_co_zawor_zam" % par['st_co_zawor_zam']
            pass

        if par['st_grzalka_1'] not in ['0'," ",""]:
            # Rpi: gpio.setFunction(par['st_grzalka_1'], gpio.OUT)
            # Rpi: gpio.digitalWrite(par['st_grzalka_1'], gpio.LOW)
            #print "Reset stycznika nr %s: st_grzalka_1" % par['st_grzalka_1']
            pass

        if par['st_grzalka_2'] not in ['0'," ",""]:
            # Rpi: gpio.setFunction(par['st_grzalka_2'], gpio.OUT)
            # Rpi: gpio.digitalWrite(par['st_grzalka_2'], gpio.LOW)
            #print "Reset stycznika nr %s: st_grzalka_2" % par['st_grzalka_2']
            pass

        if par['st_grzalka_3'] not in ['0'," ",""]:
            # Rpi: gpio.setFunction(par['st_grzalka_3'], gpio.OUT)
            # Rpi: gpio.digitalWrite(par['st_grzalka_3'], gpio.LOW)
            #print "Reset stycznika nr %s: st_grzalka_3" % par['st_grzalka_3']
            pass

        if par['st_cwu_pompa_cyr'] not in ['0'," ",""]:
            # Rpi: gpio.setFunction(par['st_cwu_pompa_cyr'], gpio.OUT)
            # Rpi: gpio.digitalWrite(par['st_cwu_pompa_cyr'], gpio.LOW)
            #print "Reset stycznika nr %s: st_cwu_pompa_cyr" % par['st_cwu_pompa_cyr']
            pass
        Log().debug('Zresetowano konfigurację wszystkich styczników', 'STYCZNIK')

class DB(Parametry):


    def __init__(self):
        pass
        _conn = None
    def db_init(self):
        try:

            _conn = MySQLdb.connect(host=par['db_server'], user=par['db_username'], passwd=par['db_password'], db=par['db_name'])

        except:
            # TBD: check_SQL_connection()
            #	print 'Blad polaczenia z DB'
            Log.error('[DB] - Blad podlaczenia do bazy danych: host= %s, user=%s, passwd=%s, db=%s' %
                          (par['db_name'], par['db_username'], par['db_password'], par['db_name']), 'DB')

            pass

    def zapis_temp(self):

        temp = Temp()
        # Temp.read_all()

        # conn.open
        """
        self._conn.begin()

        tbl_temperatury = self._conn.cursor()

        sql = "" INSERT INTO temperatury VALUES ('%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "" % \
                            (datetime.strftime(datetime.today(),'%Y-%m-%d %H:%M:%S'),
                            Temp.czuj_zew,
                            Temp.czuj_co_zas,
                            Temp.czuj_co_return,
                            Temp.czuj_buf_top,
                            Temp.czuj_buf_mid,
                            Temp.czuj_buf_low,
                            Temp.czuj_wew_01,
                            Temp.czuj_wew_02,
                            Temp.czuj_wew_03,
                            Temp.czuj_wew_04,
                            Temp.czuj_wew_05,
                            Temp.czuj_wew_06,
                            Temp.czuj_wew_07,
                            Temp.czuj_wew_08,
                            Temp.czuj_wew_09,
                            Temp.czuj_wew_10,
                            Temp.czuj_cwu,
                            Temp.czuj_cwu_cyr,
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
    st_blokada_grzania = Stycznik(par['st_taryfa'])

    st_grzalka_1 = Stycznik(par['st_grzalka_1'])
    st_grzalka_2 = Stycznik(par['st_grzalka_2'])
    st_grzalka_3 = Stycznik(par['st_grzalka_3'])

    moc = 0
    taryfa_nr = 0
    poziom = 0
    podgrzewam_CWU = False            # Czy grzeje dla CWU?
    podgrzewam_CO = False             # Czy grzeje dla CO?

    def __init__(self):
        self.temp = Temp()
        self.st_blokada_grzania = Stycznik(par['st_taryfa'])

        self.st_grzalka_1 = Stycznik(par['st_grzalka_1'])
        self.st_grzalka_2 = Stycznik(par['st_grzalka_2'])
        self.st_grzalka_3 = Stycznik(par['st_grzalka_3'])

    def on (self, zrodlo, okno_start, okno_stop, temp_zadana, histereza_zadana,  poziom = 1):   # źródło = CWU, CO

        zmieniono = False

        tmp_podgrzewam_CO = self.podgrzewam_CO
        tmp_podgrzewam_CWU = self.podgrzewam_CWU

        self.taryfa2()

        # Wyłaczenie pieca CO jeżeli ma grzać SWU i na odwrót
        if zrodlo == 'CWU' and tmp_podgrzewam_CO is True:
            self.off('CO',self.temp.czuj_buf_mid,okno_start, okno_stop,temp_zadana, histereza_zadana)

        if zrodlo == 'CO' and tmp_podgrzewam_CWU is True:
            self.off('CWU', self.temp.czuj_buf_mid,okno_start, okno_stop,temp_zadana, histereza_zadana)

        # wyłacenie pieca jeżeli poziom ma ulec zmianie i piec działa
        if self.poziom > 0 and poziom <> self.poziom:
            self.off(zrodlo, self.temp.czuj_buf_mid,okno_start, okno_stop,temp_zadana, histereza_zadana)

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


            Log().debug("Włączono grzanie na poziomie %s z mocą %s kW. Okno: %s - %s. Okres grzewczy: %s. Temp zbiornika: %s. Temp zadana: %s. Histereza: +/- %s." % (
                                poziom, self.moc, okno_start, okno_stop, par['okresgrzewczy'], self.temp.czuj_buf_mid, temp_zadana, histereza_zadana), zrodlo)

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

    def off(self, zrodlo, temp_pieca, okno_start, okno_stop, temp_zadana, histereza_zadana):

        wylacz_wszystkie_grzalki = False

        if self.podgrzewam_CWU is True:
            if zrodlo == 'CWU':
                # print "######################  wyłaczam podgrzewanie pieca dla CWU"

                logging.debug("[PIEC][CWU] - Wyłączono grzanie. Okno: %s - %s. Okres grzewczy: %s. Temp zbiornika: %s. Temp zadana: %s. Histereza: +/- %s." % (
                                okno_start, okno_stop, par['okresgrzewczy'], temp_pieca, temp_zadana, histereza_zadana))
                print "[PIEC][CWU] - Wyłączono grzanie. Okno: %s - %s. Okres grzewczy: %s. Temp zbiornika: %s. Temp zadana: %s. Histereza: +/- %s." % (
                                okno_start, okno_stop, par['okresgrzewczy'], temp_pieca, temp_zadana, histereza_zadana)

                self.podgrzewam_CWU = False
                wylacz_wszystkie_grzalki = True

        if self.podgrzewam_CO is True:
            if zrodlo == 'CO':
                logging.debug("[PIEC][CO] - Wyłączono grzanie na poziomie. Okno: %s - %s. Okres grzewczy: %s. Temp zbiornika: %s. Temp zadana: %s. Histereza: +/- %s." % (
                                okno_start, okno_stop, par['okresgrzewczy'], temp_pieca, temp_zadana, histereza_zadana))
                print "[PIEC][CO] - Wyłączono grzanie na poziomie. Okno: %s - %s. Okres grzewczy: %s. Temp zbiornika: %s. Temp zadana: %s. Histereza: +/- %s." % (
                                okno_start, okno_stop, par['okresgrzewczy'], temp_pieca, temp_zadana, histereza_zadana)
                self.podgrzewam_CO = False
                wylacz_wszystkie_grzalki = True


        if wylacz_wszystkie_grzalki is True:
            st_grzalka_1 = Stycznik(par['st_grzalka_1'])
            st_grzalka_2 = Stycznik(par['st_grzalka_2'])
            st_grzalka_3 = Stycznik(par['st_grzalka_3'])

            st_grzalka_1.off()
            st_grzalka_2.off()
            st_grzalka_3.off()

            self.moc = 0
            self.poziom = 0

            # logging.debug("[PIEC] - Wyłączono piec dla ogrzewania %s." % zrodlo)
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
            logging.debug("[PIEC][%s] - Zwiększono poziom z %s na %s (z %s kW na %s kW)" % (zrodlo, akt_poziom, self.poziom, akt_moc, self.moc))
        else:
            logging.debug("[PIEC][%s] - Nie można już zwiększyć poziomu pracy pieca" % zrodlo)
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
            logging.debug("[PIEC][%s] - Zmniejszam poziom z %s na %s (z %s kW na %s kW)" % (zrodlo, akt_poziom, self.poziom, akt_moc, self.moc))
        else:
            logging.debug("[PIEC][%s] - Nie można już zmniejszyć poziomu grzania" % zrodlo)

    def status (self):
        if self.poziom != 0 and self.poziom != None:
            return True
        else:
            return False
        # print "Piec działa na %s kW" % (self.moc)
        # logging.debug("[PIEC] - Piec działa na poziomie %s z mocą %s kW" %(self.poziom, self.moc))

    def taryfa2(self):

        dzien = {0: 'NI', 1: 'PO', 2: 'WT', 3: 'SR', 4: 'CZ', 5: 'PI', 6: 'SO'}

        # nt = aktualny czas = nowtime
        czas = time.localtime()
        czas = time.strftime("%H:%M", czas)

        # ndow = NowDayOfWeek = aktualny dzien tygodnia
        dtyg1 = time.localtime()
        dtyg2 = time.strftime("%w", dtyg1)
        dt = dzien[int(dtyg2)]

        if dt in par['taryfa2_1_dni'] and czas  >= par['taryfa2_1_godz_start'] and czas < par['taryfa2_1_godz_stop']:
            self.taryfa_nr = 2
            self.taryfa_okno = 1
            self.taryfa_pln = par['taryfa2_cena']

        elif dt in par['taryfa2_2_dni'] and czas  >= par['taryfa2_2_godz_start'] and czas < par['taryfa2_2_godz_stop']:
            self.taryfa_nr = 2
            self.taryfa_okno = 2
            self.taryfa_pln = par['taryfa2_cena']

        elif dt in par['taryfa2_3_dni'] and czas  >= par['taryfa2_3_godz_start'] and czas < par['taryfa2_3_godz_stop']:
            self.taryfa_nr = 2
            self.taryfa_okno = 3
            self.taryfa_pln = par['taryfa2_cena']

        elif dt in par['taryfa2_4_dni'] and czas  >= par['taryfa2_4_godz_start'] and czas < par['taryfa2_4_godz_stop']:
            self.taryfa_nr = 2
            self.taryfa_okno = 4
            self.taryfa_pln = par['taryfa2_cena']

        elif dt in par['taryfa2_5_dni'] and czas  >= par['taryfa2_5_godz_start'] and czas < par['taryfa2_5_godz_stop']:
            self.taryfa_nr = 2
            self.taryfa_okno = 5
            self.taryfa_pln = par['taryfa2_cena']

        elif dt in par['taryfa2_6_dni'] and czas  >= par['taryfa2_6_godz_start'] and czas < par['taryfa2_6_godz_stop']:
            self.taryfa_nr = 2
            self.taryfa_okno = 6
            self.taryfa_pln = par['taryfa2_cena']

        else:
            self.taryfa_nr = 1
            self.taryfa_okno = 0
            self.taryfa_pln = par['taryfa1_cena']

class Log():
    #def __init__(self):

    logging.basicConfig(filename='PiConnect.log', level=par['log_loginglevel'], format='%(levelname)s: %(asctime)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S %a', filemode='w')
        # Log.debug("[LOG] - Ustawiono poziom logowania: LoggingLevel = %s" % par['log_loginglevel)

    def debug(self, text, modul = 'XXX'):
        s = '[%s] - %s' % (modul,text)
        logging.debug(s)
        print '[DEBUG]' + s

    def info(self, text, modul = 'XXX'):
        s = '[%s] - %s' % (modul,text)
        logging.debug(s)
        print '[INFO]' + s

    def error(self, text, modul = 'XXX'):
        s = '[%s] - %s' % (modul,text)
        logging.error(s)
        print '[ERROR]' + s

    def warning(self, text, modul = 'XXX'):
        s = '[%s] - %s' % (modul,text)
        logging.warning(s)
        print '[WARNING]' + s

class Temp(Parametry):

    czuj_zew = 0
    czuj_co_zas = 0
    czuj_co_return = 0
    czuj_buf_top = 0
    czuj_buf_mid = 0
    czuj_buf_low = 0
    czuj_wew_01 = 0
    czuj_wew_02 = 0
    czuj_wew_03 = 0
    czuj_wew_04 = 0
    czuj_wew_05 = 0
    czuj_wew_06 = 0
    czuj_wew_07 = 0
    czuj_wew_08 = 0
    czuj_wew_09 = 0
    czuj_wew_10 = 0
    czuj_cwu = 0
    czuj_cwu_cyr = 0

    def __init__(self):

        self.czuj_zew = self.read(par['czuj_zew'])
        self.czuj_co_zas = self.read(par['czuj_co_zas'])
        self.czuj_co_return = self.read(par['czuj_co_return'])
        self.czuj_buf_top = self.read(par['czuj_buf_top'])
        self.czuj_buf_mid = self.read(par['czuj_buf_mid'])
        self.czuj_buf_low = self.read(par['czuj_buf_low'])
        self.czuj_wew_01 = self.read(par['czuj_wew_01'])
        self.czuj_wew_02 = self.read(par['czuj_wew_02'])
        self.czuj_wew_03 = self.read(par['czuj_wew_03'])
        self.czuj_wew_04 = self.read(par['czuj_wew_04'])
        self.czuj_wew_05 = self.read(par['czuj_wew_05'])
        self.czuj_wew_06 = self.read(par['czuj_wew_06'])
        self.czuj_wew_07 = self.read(par['czuj_wew_07'])
        self.czuj_wew_08 = self.read(par['czuj_wew_08'])
        self.czuj_wew_09 = self.read(par['czuj_wew_09'])
        self.czuj_wew_10 = self.read(par['czuj_wew_10'])
        self.czuj_cwu = self.read(par['czuj_cwu'])
        self.czuj_cwu_cyr = self.read(par['czuj_cwu_cyr'])


    def read(self, czujnik):
        # Odczyt temperatury z czujnika o ID
        # device = DS18B20(czujnik)
        # return float(device.getCelsius())
        t = 21
        return t

    def read_all(self):
        self.czuj_zew = self.read(par['czuj_zew'])
        self.czuj_co_zas = self.read(par['czuj_co_zas'])
        self.czuj_co_return = self.read(par['czuj_co_return'])
        self.czuj_buf_top = self.read(par['czuj_buf_top'])
        self.czuj_buf_mid = self.read(par['czuj_buf_mid'])
        self.czuj_buf_low = self.read(par['czuj_buf_low'])
        self.czuj_wew_01 = self.read(par['czuj_wew_01'])
        self.czuj_wew_02 = self.read(par['czuj_wew_02'])
        self.czuj_wew_03 = self.read(par['czuj_wew_03'])
        self.czuj_wew_04 = self.read(par['czuj_wew_04'])
        self.czuj_wew_05 = self.read(par['czuj_wew_05'])
        self.czuj_wew_06 = self.read(par['czuj_wew_06'])
        self.czuj_wew_07 = self.read(par['czuj_wew_07'])
        self.czuj_wew_08 = self.read(par['czuj_wew_08'])
        self.czuj_wew_09 = self.read(par['czuj_wew_09'])
        self.czuj_wew_10 = self.read(par['czuj_wew_10'])
        self.czuj_cwu = self.read(par['czuj_cwu'])
        self.czuj_cwu_cyr = self.read(par['czuj_cwu_cyr'])
        self.czuj_zew = self.read(par['czuj_zew'])

class CWU(Parametry, Piec, DB, Temp):



    _status = False
    _okno = None
    _okno_start = None
    _okno_stop = None
    _temp = 0
    _histereza = 0

    def __init__(self):

        self._status = False
        self._okno = None
        self._okno_start = None
        self._okno_stop = None
        self._temp = 0                  # temperatura dyspozycyjna. zadana dla CWU
        self._histereza = 0             # histereza dla temperatury dyspozycyjnej w zbiorniku

    def sprawdz_okno(self):

        dzien = {0: 'NI', 1: 'PO', 2: 'WT', 3: 'SR', 4: 'CZ', 5: 'PI', 6: 'SO'}

        # nt = aktualny czas = nowtime
        czas = time.localtime()
        czas = time.strftime("%H:%M", czas)

        # ndow = NowDayOfWeek = aktualny dzien tygodnia
        dtyg1 = time.localtime()
        dtyg2 = time.strftime("%w", dtyg1)
        dt = dzien[int(dtyg2)]

        if dt in par['cwu_okno_1_days'] and czas  >= par['cwu_okno_1_start'] and czas <= par['cwu_okno_1_stop']:
            self._status = True
            self._okno = 1
            self._okno_start = par['cwu_okno_1_start']
            self._okno_stop = par['cwu_okno_1_stop']
            self._temp = par['cwu_okno_1_temp']
            self._histereza = par['cwu_okno_1_hist']

        elif dt in par['cwu_okno_2_days'] and czas  >= par['cwu_okno_2_start'] and czas <= par['cwu_okno_2_stop']:
            self._status = True
            self._okno = 2
            self._okno_start = par['cwu_okno_2_start']
            self._okno_stop = par['cwu_okno_2_stop']
            self._temp = par['cwu_okno_2_temp']
            self._histereza = par['cwu_okno_2_hist']

        elif dt in par['cwu_okno_3_days'] and czas  >= par['cwu_okno_3_start'] and czas <= par['cwu_okno_3_stop']:
            self._status = True
            self._okno = 3
            self._okno_start = par['cwu_okno_3_start']
            self._okno_stop = par['cwu_okno_3_stop']
            self._temp = par['cwu_okno_3_temp']
            self._histereza = par['cwu_okno_3_hist']

        elif dt in par['cwu_okno_4_days'] and czas  >= par['cwu_okno_4_start'] and czas <= par['cwu_okno_4_stop']:
            self._status = True
            self._okno = 4
            self._okno_start = par['cwu_okno_4_start']
            self._okno_stop = par['cwu_okno_4_stop']
            self._temp = par['cwu_okno_4_temp']
            self._histereza = par['cwu_okno_4_hist']

        elif dt in par['cwu_okno_5_days'] and czas  >= par['cwu_okno_5_start'] and czas <= par['cwu_okno_5_stop']:
            self._status = True
            self._okno = 5
            self._okno_start = par['cwu_okno_5_start']
            self._okno_stop = par['cwu_okno_5_stop']
            self._temp = par['cwu_okno_5_temp']
            self._histereza = par['cwu_okno_5_hist']

        elif dt in par['cwu_okno_6_days'] and czas  >= par['cwu_okno_6_start'] and czas <= par['cwu_okno_6_stop']:
            self._status = True
            self._okno = 6
            self._okno_start = par['cwu_okno_6_start']
            self._okno_stop = par['cwu_okno_6_stop']
            self._temp = par['cwu_okno_6_temp']
            self._histereza = par['cwu_okno_6_hist']

        else:
            self._status = False
            self._okno = None
            self._okno_start = None
            self._okno_stop = None
            self._temp = None
            self._histereza = 0

        if self._status == True:
            Piec().on('CWU',self._okno_start, self._okno_stop,self._temp, self._histereza)

        if self.status == False:
            Piec().off('CWU',self.okno_start, self.okno_stop,self.temp, self.histereza)
        


class CO():

    par = Parametry()

    status = False
    okno_nr = None
    okno_start = None
    okno_stop = None
    temp = None
    histereza = None

    def __init__(self):
        self.status = False
        self.okno_nr = None
        self.okno_start = None
        self.okno_stop = None
        self.temp = None
        self.histereza = None

    def sprawdz_okno(self):
        dzien = {0: 'NI', 1: 'PO', 2: 'WT', 3: 'SR', 4: 'CZ', 5: 'PI', 6: 'SO'}

        # nt = aktualny czas = nowtime
        czas = time.localtime()
        czas = time.strftime("%H:%M", czas)

        # ndow = NowDayOfWeek = aktualny dzien tygodnia
        dtyg1 = time.localtime()
        dtyg2 = time.strftime("%w", dtyg1)
        dt = dzien[int(dtyg2)]

        if dt in par['co_okno_1_days'] and czas  >= par['co_okno_1_start'] and czas <= par['co_okno_1_stop']:
            self.status = True
            self.okno = 1
            self.okno_start = par['co_okno_1_start']
            self.okno_stop = par['co_okno_1_stop']
            self.temp = par['co_okno_1_temp']
            self.histereza = par['co_okno_1_hist']

            #return (True,1,par['co_okno_1_start,par['co_okno_1_stop,par['co_okno_1_temp)
        elif dt in par['co_okno_2_days'] and czas  >= par['co_okno_2_start'] and czas <= par['co_okno_2_stop']:
            self.status = True
            self.okno = 2
            self.okno_start = par['co_okno_2_start']
            self.okno_stop = par['co_okno_2_stop']
            self.temp = par['co_okno_2_temp']
            self.histereza = par['co_okno_2_hist']

            #return (True,2,par['co_okno_2_start,par['co_okno_2_stop,par['co_okno_2_temp)
        elif dt in par['co_okno_3_days'] and czas  >= par['co_okno_3_start'] and czas <= par['co_okno_3_stop']:
            self.status = True
            self.okno = 3
            self.okno_start = par['co_okno_3_start']
            self.okno_stop = par['co_okno_3_stop']
            self.temp = par['co_okno_3_temp']
            self.histereza = par['co_okno_3_hist']

            # return (True,3,par['co_okno_3_start,par['co_okno_3_stop,par['co_okno_3_temp)
        elif dt in par['co_okno_4_days'] and czas  >= par['co_okno_4_start'] and czas <= par['co_okno_4_stop']:
            self.status = True
            self.okno = 4
            self.okno_start = par['co_okno_4_start']
            self.okno_stop = par['co_okno_4_stop']
            self.temp = par['co_okno_4_temp']
            self.histereza = par['co_okno_4_hist']

            # return (True,4,par['co_okno_4_start,par['co_okno_4_stop,par['co_okno_4_temp)
        elif dt in par['co_okno_5_days'] and czas  >= par['co_okno_5_start'] and czas <= par['co_okno_5_stop']:
            self.status = True
            self.okno = 5
            self.okno_start = par['co_okno_5_start']
            self.okno_stop = par['co_okno_5_stop']
            self.temp = par['co_okno_5_temp']
            self.histereza = par['co_okno_5_hist']

            # return (True,5,par['co_okno_5_start,par['co_okno_5_stop,par['co_okno_5_temp)
        elif dt in par['co_okno_6_days'] and czas  >= par['co_okno_6_start'] and czas <= par['co_okno_6_stop']:
            self.status = True
            self.okno = 6
            self.okno_start = par['co_okno_6_start']
            self.okno_stop = par['co_okno_6_stop']
            self.temp = par['co_okno_6_temp']
            self.histereza = par['co_okno_6_hist']

            # return (True,6,par['co_okno_6_start,par['co_okno_6_stop,par['co_okno_6_temp)
        else:
            self.status = False
            self.okno = None
            self.okno_start = None
            self.okno_stop = None
            self.temp = None
            self.histereza = None

class Zawor_Trojdrogowy():

    temp_zasilania_zadana = 21

    def __init__(self):
        pass

class Pompa_CO(Parametry, Piec, DB, Temp, Stycznik):

    #Parametry.read_all()

    stycz_pompa = Stycznik(par['st_co_pompa'])

    #temp = Temp()
    #temp.read_all()
    _print_blokada_pompy_CO = False

    def __init__(self, piec_temp = 0):
        self._wlaczona = False

    def sprawdz_czy_wlaczyc(self, temp_zasilania):
        Temp().read_all()

        if Temp.czuj_buf_mid >= temp_zasilania:    # jeżeli temperatura zbiornika jest wyższa od żądanej temp zasilania CO

            if (par['pom1_temp'] - par['pom1_hist']) > self.temp.czuj_wew_01:

                if self.wlaczona == False:
                    Log().debug("Włączam pompę CO. Temperatura pomieszczenia %s jest mniejsza od Temp. zadanej %s" % (self.temp.czuj_wew_01, par['pom1_temp']),'CO POMPA')
                    self.on()

            else:
                if self.wlaczona == True:
                    Log().debug("Wyłączam pompę CO. Temperatura pomieszczenia %s jest większa od Temp. zadanej %s" % (self.temp.czuj_wew_01, par['pom1_temp']), 'CO POMPA')
                    self.off()

            print_blokada_pompy_CO = True;
        else:                                           # jeżeli temperatura zbiornika jest NIZSZA od żądanej temp zasilania CO

            if self._print_blokada_pompy_CO == False:
                Log().debug("Nie mogę włączyć pompy CO. Temperatura bufora %s jest za niska by uzyskać Temp. zasilania %s" % (Temp().czuj_buf_mid, temp_zasilania),'CO POMPA')
                self.print_blokada_pompy_CO = True
                self.off()

    def on(self):

        if self.wlaczona ==False:
            self.stycz_pompa.on()
            Log().debug("Pompa CO została włączona",'CO POMPA')
            self.wlaczona = True

    def off(self):
        #self.off
        if self._wlaczona == True:
            self.stycz_pompa.off()
            Log().debug("Pompa CO została wyłączona",'CO POMPA')
            self.wlaczona = False

class Pomieszczenia():
    def __init__(self):
        pass

def setup():
    ##################### POCZĄTEK SETUP() ########################
    log = Log()

    Parametry().read_all()

    sty = Stycznik()
    sty.reset_all()

    time.sleep(par['db_delay'])

    # _conn = MySQLdb.connect(host=par['db_server'], user=par['db_username'], passwd=par['db_password'], db=par['db_name'])

    Log().debug('[DB] - Odczytano z pliku konfiguracyjnego definicję połączenia DB: host= %s, user=%s, passwd=%s, db=%s' % (par['db_server'], par['db_username'], par['db_password'], par['db_name']),'DB')
    Log().debug('[DB] - Podłączono do bazy danych DB: host= %s, user=%s, passwd=%s, db=%s' % (par['db_server'], par['db_username'], par['db_password'], par['db_name']), 'DB')


    # TODO: DELETE: db = DB()
    # TODO: DELETE: db.db_init()

    ##################### KONIEC SETUP() ########################

def loop():


    params = Parametry()

    db = DB()

    temp = Temp()
    piec = Piec()
    pompa_co = Pompa_CO()

    cwu = CWU()
    co = CO()







    licznik_db = 1      # licznik dla zapisu temperatur do db
    licznik_tmp = 1     # licznik dla odczytu temperatur
    licznik_par = 1     # licznik dla automatycznego ponownego odczytu parametrów (ustawione na sztywno co godzinę)

    petla = True         # wyrzucić w Rpi

    while petla is True:
        params.read_all()
        cwu.sprawdz_okno()

        if par['okresgrzewczy'] == True:
            pompa_co.sprawdz_czy_wlaczyc()

        if licznik_par % 1 == 0:         # ponowny, cykliczny odczyt parametrów z pliku konfiguracyjnego co godzinę
            # Odczyt temperatur
            licznik_par = 0

        # TODO: histereza temperatury pieca

        # # # # # # #   G Ł Ó W N A          P Ę T L A              P I E C A  -  start
        """
        if par['okresgrzewczy'] is False:       # jeżeli okres grzewczy=Nie to grzejemy tylko piec na potrzeby CWU

            if piec.podgrzewam_CWU is False:
                if cwu.status is True:              # jeżeli jest okno CWU

                    if temp.czuj_buf_mid  <=  cwu.temp - cwu.histereza/2:  # jeżeli temperatura w środku BUFORA jest niższa od zadanej
                        #logging.debug ("[CWU] - Włączam ogrzewnie CWU. Przycyzna: temp bufora %s < %s. Okres grzewczy: %s. Okno: %s -> %s." % (Temp.czuj_buf_mid, cwu_okno.temp - cwu_okno.histereza/2, par['okresgrzewczy, cwu_okno.okno_start, cwu_okno.okno_stop))
                        #print "[CWU] - Włączam ogrzewnie CWU. Przycyzna: temp bufora %s < %s. Okres grzewczy: %s. Okno: %s -> %s." % (Temp.czuj_buf_mid, cwu_okno.temp - cwu_okno.histereza/2, par['okresgrzewczy, cwu_okno.okno_start, cwu_okno.okno_stop)
                        piec.on('CWU',temp.czuj_buf_mid, cwu.okno_start, cwu.okno_stop, cwu.temp, cwu.histereza, 1)

                    if temp.czuj_buf_mid  > cwu.temp + cwu.histereza/2:  # jeżeli temperatura w środku BUFORA jest wyższa od zadanej
                        #logging.debug ("[CWU] - Wyłączam ogrzewanie CWU. Przycyzna: temp bufora %s > %s. Okres grzewczy: %s. Okno: %s -> %s." % (Temp.czuj_buf_mid, cwu_okno.temp + cwu_okno.histereza/2, par['okresgrzewczy, cwu_okno.okno_start, cwu_okno.okno_stop))
                        #print "[CWU] - Wyłączam ogrzewanie CWU. Przycyzna: temp bufora %s > %s. Okres grzewczy: %s. Okno: %s -> %s." % (Temp.czuj_buf_mid, cwu_okno.temp + cwu_okno.histereza/2, par['okresgrzewczy, cwu_okno.okno_start, cwu_okno.okno_stop)
                        piec.off('CWU',temp.czuj_buf_mid,cwu.okno_start, cwu.okno_stop,cwu.temp, cwu.histereza)

                else:
                    if piec.status is True:
                        #logging.debug ("[CWU] - Wyłączam ogrzewanie CWU. Przycyzna: koniec okna nr %s. Okres grzewczy: %s. Okno: %s -> %s." % (cwu_okno.okno, par['okresgrzewczy, cwu_okno.okno_start, cwu_okno.okno_stop))
                        piec.off('CWU',temp.czuj_buf_mid,cwu.okno_start, cwu.okno_stop,cwu.temp, cwu.histereza)

        elif par['okresgrzewczy'] is True:      # jeżeli okres grzewczy = Tak - trzeba skombinować okna i temperatury

            if cwu.status is True: # jeżeli jest okno CWU

                if temp.czuj_buf_mid  <=  cwu.temp - cwu.histereza/2:  # jeżeli temperatura w środku BUFORA jest niższa od zadanej
                    #logging.debug ("[CWU] - Włączam ogrzewnie CWU. Przycyzna: temp bufora %s < %s. Okres grzewczy: %s. Okno: %s -> %s." % (Temp.czuj_buf_mid, cwu_okno.temp - cwu_okno.histereza/2, par['okresgrzewczy, cwu_okno.okno_start, cwu_okno.okno_stop))
                    #print "[CWU] - Włączam ogrzewnie CWU. Przycyzna: temp bufora %s < %s. Okres grzewczy: %s. Okno: %s -> %s." % (Temp.czuj_buf_mid, cwu_okno.temp - cwu_okno.histereza/2, par['okresgrzewczy, cwu_okno.okno_start, cwu_okno.okno_stop)
                    piec.on('CWU',temp.czuj_buf_mid, cwu.okno_start, cwu.okno_stop, cwu.temp, cwu.histereza, 1)

                if temp.czuj_buf_mid  > cwu.temp + cwu.histereza/2:  # jeżeli temperatura w środku BUFORA jest wyższa od zadanej
                    #logging.debug ("[CWU] - Wyłączam ogrzewanie CWU. Przycyzna: temp bufora %s > %s. Okres grzewczy: %s. Okno: %s -> %s." % (Temp.czuj_buf_mid, cwu_okno.temp + cwu_okno.histereza/2, par['okresgrzewczy, cwu_okno.okno_start, cwu_okno.okno_stop))
                    #print "[CWU] - Wyłączam ogrzewanie CWU. Przycyzna: temp bufora %s > %s. Okres grzewczy: %s. Okno: %s -> %s." % (Temp.czuj_buf_mid, cwu_okno.temp + cwu_okno.histereza/2, par['okresgrzewczy, cwu_okno.okno_start, cwu_okno.okno_stop)
                    piec.off('CWU',temp.czuj_buf_mid, cwu.okno_start, cwu.okno_stop,cwu.temp, cwu.histereza)

            if cwu.status is False and piec.podgrzewam_CWU is True:
                if piec.status() is True:
                    #logging.debug ("[CWU] - Wyłączam ogrzewanie CWU. Przycyzna: koniec okna nr %s. Okres grzewczy: %s. Okno: %s -> %s." % (cwu_okno.okno, par['okresgrzewczy, cwu_okno.okno_start, cwu_okno.okno_stop))
                    #print "[CWU] - Wyłączam ogrzewanie CWU. Przycyzna: koniec okna nr %s. Okres grzewczy: %s. Okno: %s -> %s." % (cwu_okno.okno, par['okresgrzewczy, cwu_okno.okno_start, cwu_okno.okno_stop)
                    piec.off('CWU', temp.czuj_buf_mid,cwu.okno_start, cwu.okno_stop,cwu.temp, cwu.histereza)

            if piec.podgrzewam_CWU is False:
                if co.status is True:        # jeżeli jest okno CO
                    if temp.czuj_buf_mid  <=  co.temp - co.histereza/2:  # jeżeli temperatura w środku BUFORA jest niższa od zadanej
                        #logging.debug ("[CO] - Włączam ogrzewnie CO. Przycyzna: temp bufora %s < %s. Okres grzewczy: %s. Okno: %s -> %s." % (Temp.czuj_buf_mid, co.temp - co.histereza/2, par['okresgrzewczy, co.okno_start, co.okno_stop))
                        #print "[CO] - Włączam ogrzewnie CO. Przycyzna: temp bufora %s < %s. Okres grzewczy: %s. Okno: %s -> %s." % (Temp.czuj_buf_mid, co.temp - co.histereza/2, par['okresgrzewczy, co.okno_start, co.okno_stop)
                        piec.on('CO',temp.czuj_buf_mid, co.okno_start, co.okno_stop, co.temp, co.histereza)

                    if temp.czuj_buf_mid  > co.temp + co.histereza/2:  # jeżeli temperatura w środku BUFORA jest wyższa od zadanej
                        #logging.debug ("[CO] - Wyłączam ogrzewanie CO. Przycyzna: temp bufora %s > %s. Okres grzewczy: %s. Okno: %s -> %s." % (Temp.czuj_buf_mid, co.temp + co.histereza/2, par['okresgrzewczy, co.okno_start, co.okno_stop))
                        #print "[CO] - Wyłączam ogrzewanie CO. Przycyzna: temp bufora %s > %s. Okres grzewczy: %s. Okno: %s -> %s." % (Temp.czuj_buf_mid, co.temp + co.histereza/2, par['okresgrzewczy, co.okno_start, co.okno_stop)
                        Piec.off('CO',temp.czuj_buf_mid,co.okno_start, co.okno_stop, co.temp, co.histereza)

            if co.status is False and piec.podgrzewam_CO is True:
                if piec.status is True:
                    #logging.debug ("[CO] - Wyłączam ogrzewanie CO. Przycyzna: koniec okna nr %s. Okres grzewczy: %s. Okno: %s -> %s." % (co.okno, par['okresgrzewczy, co.okno_start, co.okno_stop))
                    #print "[CO] - Wyłączam ogrzewanie CO. Przycyzna: koniec okna nr %s. Okres grzewczy: %s. Okno: %s -> %s." % (co.okno, par['okresgrzewczy, co.okno_start, co.okno_stop)
                    piec.off('CO',temp.czuj_buf_mid,co.okno_start, co.okno_stop, co.temp, co.histereza)
        """
        ######## P I E C A    - stop      # # # # # # #   G Ł Ó W N A          P Ę T L A

        if licznik_tmp % par['temp_timeinterval'] == 0:
            # Odczyt temperatur
            licznik_tmp = 0


        if licznik_db % par['db_timeinterval'] == 0:
            db.zapis_temp()
            licznik_db = 0


        pompa_co.sprawdz_czy_wlaczyc(Zawor_Trojdrogowy.temp_zasilania_zadana)


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
    logging.debug("PiConnect zostal zamkniety")
    conn.close

    """