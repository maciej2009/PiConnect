#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  PiConnect.py

import os
import time
from datetime import datetime

import webiopi


import MySQLdb


from ReadConfig import DB
from ReadConfig import TimeInterval
from Common import *




def main():	
		
	count = 0
	while count < 9:	
		count = count + 1 
		print str(count) + " " +str(Temp('tZEW'))
		time.sleep(TimeInterval())
		print "db_name = " + DB.db_name 
	return 0

if __name__ == '__main__':
	main()

		










