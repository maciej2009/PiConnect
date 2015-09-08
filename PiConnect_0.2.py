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

def parReadAll():
    conf = ConfigParser.ConfigParser()
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
        'poziom1' : conf.getint('Piec', 'poziom1'),
        'poziom2' : conf.getint('Piec', 'poziom2'),
        'poziom3' : conf.getint('Piec', 'poziom3'),
        'poziom4' : conf.getint('Piec', 'poziom4'),
        'poziom5' : conf.getint('Piec', 'poziom5'),
        'poziom6' : conf.getint('Piec', 'poziom6'),
        'piec_delta_temp' : conf.getint('Piec','piec_delta_temp'),
        'piec_delta_time' : conf.getint('Piec','piec_delta_time')*60,

        # Pomieszczenia
        'pom1_temp' : int(conf.get('Pomieszczenia', 'pom1_temp')),
        'pom1_hist': float(conf.get('Pomieszczenia', 'pom1_hist')),
        'pom1_nazwa' : conf.get('Pomieszczenia', 'pom1_nazwa')
        }

class Temp():
    #TODO: Usunąć odczy temperatur z pliku tekstowego temperaturki.conf
    conf = ConfigParser.ConfigParser()
    conf.read("PiConnect.conf")

    def __init__(self):


        # self._czuj_zew = self.read(par['czuj_zew'])
        # self._czuj_co_zas = self.read(par['czuj_co_zas'])
        # self._czuj_co_return = self.read(par['czuj_co_return'])
        # self._czuj_buf_top = self.read(par['czuj_buf_top'])
        self._czuj_buf_mid = self.read(par['czuj_buf_mid'])
        # self._czuj_buf_low = self.read(par['czuj_buf_low'])
        self._czuj_wew_01 = self.read(par['czuj_wew_01'])
        # self._czuj_wew_02 = self.read(par['czuj_wew_02'])
        # self._czuj_wew_03 = self.read(par['czuj_wew_03'])
        # self._czuj_wew_04 = self.read(par['czuj_wew_04'])
        # self._czuj_wew_05 = self.read(par['czuj_wew_05'])
        # self._czuj_wew_06 = self.read(par['czuj_wew_06'])
        # self._czuj_wew_07 = self.read(par['czuj_wew_07'])
        # elf._czuj_wew_08 = self.read(par['czuj_wew_08'])
        # self._czuj_wew_09 = self.read(par['czuj_wew_09'])
        # self._czuj_wew_10 = self.read(par['czuj_wew_10'])
        # self._czuj_cwu = self.read(par['czuj_cwu'])
        # self._czuj_cwu_cyr = self.read(par['czuj_cwu_cyr'])
        # self._czuj_zew = self.read(par['czuj_zew'])

    def readall(self):
        # self._czuj_zew = self.read(par['czuj_zew'])
        # self._czuj_co_zas = self.read(par['czuj_co_zas'])
        # self._czuj_co_return = self.read(par['czuj_co_return'])
        # self._czuj_buf_top = self.read(par['czuj_buf_top'])
        self._czuj_buf_mid = self.read(par['czuj_buf_mid'])
        # self._czuj_buf_low = self.read(par['czuj_buf_low'])
        self._czuj_wew_01 = self.read(par['czuj_wew_01'])
        # self._czuj_wew_02 = self.read(par['czuj_wew_02'])
        # self._czuj_wew_03 = self.read(par['czuj_wew_03'])
        # self._czuj_wew_04 = self.read(par['czuj_wew_04'])
        # self._czuj_wew_05 = self.read(par['czuj_wew_05'])
        # self._czuj_wew_06 = self.read(par['czuj_wew_06'])
        # self._czuj_wew_07 = self.read(par['czuj_wew_07'])
        # self._czuj_wew_08 = self.read(par['czuj_wew_08'])
        # self._czuj_wew_09 = self.read(par['czuj_wew_09'])
        # self._czuj_wew_10 = self.read(par['czuj_wew_10'])
        # self._czuj_cwu = self.read(par['czuj_cwu'])
        # self._czuj_cwu_cyr = self.read(par['czuj_cwu_cyr'])
        # self._czuj_zew = self.read(par['czuj_zew'])


    def read(self, czujnik):



        # Odczyt temperatury z czujnika o ID
        # device = DS18B20(czujnik)
        # return float(device.getCelsius())

        #TODO: Usunąć odczy temperatur z pliku tekstowego temperaturki.conf
        conf = ConfigParser.ConfigParser()
        conf.read("PiConnect.conf")

        t = conf.getfloat('Temp',czujnik)
        return t

class Log():
    def __init__(self):
        logging.basicConfig(filename='PiConnect.log', level=par['log_loginglevel'], format='%(levelname)s: %(asctime)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S %a', filemode='w')
        # Log.debug("[LOG] - Ustawiono poziom logowania: LoggingLevel = %s" % par['log_loginglevel)

    def debug(self, text, modul = 'XXX'):
        modul = modul.upper()
        s = '[%s] - %s' % (modul,text)
        logging.debug(s)
        print '[DEBUG]' + s

    def info(self, text, modul = 'XXX'):
        modul = modul.upper()
        s = '[%s] - %s' % (modul,text)
        logging.debug(s)
        print '[INFO]' + s

    def error(self, text, modul = 'XXX'):
        modul = modul.upper()
        s = '[%s] - %s' % (modul,text)
        logging.error(s)
        print '[ERROR]' + s

    def warning(self, text, modul = 'XXX'):
        modul = modul.upper()
        s = '[%s] - %s' % (modul,text)
        logging.warning(s)
        print '[WARNING]' + s

class DB():
    def __init__(self):
        log = Log()
        global _conn
        #_conn = MySQLdb.connect(host=par['db_server'], user=par['db_username'], passwd=par['db_password'], db=par['db_name'])
        log.debug('Podłaczono do bazy danych', 'db')
        pass

    def zapisTemp(self):
        temp = Temp()

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
            Log().debug("Stycznik nr %s został wyłączony" % self.stycz, 'STYCZNIK')
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
            # Rpi: gpio.setFunction(par['_st_grzalka_1'], gpio.OUT)
            # Rpi: gpio.digitalWrite(par['_st_grzalka_1'], gpio.LOW)
            #print "Reset stycznika nr %s: _st_grzalka_1" % par['_st_grzalka_1']
            pass

        if par['st_grzalka_2'] not in ['0'," ",""]:
            # Rpi: gpio.setFunction(par['_st_grzalka_2'], gpio.OUT)
            # Rpi: gpio.digitalWrite(par['_st_grzalka_2'], gpio.LOW)
            #print "Reset stycznika nr %s: _st_grzalka_2" % par['_st_grzalka_2']
            pass

        if par['st_grzalka_3'] not in ['0'," ",""]:
            # Rpi: gpio.setFunction(par['_st_grzalka_3'], gpio.OUT)
            # Rpi: gpio.digitalWrite(par['_st_grzalka_3'], gpio.LOW)
            #print "Reset stycznika nr %s: _st_grzalka_3" % par['_st_grzalka_3']
            pass

        if par['st_cwu_pompa_cyr'] not in ['0'," ",""]:
            # Rpi: gpio.setFunction(par['st_cwu_pompa_cyr'], gpio.OUT)
            # Rpi: gpio.digitalWrite(par['st_cwu_pompa_cyr'], gpio.LOW)
            #print "Reset stycznika nr %s: st_cwu_pompa_cyr" % par['st_cwu_pompa_cyr']
            pass
        Log().debug('Zresetowano konfigurację wszystkich styczników', 'STYCZNIK')


class Zawor_Trojdrogowy():

    temp_zasilania_zadana = 21

    def __init__(self):
        pass


class Piec():

    parReadAll()

    _st_blokada_grzania = Stycznik(par['st_taryfa'])

    _st_grzalka_1 = Stycznik(par['st_grzalka_1'])
    _st_grzalka_2 = Stycznik(par['st_grzalka_2'])
    _st_grzalka_3 = Stycznik(par['st_grzalka_3'])

    _moc = 0
    _taryfa_nr = 0
    _poziom = 0
    _piec_temp_zadana = 0
    _piec_histereza = 0
    _podgrzej_CWU = False            # Czy grzeje dla CWU?
    _podgrzej_CO = False             # Czy grzeje dla CO?
    _podgrzewam_CWU = False            # Czy grzeje dla CWU?
    _podgrzewam_CO = False             # Czy grzeje dla CO?
    i = 0

    def __init__(self):

        self.temp = Temp()

        self._st_blokada_grzania = Stycznik(par['st_taryfa'])
        self._st_grzalka_1 = Stycznik(par['st_grzalka_1'])
        self._st_grzalka_2 = Stycznik(par['st_grzalka_2'])
        self._st_grzalka_3 = Stycznik(par['st_grzalka_3'])

        self.temp_pocz_zbiornika = self.temp._czuj_buf_mid
        self.delta = 0

    def on (self, temp_zadana, histereza, cel, poziom = 1):   # źródło = CWU, CO
        i = 0

        self.temp.readall()

        if cel == 'CWU':
            print "Cel: Podgrzej CWU   =",self._podgrzej_CWU
        elif cel == 'CO':
            print "Cel: Podgrzej CO    =",self._podgrzej_CO
        else:
            print 'Cel: Brak celu właczenia pieca'



        print self.i, "Cel: %s, T.Buf: %s, T. zadana: %s, Hist: %s, T. pocz: %s, Delta: %s, Grzeję: %s" % (cel,self.temp._czuj_buf_mid, temp_zadana, histereza, self.temp_pocz_zbiornika, self.delta, Piec._poziom)

        if  self.temp._czuj_buf_mid <= temp_zadana - histereza:     # piec pracuje

            if Piec._podgrzej_CWU == True:
                Piec._podgrzewam_CWU = True
            elif Piec._podgrzej_CO == True:
                Piec._podgrzewam_CO = True


            self.delta = self.temp._czuj_buf_mid - self.temp_pocz_zbiornika


            if poziom <> Piec._poziom :

                zmieniono = True
                self.i = 0
                self.delta = 0
            else:
                zmieniono = False

            if zmieniono is True:
                self.taryfa2()      # odczytaj taryfę i parametry taryfy

                if poziom == 1:            # 3kW
                    self._st_grzalka_1.on()
                    self._st_grzalka_2.off()
                    self._st_grzalka_3.off()
                    self._moc = 3

                elif poziom == 2:           # 6kW
                    self._st_grzalka_1.off()
                    self._st_grzalka_2.on()
                    self._st_grzalka_3.off()
                    self._moc = 6

                elif poziom == 3:           # 9kW
                    self._st_grzalka_1.off()
                    self._st_grzalka_2.off()
                    self._st_grzalka_3.on()
                    self._moc = 9

                elif poziom == 4:           # 12kW
                    self._st_grzalka_1.on()
                    self._st_grzalka_2.off()
                    self._st_grzalka_3.on()
                    self._moc = 12

                elif poziom == 5:           # 15kW
                    self._st_grzalka_1.off()
                    self._st_grzalka_2.on()
                    self._st_grzalka_3.on()
                    self._moc = 15

                elif poziom == 6:           # 18kW
                    self._st_grzalka_1.on()
                    self._st_grzalka_2.on()
                    self._st_grzalka_3.on()
                    self._moc = 18

                Piec._poziom = poziom


                if Piec._podgrzewam_CWU ==True and Piec._podgrzewam_CO == False:
                    Log().debug("Włączono grzanie na poziomie %s z mocą %s kW. Okres grzewczy: %s. Temp zbiornika: %s. Temp zadana: %s. Histereza: +/- %s." % (
                        Piec._poziom, self._moc, par['okresgrzewczy'], self.temp._czuj_buf_mid, self._piec_temp_zadana, histereza), 'CWU')
                if Piec._podgrzewam_CWU ==False and Piec._podgrzewam_CO == True:
                    Log().debug("Włączono grzanie na poziomie %s z mocą %s kW. Okres grzewczy: %s. Temp zbiornika: %s. Temp zadana: %s. Histereza: +/- %s." % (
                        Piec._poziom, self._moc, par['okresgrzewczy'], self.temp._czuj_buf_mid, self._piec_temp_zadana, histereza), 'CO')
                """
                if Piec._poziom != poziom:   # zapis do tabeli "piec" jezeli nastapiła zmiana poziomu

                    #try:
                    # conn.open
                    conn.begin()

                    if Piec._poziom == 0 or Piec._poziom == None:        # gdy właczamy piec, a nie zmieniamy wartość poziomu
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

                Piec._poziom = poziom
                """


            self._piec_temp_zadana = temp_zadana
            self._piec_histereza = histereza


            if self.i % par['piec_delta_time'] == 0:            # pętla do mierzenia przyrostu/spadku temperatury

                self.i = 0

                self.temp_pocz_zbiornika = self.temp._czuj_buf_mid  # na nowo przypisz temp. pocz


                # jezeli temperatura spada to zwieksz poziom

                if self.delta  <= -par['piec_delta_temp']:
                    self.zwieksz_moc(temp_zadana, histereza)

                if self.delta  >= par['piec_delta_temp']:
                    self.zmniejsz_moc(temp_zadana, histereza)

        elif self.temp._czuj_buf_mid >= temp_zadana + histereza:

            if Piec._poziom <>0:
                self.off()
                Piec._podgrzej_CWU = False
                Piec._podgrzej_CO = False
                Piec._podgrzewam_CWU = False
                Piec._podgrzewam_CO = False



        self.i = self.i + 1


    def off(self):

        wylacz_wszystkie_grzalki = False

        if self._podgrzej_CWU is True:
            zrodlo = 'CWU'
            # print "######################  wyłaczam podgrzewanie pieca dla CWU"

            Log().debug("[PIEC][CWU] - Wyłączono grzanie. Okres grzewczy: %s. Temp zbiornika: %s. Temp zadana: %s. Histereza: +/- %s." % (
                            par['okresgrzewczy'], self.temp._czuj_buf_mid, self._piec_temp_zadana, self._piec_histereza))

            self._podgrzej_CWU = False
            wylacz_wszystkie_grzalki = True

        elif self._podgrzej_CO is True:
            zrodlo = 'CO'
            # print "######################  wyłaczam podgrzewanie pieca dla CWU"

            Log().debug("[PIEC][CO] - Wyłączono grzanie. Okres grzewczy: %s. Temp zbiornika: %s. Temp zadana: %s. Histereza: +/- %s." % (
                            par['okresgrzewczy'], self.temp._czuj_buf_mid, self._piec_temp_zadana, self._piec_histereza))

            self._podgrzej_CO = False
            wylacz_wszystkie_grzalki = True

        if wylacz_wszystkie_grzalki is True:
            self._st_grzalka_1.off()
            self._st_grzalka_2.off()
            self._st_grzalka_3.off()

            self._moc = 0
            Piec._poziom = 0

            Piec._podgrzej_CWU = False
            Piec._podgrzej_CO = False
            Piec._podgrzewam_CWU = False
            Piec._podgrzewam_CO = False
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

    def zwieksz_moc (self, temp_zadana, histereza):

        if self._podgrzej_CWU == True and self._podgrzej_CO  == False:
            zrodlo = 'CWU'
        elif self._podgrzej_CO  == True and self._podgrzej_CWU  == False:
            zrodlo = 'CO'
        else:
            zrodlo = 'XXX'

        akt_poziom = Piec._poziom
        akt_moc = self._moc

        if Piec._poziom == 0:
            self.on(temp_zadana, histereza, 1)
        elif Piec._poziom == 1:
            self.on(temp_zadana, histereza, 2)
        elif Piec._poziom == 2:
            self.on(temp_zadana, histereza, 3)
        elif Piec._poziom == 3:
            self.on(temp_zadana, histereza, 4)
        elif Piec._poziom == 4:
            self.on(temp_zadana, histereza, 5)
        elif Piec._poziom == 5:
            self.on(temp_zadana, histereza, 6)

        if akt_poziom < 6:
            Log().debug("[PIEC] - Zwiększono poziom z %s na %s (z %s kW na %s kW)" % ( akt_poziom, Piec._poziom, akt_moc, self._moc),'CWU')
        else:
            Log().debug("[PIEC] - Nie można już zwiększyć poziomu pracy pieca", zrodlo)
            pass

    def zmniejsz_moc (self, temp_zadana, histereza, cel):

        akt_poziom = Piec._poziom
        akt_moc = self._moc

        if Piec._poziom == 0:
            pass
        elif Piec._poziom == 1:
            pass
            #self.off()
        elif Piec._poziom == 2:
            self.on(temp_zadana, histereza, 1, cel)
        elif Piec._poziom == 3:
            self.on(temp_zadana, histereza, 2, cel)
        elif Piec._poziom == 4:
            self.on(temp_zadana, histereza, 3, cel)
        elif Piec._poziom == 5:
            self.on(temp_zadana, histereza, 4, cel)
        elif Piec._poziom == 6:
            self.on(temp_zadana, histereza, 5, cel)


        if akt_poziom >= 2 and akt_poziom <= 6:
            Log().debug("[PIEC] - Zmniejszam poziom z %s na %s (z %s kW na %s kW)" % (akt_poziom, Piec._poziom, akt_moc, self._moc), cel)

        else:
            Log().debug("[PIEC] - Nie można już zmniejszyć poziomu grzania" , cel)

    def status (self):
        if Piec._poziom != 0 and Piec._poziom != None:
            return True
        else:
            return False

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
            self._taryfa_nr = 2
            self._taryfa_okno = 1
            self._taryfa_pln = par['taryfa2_cena']

        elif dt in par['taryfa2_2_dni'] and czas  >= par['taryfa2_2_godz_start'] and czas < par['taryfa2_2_godz_stop']:
            self._taryfa_nr = 2
            self._taryfa_okno = 2
            self._taryfa_pln = par['taryfa2_cena']

        elif dt in par['taryfa2_3_dni'] and czas  >= par['taryfa2_3_godz_start'] and czas < par['taryfa2_3_godz_stop']:
            self._taryfa_nr = 2
            self._taryfa_okno = 3
            self._taryfa_pln = par['taryfa2_cena']

        elif dt in par['taryfa2_4_dni'] and czas  >= par['taryfa2_4_godz_start'] and czas < par['taryfa2_4_godz_stop']:
            self._taryfa_nr = 2
            self._taryfa_okno = 4
            self._taryfa_pln = par['taryfa2_cena']

        elif dt in par['taryfa2_5_dni'] and czas  >= par['taryfa2_5_godz_start'] and czas < par['taryfa2_5_godz_stop']:
            self._taryfa_nr = 2
            self._taryfa_okno = 5
            self._taryfa_pln = par['taryfa2_cena']

        elif dt in par['taryfa2_6_dni'] and czas  >= par['taryfa2_6_godz_start'] and czas < par['taryfa2_6_godz_stop']:
            self._taryfa_nr = 2
            self._taryfa_okno = 6
            self._taryfa_pln = par['taryfa2_cena']

        else:
            self._taryfa_nr = 1
            self._taryfa_okno = 0
            self._taryfa_pln = par['taryfa1_cena']

class CWU():

    _status = False
    _okno_numer = None
    _okno_start = None
    _okno_stop = None
    _piec_temp_zadana = 0                    # temperatura dyspozycyjna/zadana pieca. zadana dla CWU
    _piec_temp_histereza = 0                 # histereza dla temperatury dyspozycyjnej w zbiorniku

    def __init__(self):

        self.piec = Piec()
        self.temp = Temp()
        self._status = False
        self._okno_numer = None
        self._okno_start = None
        self._okno_stop = None
        self._piec_temp_zadana = 0  # temperatura dyspozycyjna. zadana dla CWU
        self._piec_temp_histereza = 0  # histereza dla temperatury dyspozycyjnej w zbiorniku

    def sprawdz_czy_wlaczyc(self):

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
            self._okno_numer = 1
            self._okno_start = par['cwu_okno_1_start']
            self._okno_stop = par['cwu_okno_1_stop']
            self._piec_temp_zadana = par['cwu_okno_1_temp']
            self._piec_temp_histereza = par['cwu_okno_1_hist']

        elif dt in par['cwu_okno_2_days'] and czas  >= par['cwu_okno_2_start'] and czas <= par['cwu_okno_2_stop']:
            self._status = True
            self._okno_numer = 2
            self._okno_start = par['cwu_okno_2_start']
            self._okno_stop = par['cwu_okno_2_stop']
            self._piec_temp_zadana = par['cwu_okno_2_temp']
            self._piec_temp_histereza = par['cwu_okno_2_hist']

        elif dt in par['cwu_okno_3_days'] and czas  >= par['cwu_okno_3_start'] and czas <= par['cwu_okno_3_stop']:
            self._status = True
            self._okno_numer = 3
            self._okno_start = par['cwu_okno_3_start']
            self._okno_stop = par['cwu_okno_3_stop']
            self._piec_temp_zadana = par['cwu_okno_3_temp']
            self._piec_temp_histereza = par['cwu_okno_3_hist']

        elif dt in par['cwu_okno_4_days'] and czas  >= par['cwu_okno_4_start'] and czas <= par['cwu_okno_4_stop']:
            self._status = True
            self._okno_numer = 4
            self._okno_start = par['cwu_okno_4_start']
            self._okno_stop = par['cwu_okno_4_stop']
            self._piec_temp_zadana = par['cwu_okno_4_temp']
            self._piec_temp_histereza = par['cwu_okno_4_hist']

        elif dt in par['cwu_okno_5_days'] and czas  >= par['cwu_okno_5_start'] and czas <= par['cwu_okno_5_stop']:
            self._status = True
            self._okno_numer = 5
            self._okno_start = par['cwu_okno_5_start']
            self._okno_stop = par['cwu_okno_5_stop']
            self._piec_temp_zadana = par['cwu_okno_5_temp']
            self._piec_temp_histereza = par['cwu_okno_5_hist']

        elif dt in par['cwu_okno_6_days'] and czas  >= par['cwu_okno_6_start'] and czas <= par['cwu_okno_6_stop']:
            self._status = True
            self._okno_numer = 6
            self._okno_start = par['cwu_okno_6_start']
            self._okno_stop = par['cwu_okno_6_stop']
            self._piec_temp_zadana = par['cwu_okno_6_temp']
            self._piec_temp_histereza = par['cwu_okno_6_hist']

        else:
            self._status = False
            self._okno_numer = None
            self._okno_start = None
            self._okno_stop = None
            self._piec_temp_zadana = None
            self._piec_temp_histereza = 0

        if self._status == True:
            Piec._podgrzej_CWU = True
            #self.piec._podgrzej_CO = False

        if self._status == False:
            Piec._podgrzej_CWU = False
            #self.piec._podgrzej_CO = False


        if Piec._podgrzej_CWU == True:
            if Piec._poziom <> 0:
                self.piec.on(self._piec_temp_zadana, self._piec_temp_histereza, 'CWU', Piec._poziom)

            else:
                self.piec.on(self._piec_temp_zadana, self._piec_temp_histereza, 'CWU', 1)

class CO():

    _status = False
    _okno_nr = None
    _okno_start = None
    _okno_stop = None
    _piec_temp_zadana = 0                    # temperatura dyspozycyjna/zadana pieca. zadana dla CWU
    _piec_histereza = 0                 # histereza dla temperatury dyspozycyjnej w zbiorniku

    _print_blokada_pompy_CO = False
    _pompa_co_wlaczona = False
    _temp_zasilania_CO = 0

    stycz_pompa = Stycznik(par['st_co_pompa'])

    def __init__(self):

        self.piec = Piec()
        self.temp = Temp()
        self.cwu = CWU()

        self._status = False
        self._okno_nr = 0
        self._okno_start = None
        self._okno_stop = None
        self._piec_temp_zadana = 0  # temperatura dyspozycyjna. zadana dla CWU
        self._piec_histereza = 0  # histereza dla temperatury dyspozycyjnej w zbiorniku
        self.stycz_pompa = Stycznik(par['st_co_pompa'])
        self._print_blokada_pompy_CO = False
        self._pompa_co_wlaczona = False
        self._temp_zasilania_CO = 0


    def sprawdz_czy_wlaczyc(self):

        if par['okresgrzewczy'] == True:

            dzien = {0: 'NI', 1: 'PO', 2: 'WT', 3: 'SR', 4: 'CZ', 5: 'PI', 6: 'SO'}

            # nt = aktualny czas = nowtime
            czas = time.localtime()
            czas = time.strftime("%H:%M", czas)

            # ndow = NowDayOfWeek = aktualny dzien tygodnia
            dtyg1 = time.localtime()
            dtyg2 = time.strftime("%w", dtyg1)
            dt = dzien[int(dtyg2)]

            if dt in par['co_okno_1_days'] and czas  >= par['co_okno_1_start'] and czas <= par['co_okno_1_stop']:
                self._status = True
                self._okno_nr = 1
                self._okno_start = par['co_okno_1_start']
                self._okno_stop = par['co_okno_1_stop']
                self._piec_temp_zadana = par['co_okno_1_temp']
                self._piec_histereza = par['co_okno_1_hist']

            elif dt in par['co_okno_2_days'] and czas  >= par['co_okno_2_start'] and czas <= par['co_okno_2_stop']:
                self._status = True
                self._okno_nr = 2
                self._okno_start = par['co_okno_2_start']
                self._okno_stop = par['co_okno_2_stop']
                self._piec_temp_zadana = par['co_okno_2_temp']
                self._piec_histereza = par['co_okno_2_hist']

            elif dt in par['co_okno_3_days'] and czas  >= par['co_okno_3_start'] and czas <= par['co_okno_3_stop']:
                self._status = True
                self._okno_nr = 3
                self._okno_start = par['co_okno_3_start']
                self._okno_stop = par['co_okno_3_stop']
                self._piec_temp_zadana = par['co_okno_3_temp']
                self._piec_histereza = par['co_okno_3_hist']

            elif dt in par['co_okno_4_days'] and czas  >= par['co_okno_4_start'] and czas <= par['co_okno_4_stop']:
                self._status = True
                self._okno_nr = 4
                self._okno_start = par['co_okno_4_start']
                self._okno_stop = par['co_okno_4_stop']
                self._piec_temp_zadana = par['co_okno_4_temp']
                self._piec_histereza = par['co_okno_4_hist']

            elif dt in par['co_okno_5_days'] and czas  >= par['co_okno_5_start'] and czas <= par['co_okno_5_stop']:
                self._status = True
                self._okno_nr = 5
                self._okno_start = par['co_okno_5_start']
                self._okno_stop = par['co_okno_5_stop']
                self._temp = par['co_okno_5_temp']
                self._piec_histereza = par['co_okno_5_hist']

            elif dt in par['co_okno_6_days'] and czas  >= par['co_okno_6_start'] and czas <= par['co_okno_6_stop']:
                self._status = True
                self._okno_nr = 6
                self._okno_start = par['co_okno_6_start']
                self._okno_stop = par['co_okno_6_stop']
                self._piec_temp_zadana = par['co_okno_6_temp']
                self._piec_histereza = par['co_okno_6_hist']

            else:
                self._status = False
                self._okno_nr = 0
                self._okno_start = None
                self._okno_stop = None
                self._piec_temp_zadana = None
                self._piec_histereza = None



            #TODO: Wstawić ustalenie temperatury zasilania na podsatwie krzywej grzewczej. Ma znadac wartosć self._temp_zasilania_CO
            self.temp.readall()
            self._temp_zasilania_CO = 31

            if self.temp._czuj_buf_mid >= self._temp_zasilania_CO:  # jeżeli temperatura zbiornika jest wyższa od żądanej temp zasilania CO

                if (par['pom1_temp'] - par['pom1_hist']) > self.temp._czuj_wew_01:

                    if self._pompa_co_wlaczona == False:
                        Log().debug("Włączam pompę CO. Temperatura pomieszczenia %s jest mniejsza od Temp. zadanej %s. Temp. zasilania = %s" % (self.temp._czuj_wew_01, par['pom1_temp'], self._temp_zasilania_CO),'CO POMPA')
                        self.pompa_co_on()
                        self._pompa_co_wlaczona = True

                elif(par['pom1_temp'] + par['pom1_hist']) < self.temp._czuj_wew_01:

                    if self._pompa_co_wlaczona == True:
                        Log().debug("Wyłączam pompę CO. Temperatura pomieszczenia %s jest większa od Temp. zadanej %s. Temp. zasilania = %s" % (self.temp._czuj_wew_01, par['pom1_temp'], self._temp_zasilania_CO), 'CO POMPA')
                        self.pompa_co_off()
                        self._pompa_co_wlaczona = False

            else:    # jeżeli temperatura zbiornika jest NIZSZA od żądanej temp zasilania CO

                Log().debug("Nie mogę włączyć pompy CO. Temperatura bufora %s jest za niska by uzyskać Temp. zasilania %s" % (self.temp._czuj_buf_mid, self._temp_zasilania_CO),'CO POMPA')
                self.pompa_co_off()


    def pompa_co_on(self):

        if self._pompa_co_wlaczona ==False:
            self.stycz_pompa.on()
            Log().debug("Pompa CO została włączona",'CO POMPA')
            self._pompa_co_wlaczona = True

    def pompa_co_off(self):
        if self._pompa_co_wlaczona== True:
            self.stycz_pompa.off()
            Log().debug("Pompa CO została wyłączona",'CO POMPA')
            self._pompa_co_wlaczona = False


def setup():
    parReadAll()
    Log().info('Dzień dobry. Uruchamiam system PiConnect', 'SYSTEM')

    st = Stycznik()
    st.reset_all()

    loop()


def loop():
    parReadAll()

    log = Log()
    temp = Temp()
    db = DB()
    st = Stycznik()

    db.zapisTemp()

    cwu = CWU()
    co = CO()

    while 1:
        temp.readall()


        cwu.sprawdz_czy_wlaczyc()
        co.sprawdz_czy_wlaczyc()

        time.sleep(1)




setup()


