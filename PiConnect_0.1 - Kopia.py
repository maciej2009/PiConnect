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


def setup():
    ################################
    # Odczyt paramterów
    ################################

    class Params:

        def readall(self):
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
                'poziom6' : int(conf.get('Piec', 'poziom6'))

                }

            logging.basicConfig(filename='PiConnect.log', level='DEBUG', format='%(levelname)s: %(asctime)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S %a', filemode = 'w')

            for (char,n) in sorted(par.items()):
                # logging.info("[CONF] - Odczytano z pliku konfiguracyjnego parametr: %s = %s" % (char, n))
                # print "Odczytano z pliku konfiguracyjnego parametr: %s = %s" % (char, n)
                pass
            return par

    def reset_stycznikow():
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
        logging.info('[STYCZNIK] - Zresetowano konfigurację wszystkich styczników')


    def db_init():
        try:

            time.sleep(par['db_delay'])

            global conn
            conn = MySQLdb.connect(host=par['db_server'], user=par['db_username'], passwd=par['db_password'], db=par['db_name'])

            logging.info('[DB] - Odczytano z pliku konfiguracyjnego definicję połączenia DB: host= %s, user=%s, passwd=%s, db=%s' % (par['db_server'], par['db_username'], par['db_password'], par['db_name']))
            logging.info('[DB] - Podłączono do bazy danych DB: host= %s, user=%s, passwd=%s, db=%s' % (par['db_server'], par['db_username'], par['db_password'], par['db_name']))

            return conn

        except:
            # TBD: check_SQL_connection()
            #	print 'Blad polaczenia z DB'
            logging.error('[DB] - Blad podlaczenia do bazy danych: host= %s, user=%s, passwd=%s, db=%s' % (par['db_server'], par['db_username'], par['db_password'], par['db_name']))

            pass

    def log_init():
            logging.basicConfig(filename='PiConnect.log', level=par['log_loginglevel'], format='%(levelname)s: %(asctime)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S %a')
            logging.info("[LOG] - Ustawiono poziom logowania: LoggingLevel = %s" % par['log_loginglevel'])


    Para = Params()
    parametry = Para.readall()
    log_init()
    reset_stycznikow()
    db_init()


    # print '###### KONIEC SETUP()'

    ##################### KONIEC SETUP() ########################




def loop():

    class Temp():

        def read(self, czujnik):
            # Odczyt temperatury z czujnika o ID
            # device = DS18B20(czujnik)
            # return float(device.getCelsius())
            t = 21
            return t

        def readall(self):
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

    class cwu_okno():

        def __init__(self):
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

            if dt in par['cwu_okno_1_days'] and czas >= par['cwu_okno_1_start'] and czas <= par['cwu_okno_1_stop']:
                self.status = True
                self.okno = 1
                self.okno_start = par['cwu_okno_1_start']
                self.okno_stop = par['cwu_okno_1_stop']
                self.temp = par['cwu_okno_1_temp']
                self.histereza = par['cwu_okno_1_hist']

                #return (True,1,par['cwu_okno_1_start'],par['cwu_okno_1_stop'],par['cwu_okno_1_temp'])
            elif dt in par['cwu_okno_2_days'] and czas >= par['cwu_okno_2_start'] and czas <= par['cwu_okno_2_stop']:
                self.status = True
                self.okno = 2
                self.okno_start = par['cwu_okno_2_start']
                self.okno_stop = par['cwu_okno_2_stop']
                self.temp = par['cwu_okno_2_temp']
                self.histereza = par['cwu_okno_2_hist']
                #return (True,2,par['cwu_okno_2_start'],par['cwu_okno_2_stop'],par['cwu_okno_2_temp'])

            elif dt in par['cwu_okno_3_days'] and czas >= par['cwu_okno_3_start'] and czas <= par['cwu_okno_3_stop']:
                self.status = True
                self.okno = 3
                self.okno_start = par['cwu_okno_3_start']
                self.okno_stop = par['cwu_okno_3_stop']
                self.temp = par['cwu_okno_3_temp']
                self.histereza = par['cwu_okno_3_hist']

                # return (True,3,par['cwu_okno_3_start'],par['cwu_okno_3_stop'],par['cwu_okno_3_temp'])
            elif dt in par['cwu_okno_4_days'] and czas >= par['cwu_okno_4_start'] and czas <= par['cwu_okno_4_stop']:
                self.status = True
                self.okno = 4
                self.okno_start = par['cwu_okno_4_start']
                self.okno_stop = par['cwu_okno_4_stop']
                self.temp = par['cwu_okno_4_temp']
                self.histereza = par['cwu_okno_4_hist']

                # return (True,4,par['cwu_okno_4_start'],par['cwu_okno_4_stop'],par['cwu_okno_4_temp'])
            elif dt in par['cwu_okno_5_days'] and czas >= par['cwu_okno_5_start'] and czas <= par['cwu_okno_5_stop']:
                self.status = True
                self.okno = 5
                self.okno_start = par['cwu_okno_5_start']
                self.okno_stop = par['cwu_okno_5_stop']
                self.temp = par['cwu_okno_5_temp']
                self.histereza = par['cwu_okno_5_hist']

                # return (True,5,par['cwu_okno_5_start'],par['cwu_okno_5_stop'],par['cwu_okno_5_temp'])
            elif dt in par['cwu_okno_6_days'] and czas >= par['cwu_okno_6_start'] and czas <= par['cwu_okno_6_stop']:
                self.status = True
                self.okno = 6
                self.okno_start = par['cwu_okno_6_start']
                self.okno_stop = par['cwu_okno_6_stop']
                self.temp = par['cwu_okno_6_temp']
                self.histereza = par['cwu_okno_6_hist']

                # return (True,6,par['cwu_okno_6_start'],par['cwu_okno_6_stop'],par['cwu_okno_6_temp'])
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

            if dt in par['co_okno_1_days'] and czas >= par['co_okno_1_start'] and czas <= par['co_okno_1_stop']:
                self.status = True
                self.okno = 1
                self.okno_start = par['co_okno_1_start']
                self.okno_stop = par['co_okno_1_stop']
                self.temp = par['co_okno_1_temp']
                self.histereza = par['co_okno_1_hist']

                #return (True,1,par['co_okno_1_start'],par['co_okno_1_stop'],par['co_okno_1_temp'])
            elif dt in par['co_okno_2_days'] and czas >= par['co_okno_2_start'] and czas <= par['co_okno_2_stop']:
                self.status = True
                self.okno = 2
                self.okno_start = par['co_okno_2_start']
                self.okno_stop = par['co_okno_2_stop']
                self.temp = par['co_okno_2_temp']
                self.histereza = par['co_okno_2_hist']

                #return (True,2,par['co_okno_2_start'],par['co_okno_2_stop'],par['co_okno_2_temp'])
            elif dt in par['co_okno_3_days'] and czas >= par['co_okno_3_start'] and czas <= par['co_okno_3_stop']:
                self.status = True
                self.okno = 3
                self.okno_start = par['co_okno_3_start']
                self.okno_stop = par['co_okno_3_stop']
                self.temp = par['co_okno_3_temp']
                self.histereza = par['co_okno_3_hist']

                # return (True,3,par['co_okno_3_start'],par['co_okno_3_stop'],par['co_okno_3_temp'])
            elif dt in par['co_okno_4_days'] and czas >= par['co_okno_4_start'] and czas <= par['co_okno_4_stop']:
                self.status = True
                self.okno = 4
                self.okno_start = par['co_okno_4_start']
                self.okno_stop = par['co_okno_4_stop']
                self.temp = par['co_okno_4_temp']
                self.histereza = par['co_okno_4_hist']

                # return (True,4,par['co_okno_4_start'],par['co_okno_4_stop'],par['co_okno_4_temp'])
            elif dt in par['co_okno_5_days'] and czas >= par['co_okno_5_start'] and czas <= par['co_okno_5_stop']:
                self.status = True
                self.okno = 5
                self.okno_start = par['co_okno_5_start']
                self.okno_stop = par['co_okno_5_stop']
                self.temp = par['co_okno_5_temp']
                self.histereza = par['co_okno_5_hist']

                # return (True,5,par['co_okno_5_start'],par['co_okno_5_stop'],par['co_okno_5_temp'])
            elif dt in par['co_okno_6_days'] and czas >= par['co_okno_6_start'] and czas <= par['co_okno_6_stop']:
                self.status = True
                self.okno = 6
                self.okno_start = par['co_okno_6_start']
                self.okno_stop = par['co_okno_6_stop']
                self.temp = par['co_okno_6_temp']
                self.histereza = par['co_okno_6_hist']

                # return (True,6,par['co_okno_6_start'],par['co_okno_6_stop'],par['co_okno_6_temp'])
            else:
                self.status = False
                self.okno = None
                self.okno_start = None
                self.okno_stop = None
                self.temp = None
                self.histereza = None




    def taryfa2():

        dzien = {0: 'NI', 1: 'PO', 2: 'WT', 3: 'SR', 4: 'CZ', 5: 'PI', 6: 'SO'}

        # nt = aktualny czas = nowtime
        czas = time.localtime()
        czas = time.strftime("%H:%M", czas)

        # ndow = NowDayOfWeek = aktualny dzien tygodnia
        dtyg1 = time.localtime()
        dtyg2 = time.strftime("%w", dtyg1)
        dt = dzien[int(dtyg2)]

        if dt in par['taryfa2_1_dni'] and czas >= par['taryfa2_1_godz_start'] and czas < par['taryfa2_1_godz_stop']:
            return (True, par['taryfa2_cena'], 1, par['taryfa2_1_godz_start'],par['taryfa2_1_godz_stop'])
        elif dt in par['taryfa2_2_dni'] and czas >= par['taryfa2_2_godz_start'] and czas < par['taryfa2_2_godz_stop']:
            return (True, par['taryfa2_cena'], 2, par['taryfa2_1_godz_start'],par['taryfa2_2_godz_stop'])
        elif dt in par['taryfa2_3_dni'] and czas >= par['taryfa2_3_godz_start'] and czas < par['taryfa2_3_godz_stop']:
            return (True, par['taryfa2_cena'], 3, par['taryfa2_1_godz_start'],par['taryfa2_3_godz_stop'])
        elif dt in par['taryfa2_4_dni'] and czas >= par['taryfa2_4_godz_start'] and czas < par['taryfa2_4_godz_stop']:
            return (True, par['taryfa2_cena'], 4, par['taryfa2_1_godz_start'],par['taryfa2_4_godz_stop'])
        elif dt in par['taryfa2_5_dni'] and czas >= par['taryfa2_5_godz_start'] and czas < par['taryfa2_5_godz_stop']:
            return (True, par['taryfa2_cena'], 5, par['taryfa2_5_godz_start'],par['taryfa2_5_godz_stop'])
        elif dt in par['taryfa2_6_dni'] and czas >= par['taryfa2_6_godz_start'] and czas < par['taryfa2_6_godz_stop']:
            return (True, par['taryfa2_cena'], 6, par['taryfa2_1_godz_start'],par['taryfa2_6_godz_stop'])
        else:
            return (False, par['taryfa1_cena'], 0)

    class Stycznik():

        def __init__(self):
            pass

        def on(self, stycz):
            # Rpi: gpio.digitalWrite(stycz, gpio.HIGH)
            # print 'Włączyłem stycznik %s' % stycz
            logging.info("[STYCZNIK] - Stycznik nr %s został włączony" % stycz)
            pass

        def off (self, stycz):
            # Rpi: gpio.digitalWrite(stycz, gpio.LOW)
            # print 'Wyłączyłem stycznik %s' % stycz
            logging.info("[STYCZNIK] - Stycznik nr %s został wyłączony" % stycz)

            pass

        def status (self, stycz):
            # TODO: Dorobić zwracanie wartości poszczególnego stycznika.
            pass

    class Piec():

        def __init__(self):
            self.moc = 0
            self.nr_taryfy = 1
            self.taryfa_pln = taryfa2()[1]
            self.taryfa_okno = taryfa2()[2]
            self.poziom = 0
            self.podgrzewam_CWU = False            # Czy grzeje dla CWU
            self.podgrzewam_CO = False             # zy grzeje dla CO



        def on (self, zrodlo, poziom = 1):   # źródło = CWU, CO lub dogrzanie do temp. min po wyjściu z petli.

            zmieniono = False

            tmp_podgrzewam_CO = self.podgrzewam_CO
            tmp_podgrzewam_CWU = self.podgrzewam_CWU

            s = Stycznik()

            if taryfa2()[0]==True:
                self.nr_taryfy = 2
            elif taryfa2()[0]==False:
                self.nr_taryfy = 1

            # Wyłaczenie pieca CO jeżeli ma grzać SWU i na odwrót
            if zrodlo == 'CWU' and tmp_podgrzewam_CO == True:
                piec.off('CO')

            if zrodlo == 'CO' and tmp_podgrzewam_CWU == True:
                piec.off('CWU')

            # wyłacenie pieca jeżeli poziom ma ulec zmianie i piec działa
            if self.poziom > 0 and poziom <> self.poziom:
               piec.off(zrodlo)

            # odczytaj ponownie self...... bo piec.off() mógł je zmienić.
            tmp_podgrzewam_CO = self.podgrzewam_CO
            tmp_podgrzewam_CWU = self.podgrzewam_CWU


            # jeżeli coś się zmieniło to przestaw styczniki i zaloguj zmiany
            if zrodlo == 'CWU' and tmp_podgrzewam_CWU == False:
                zmieniono = True
                self.podgrzewam_CWU = True

            if zrodlo == 'CO' and tmp_podgrzewam_CO == False:
                zmieniono = True
                self.podgrzewam_CO = True



            if zmieniono == True:

                if poziom == 1:            # 3kW
                    s.on(par['st_grzalka_1'])
                    s.off(par['st_grzalka_2'])
                    s.off(par['st_grzalka_3'])
                    self.moc = 3

                elif poziom == 2:           # 6kW
                    s.off(par['st_grzalka_1'])
                    s.on(par['st_grzalka_2'])
                    s.off(par['st_grzalka_3'])
                    self.moc = 6

                elif poziom == 3:           # 9kW
                    s.off(par['st_grzalka_1'])
                    s.off(par['st_grzalka_2'])
                    s.on(par['st_grzalka_3'])
                    self.moc = 9

                elif poziom == 4:           # 12kW
                    s.on(par['st_grzalka_1'])
                    s.off(par['st_grzalka_2'])
                    s.on(par['st_grzalka_3'])
                    self.moc = 12

                elif poziom == 5:           # 15kW
                    s.off(par['st_grzalka_1'])
                    s.on(par['st_grzalka_2'])
                    s.on(par['st_grzalka_3'])
                    self.moc = 15

                elif poziom == 6:           # 18kW
                    s.on(par['st_grzalka_1'])
                    s.on(par['st_grzalka_2'])
                    s.on(par['st_grzalka_3'])
                    self.moc = 18



                # logging.info("[PIEC] - Włączono grzanie na potrzeby %s na poziomie %s z mocą %s kW" % (zrodlo, poziom, self.moc))
                print "[PIEC] - Włączono grzanie na potrzeby %s na poziomie %s z mocą %s kW" % (zrodlo, poziom, self.moc)


                if self.poziom != poziom:   # zapis do tabeli "piec" jezeli nastapiła zmiana poziomu

                    #try:
                    # conn.open
                    conn.begin()

                    if self.poziom == 0 or self.poziom == None:        # gdy właczamy piec, a nie zmieniamy wartość poziomu
                        tbl_piec_start = conn.cursor()
                        self.czas_start = datetime.today()

                        str = '''INSERT INTO piec VALUES('%s', '%s','0000-00-00 00:00:00',0,%s,%s,%s,%s,0,%s)''' % (zrodlo, datetime.strftime(self.czas_start,'%Y-%m-%d %H:%M:%S'), poziom, self.moc, self.nr_taryfy, self.taryfa_pln, self.taryfa_okno)
                        print str
                        # tbl_piec_start.execute(str)
                    else:
                        tbl_piec_stop = conn.cursor()
                        il_godzin1 = datetime.today()- self.czas_start
                        il_godzin = round(il_godzin1.total_seconds()/60/60,10)

                        str = """UPDATE piec SET piec_czas_stop = '%s', piec_il_godzin = '%s', piec_taryfa_wartosc = ROUND (piec_moc * piec_taryfa_pln * '%s',2) WHERE piec_czas_start = '%s'""" % (datetime.strftime(datetime.today(),'%Y-%m-%d %H:%M:%S'),round(il_godzin,3),il_godzin, datetime.strftime(self.czas_start,'%Y-%m-%d %H:%M:%S'))
                        print str
                        # tbl_piec_stop.execute(str)

                        tbl_piec_start = conn.cursor()
                        self.czas_start = datetime.today()
                        str = '''INSERT INTO piec VALUES('%s', '%s','0000-00-00 00:00:00',0,%s,%s,%s,%s,0,%s)''' % (zrodlo,datetime.strftime(self.czas_start,'%Y-%m-%d %H:%M:%S'), poziom, self.moc, self.nr_taryfy, self.taryfa_pln, self.taryfa_okno)
                        print str
                        # tbl_piec_start.execute(str)

                    conn.commit()

                self.poziom = poziom

        def off(self, zrodlo):

            wylacz_wszystkie_styczniki = False

            if self.podgrzewam_CWU == True:
                if zrodlo == 'CWU':
                    print "######################  wyłaczam podgrzewanie pieca dla CWU"
                    self.podgrzewam_CWU = False
                    wylacz_wszystkie_styczniki = True

            if self.podgrzewam_CO == True:
                if zrodlo == 'CO':
                    print "######################  wyłaczam podgrzewanie pieca dla CO"
                    self.podgrzewam_CO = False
                    wylacz_wszystkie_styczniki = True


            if wylacz_wszystkie_styczniki == True:
                s = Stycznik()


                s.off(par['st_grzalka_1'])
                s.off(par['st_grzalka_2'])
                s.off(par['st_grzalka_3'])
                self.moc = 0
                self.poziom = 0

                # logging.info("[PIEC] - Wyłączono piec dla ogrzewania %s." % zrodlo)
                print ("[PIEC] - Wyłączono piec dla ogrzewania %s." % zrodlo)

                # conn.open
                conn.begin()

                tbl_piec_stop = conn.cursor()
                il_godzin1 = datetime.today()-self.czas_start
                il_godzin = round(il_godzin1.total_seconds()/60/60,4)

                str = """UPDATE piec SET piec_czas_stop = '%s', piec_il_godzin = '%s', piec_taryfa_wartosc = ROUND (piec_moc * piec_taryfa_pln * '%s',2) WHERE piec_czas_start = '%s'""" % (datetime.strftime(datetime.today(),'%Y-%m-%d %H:%M:%S'), round(il_godzin,3), il_godzin, datetime.strftime(self.czas_start,'%Y-%m-%d %H:%M:%S'))
                print str
                tbl_piec_stop.execute(str)
                # print u"Piec wyłączony"
                conn.commit()


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
                logging.info("[PIEC] - Zwiększono poziom z %s na %s (z %s kW na %s kW)" % (akt_poziom, self.poziom, akt_moc, self.moc))
            else:
                logging.info("[PIEC] - Nie można już zwiększyć poziomu pracy pieca")
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
                logging.info("[PIEC] - Zmniejszono poziom z %s na %s (z %s kW na %s kW)" % (akt_poziom, self.poziom, akt_moc, self.moc))
            else:
                logging.info("[PIEC] - Nie można już zmniejszyć poziomu grzania")

        def status (self):
            if self.poziom != 0 and self.poziom != None:
                return True
            else:
                return False
            # print "Piec działa na %s kW" % (self.moc)
            # logging.info("[PIEC] - Piec działa na poziomie %s z mocą %s kW" %(self.poziom, self.moc))






    def db_zapis_temp():

        temp.readall()

        # conn.open
        conn.begin()

        tbl_temperatury = conn.cursor()

        sql = """ INSERT INTO temperatury VALUES ('%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """ % \
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
                            piec.nr_taryfy,
                            0,
                            0
                        )
        # print sql

        tbl_temperatury.execute(sql)
        conn.commit()







    stycznik = Stycznik()
    temp = Temp()
    temp.readall()
    piec = Piec()
    cwu = cwu_okno()
    co = co_okno()

    """
    print "Poziom pieca: ", piec.poziom
    print "Poziom pieca: ", piec.moc
    piec.on(0.1)
    print "Poziom pieca: ", piec.poziom
    print "Poziom pieca: ", piec.moc
    time.sleep(0.1)
    piec.zwieksz_moc()
    print "Poziom pieca: ", piec.poziom
    print "Poziom pieca: ", piec.moc
    time.sleep(0.1)
    piec.zwieksz_moc()
    print "Poziom pieca: ", piec.poziom
    print "Poziom pieca: ", piec.moc
    time.sleep(0.1)
    piec.off()
    print "Poziom pieca: ", piec.poziom
    print "Poziom pieca: ", piec.moc
    """

    petla = True         # wyrzucić w Rpi

    licznik_db = 1      # licznik dla zapisu temperatur do db
    licznik_tmp = 1     # licznik dla odczytu temperatur
    licznik_par = 1     # licznik dla automatycznego ponownego odczytu parametrów (ustawione na sztywno co godzinę)

    while petla == True:


        if licznik_par % 60 == 0:         # ponowny, cykliczny odczyt parametrów z pliku konfiguracyjnego co godzinę
            # Odczyt temperatur
            Para = setup()
            parametry = Para.readall()

            licznik_par = 0

        cwu.__call__()
        co.__call__()


        # print "#### Okres grzewczy = ",par['okresgrzewczy']
        # print "#### Oknco CWU = ", cwu.status
        # print "#### Piec - poziom = ", piec.poziom
        # TODO: histereza temperatury pieca


        if par['okresgrzewczy'] == False:       # jeżeli okres grzewczy=Nie to grzejemy tylko piec na potrzeby CWU

            if piec.podgrzewam_CWU == False:
                if cwu.status == True:              # jeżeli jest okno CWU

                    if temp.czuj_buf_mid  <=  cwu.temp - cwu.histereza/2:  # jeżeli temperatura w środku BUFORA jest niższa od zadanej
                        # logging.info ("[CWU] - Włączam piec dla CWU. Przycyzna: temp bufora %s < %s. Okres grzewczy: %s. Okno: %s -> %s." % (temp.czuj_buf_mid, cwu.temp, par['okresgrzewczy'], cwu.okno_start, cwu.okno_stop))
                        piec.on('CWU', 1)

                    if temp.czuj_buf_mid  > cwu.temp + cwu.histereza/2:  # jeżeli temperatura w środku BUFORA jest wyższa od zadanej
                        # logging.info ("[CWU] - Wyłączam piec dla CWU. Przycyzna: temp bufora %s > %s. Okres grzewczy: %s. Okno: %s -> %s." % (temp.czuj_buf_mid, cwu.temp, par['okresgrzewczy'], cwu.okno_start, cwu.okno_stop))
                        piec.off('CWU')

                else:
                    piec.off('CWU')

        elif par['okresgrzewczy'] == True:      # jeżeli okres grzewczy = Tak - trzeba skombinować okna i temperatury

            if cwu.status == True: # jeżeli jest okno CWU

                if temp.czuj_buf_mid  <=  cwu.temp - cwu.histereza/2:  # jeżeli temperatura w środku BUFORA jest niższa od zadanej
                    # logging.info ("[CWU] - Włączam piec dla CWU. Przycyzna: temp bufora %s < %s. Okres grzewczy: %s. Okno: %s -> %s." % (temp.czuj_buf_mid, cwu.temp, par['okresgrzewczy'], cwu.okno_start, cwu.okno_stop))
                    # print "!!! - Uruchamiam CWU..."
                    piec.on('CWU',1)

                if temp.czuj_buf_mid  > cwu.temp + cwu.histereza/2:  # jeżeli temperatura w środku BUFORA jest wyższa od zadanej
                    # logging.info ("[CWU] - Wyłączam piec dla CWU. Przycyzna: temp bufora %s > %s. Okres grzewczy: %s. Okno: %s -> %s." % (temp.czuj_buf_mid, cwu.temp, par['okresgrzewczy'], cwu.okno_start, cwu.okno_stop))
                    print "!!! - Zatrzynuję CWU..."
                    piec.off('CWU')

            if cwu.status == False and piec.podgrzewam_CWU == True:

                print "!!! - Zatrzymuję CWU..."
                piec.off('CWU')

            if piec.podgrzewam_CWU == False:
                if co.status == True:       # jeżeli jest okno CO
                    if temp.czuj_buf_mid  <=  co.temp - co.histereza/2:  # jeżeli temperatura w środku BUFORA jest niższa od zadanej
                        # logging.info ("[CO] - Włączam piec dla CO. Przycyzna: temp bufora %s < %s. Okres grzewczy: %s. Okno: %s -> %s." % (temp.czuj_buf_mid, co.temp, par['okresgrzewczy'], co.okno_start, co.okno_stop))
                        # print "!!! - Uruchamiam CO..."
                        piec.on('CO',1)

                    if temp.czuj_buf_mid  > co.temp + co.histereza/2:  # jeżeli temperatura w środku BUFORA jest wyższa od zadanej
                        # logging.info ("[CO] - Wyłączam piec dla CO. Przycyzna: temp bufora %s > %s. Okres grzewczy: %s. Okno: %s -> %s." % (temp.czuj_buf_mid, co.temp, par['okresgrzewczy'], co.okno_start, co.okno_stop))
                        print "!!! - Zatrzymuję CO..."
                        piec.off('CO')
            if co.status == False and piec.podgrzewam_CO == True:
                print "!!! - Zatrzymuję CO..."
                piec.off('CO')






        if licznik_tmp % par['temp_timeinterval'] == 0:
            # Odczyt temperatur
            db_zapis_temp()
            licznik_tmp = 0

        if licznik_db % par['db_timeinterval'] == 0:

            #print 'Zapisanano do bazy danych: %s' % licznik_db
            licznik_db = 0

        time.sleep(2)
        licznik_db = licznik_db +1
        licznik_tmp = licznik_tmp + 1
























    """
    piec = Piec()

    print "##### Włącz poziom 2"
    piec.on(2)

    print "##### Włącz poziom 3"
    piec.on(3)

    print "##### Zwiększ poziom"
    piec.zwieksz_moc()

    print "##### Status"
    piec.status()

    print "##### Zmniejsz poziom"
    piec.zmniejsz_moc()

    print "##### status"
    piec.status()

    print "##### Wyłącz piec"
    piec.off()

    piec.on(5)
    piec.zwieksz_moc()
    piec.zwieksz_moc()
    piec.on(2)
    piec.zmniejsz_moc()
    piec.zmniejsz_moc()
    piec.off()

    t = Temp()
    print t.read(par['czuj_cwu_cyr'])
    print t.readall()

    """













    ############################### KONIEC LOOP #####################################



setup()
loop()











































































"""
    global flag_grzanie_cwu
    flag_grzanie_cwu = False  # True jezeli grzanie jest wlaczone

    global okres_grzewczy






    ########################################################################################################################
    # Odczytaj czasy probkowania
    ########################################################################################################################

    TimeIntervalTemp =
    TimeIntervalDB = float(conf('General', 'TimeIntervalDB'))

    logging.info("Czas probkowania temepratur wynosi: %s [sek]" % TimeIntervalTemp)
    logging.info("Interwal zapisu historii do bazy danych wynosi: %s [sek]" % TimeIntervalDB)

    # Odczytaj polaczenie z DB
    conn = DB()

    # Przypisanie czujnikow do zmiennych
    ReadCzujniki()

    # Odczytaj jakie sa okna czasowe i zadane temperatury w oknach czasowych CWU

    global dzien
    dzien = {0: 'NI', 1: 'PO', 2: 'WT', 3: 'SR', 4: 'CZ', 5: 'PI', 6: 'SO'}


    Read_CWU_Windows()
    Read_CO_Windows()

    ########################################################################################################################
    # Odczytaj okres grzewczy
    ########################################################################################################################




def loop():
    ########################################################################################################################
    # GlOWNA PETLA
    ########################################################################################################################

    def GrzanieCWU_Start(okno, temperatura, okno_czas_stop):
        #TODO : Odczyt stycznikow z pliku konfiguracyjnego

        okno = str(okno)
        temperatura = str(temperatura)
        okno_czas_stop = str(okno_czas_stop)

        if flag_grzanie_cwu == False:
            logging.info("####")
            logging.info("#### Uruchomiono ogrzewanie CWU w oknie nr %s. CWU bedzie grzana do godz %s. Docelowa temp = %s st.C." % (okno, okno_czas_stop, temperatura))
            logging.info("####")

            gpio = webiopi.GPIO
            stycznik_blokada_grzania = 18
            gpio.setFunction(stycznik_blokada_grzania, gpio.OUT)
            gpio.digitalWrite(stycznik_blokada_grzania, gpio.HIGH)

    def GrzanieCWU_Stop():
        if flag_grzanie_cwu == True:
            logging.info("####")
            logging.info("#### Zatrzymano ogrzewanie CWU")
            logging.info("####")

            gpio = webiopi.GPIO
            stycznik_blokada_grzania = 18
            gpio.setFunction(stycznik_blokada_grzania, gpio.OUT)
            gpio.digitalWrite(stycznik_blokada_grzania, gpio.LOW)





    ########################################################################################################################
    # START SYSTEMU
    ########################################################################################################################

    global flag_grzanie_cwu
    #	flag_grzanie_cwu = False  # True jezeli grzanie jest wlaczone

    sec_db = 1
    sec_tmp = 1

    loop = True


    if sec_tmp % TimeIntervalTemp == 0:
        # Odczyt temperatur
        sec_tmp = 0

    # nt = aktualny czas = nowtime
    nt = time.localtime()
    nt = time.strftime("%H:%M", nt)

    # ndow = NowDayOfWeek = aktualny dzien tygodnia
    dtyg1 = time.localtime()
    dtyg2 = time.strftime("%w", dtyg1)
    ndow = dzien[int(dtyg2)]


    #####################################################################
    # CWU
    #####################################################################

    # jezeli flag_grzanie_co = True

    if (ndow in cwu_window_1_days) and (nt >= cwu_window_1_start and nt < cwu_window_1_stop):
        if flag_grzanie_cwu == False:
            # print "CWU START --> OKNO NR 1"
            GrzanieCWU_Start(1, tcwu_window_1, cwu_window_1_stop)
            flag_grzanie_cwu = True

    elif (ndow in cwu_window_2_days) and (nt >= cwu_window_2_start and nt < cwu_window_2_stop):
        if flag_grzanie_cwu == False:
            # print "CWU START --> OKNO NR 2"
            GrzanieCWU_Start(2, tcwu_window_2, cwu_window_2_stop)
            flag_grzanie_cwu = True

    elif (ndow in cwu_window_3_days) and (nt >= cwu_window_3_start and nt < cwu_window_3_stop):
        if flag_grzanie_cwu == False:
            # print "CWU START --> OKNO NR 3"
            GrzanieCWU_Start(3, tcwu_window_3, cwu_window_3_stop)
            flag_grzanie_cwu = True

    elif (ndow in cwu_window_4_days) and (nt >= cwu_window_4_start and nt < cwu_window_4_stop):
        if flag_grzanie_cwu == False:
            # print "CWU START --> OKNO NR 4"
            GrzanieCWU_Start(4, tcwu_window_4, cwu_window_4_stop)
            flag_grzanie_cwu = True

    elif (ndow in cwu_window_5_days) and (nt >= cwu_window_5_start and nt < cwu_window_5_stop):
        if flag_grzanie_cwu == False:
            # print "CWU START --> OKNO NR 5"
            GrzanieCWU_Start(5, tcwu_window_5, cwu_window_5_stop)
            flag_grzanie_cwu = True

    elif (ndow in cwu_window_6_days) and (nt >= cwu_window_6_start and nt < cwu_window_6_stop):
        if flag_grzanie_cwu == False:
            # print "CWU START --> OKNO NR 5"
            GrzanieCWU_Start(6, tcwu_window_6, cwu_window_6_stop)
            flag_grzanie_cwu = True

    else:
        if flag_grzanie_cwu == True:
            # print "CWU STOP"
            GrzanieCWU_Stop()
            flag_grzanie_cwu = False

    if sec_db % TimeIntervalDB == 0:
        #Zapis do bazy danych
        #print 'Reseet sec_db:', sec_db

        logging.info("Zapisano temperatury do bazy danych.")

        sec_db = 0

    sec_tmp = sec_tmp + 1
    sec_db = sec_db + 1
    time.sleep(1)


def destroy():
    ########################################################################################################################
    # Zerowanie przekaznikow
    ########################################################################################################################
    gpio = webiopi.GPIO  # Helper for LOW/HIGH values
    #gpio.setFunction(stycznik_blokada_grzania, gpio.OUT)
    gpio.digitalWrite(stycznik_blokada_grzania, gpio.LOW)
    logging.info("PiConnect zostal zamkniety")


    """