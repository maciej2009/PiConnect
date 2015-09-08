#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import ConfigParser
import MySQLdb
from webiopi.devices.sensor.onewiretemp import DS18B20




	
def CzujnikID (Czujnik):

	# Odczyt ID czujników z pliku konfiguracyjnego
	
	czujniki = {
				 "tZEW": conf('Czujniki', 'tZEW'),	
				 "tZAS": conf('Czujniki', 'tZAS'),
				 "tBUF" : conf('Czujniki', 'tBUF_GORA'), 	
				 "tBUF_SRODEK" : conf('Czujniki', 'tBUF_SRODEK'), 	
				 "tBUF_DOL" : conf('Czujniki', 'tBUF_DOL'), 	
				 "tWEW_1" : conf('Czujniki', 'tWEW_1'),
				 "tPOW" : conf('Czujniki', 'tPOW'), 		
				 "tCWU" : conf('Czujniki', 'tCWU')
				}			
				
	return czujniki["tZEW"]

		

def DB():		
	""" Odczyt konfiguracji MySQL"""
	
	db_server  = conf('MySQL', 'Server')
	db_name = conf('MySQL', 'DbName')
	db_username = conf('MySQL', 'Username')
	db_password = conf('MySQL', 'Password')
	
	DB.db_name=db_name
	conn = MySQLdb.connect(host=db_server,user=db_username, passwd=db_password,db=db_name)
	print conn.info
	# TBD: check_SQL_connection()
		
	return conn
		
def TimeInterval():
	TimeInterval = conf('General', 'TimeInterval')
	logging.debug('time_interval loaded from conf file:%s' % (TimeInterval))
	return float(TimeInterval)

def conf(opcja,element):
	config = ConfigParser.RawConfigParser()
	config.read ('/home/pi/projects/PiConnect/PiConnect.conf')
	
	return config.get(opcja, element)  
	
#print TimeInterval()
#print CzujnikID("tZEW")
#print Temp("tZEW")

if __name__ == "__main__":
    from ReadConfig import *
	
