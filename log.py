#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Biblioteka tworzenia logów  
#  



import logging

logging.basicConfig(filename='PiConnect.log',level='WARNING', format='%(levelname)s: %(asctime)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S %a')

logging.warning('Watch out!') # will print a message to the console
logging.info('I told you so') # will not print anything
logging.warning ('TEST')
