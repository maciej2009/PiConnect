#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  bez nazwy.py
#  
#  Copyright 2014  <pi@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
from webiopi.devices.sensor.onewiretemp import DS18B20
from ReadConfig import conf
import logging


class czujnik(object):

	def __init__(self, symbol): 
		#print symbol
		
		
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
		self.ID = czujniki[symbol]
		#print self.ID
		
		
	def Temp (self):
		# Odczyt temperatury z czujnika o ID
		try:
			device = DS18B20(self.ID)
			return device.getCelsius()
		except:
			#dorobić PASS
			pass
			
def Log(text, severity="E"):
	#Konfiguracja danych loggingu

	LoggingLevel = conf('General','LoggingLevel')
	self.basicConfig(filename='PiConnect.log',level=LoggingLevel, format='dupa: %(levelname)s: %(asctime)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S %a')
	
	if severity == "E":
		logging.error (text):
	elif severity == "W":
		logging.warning (text):
	elif severity == "D":
		logging.debug (text):
	elif severity == "C":
		logging.critical (text):
	elif severity == "I":
		logging.info (text):
	

		
						
c1 = czujnik("tZEW")
c2 = czujnik("tZAS")
print c1.ID
print c2.ID
print c2.Temp()
#print LoggingLevel
l=Log()

l.Warning("SSSS")
l.Debug("SSSS")
