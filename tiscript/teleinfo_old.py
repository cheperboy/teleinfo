#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
api = '/home/pi/teleinfo/teleinfoapp/'
import datetime
import serial
import string
import sys
sys.path.append(api)
from api import createti

##########
# LOGGER #
##########
import logging

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
LOG_FILE = '/home/pi/teleinfo/tiscript/log/teleinfo.log'
os.path.join(os.path.dirname(BASE_DIR), LOG_FILE)


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create a file handler
handler = logging.FileHandler(LOG_FILE)
handler.setLevel(logging.DEBUG)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

logger.debug('started')

"""
Wh. Index option Base.
BASE 011130000 Q 

A. Intensite Instantanee pour les 3 phases
IINST1003KIINST2000I
IINST3 001 K

VA. Puissance apparente triphas e soutiree
S (en VA), arrondi a la dizaine la plus proche
PAPP 00980 2
"""

ser = serial.Serial(
  port='/dev/ttyS0',
  baudrate = 1200,
  stopbits=serial.STOPBITS_ONE,
  bytesize=serial.SEVENBITS
)

try:
    while 1:
        logger.info('While')
        teleinfo = dict([('papp', -1), ('base', -1), ('iinst1', -1), ('iinst2', -1), ('iinst3', -1), ('valid', -1)])
#        print teleinfo
        
        reading = True #End of frame found / all datas are set
        count_valid = 0
        while (reading == True):
            data = ser.readline()
#            print data
            if (string.find(data, 'BASE ') != -1):
                if (data[5:14].isdigit() == True):
                    teleinfo['base'] = int(data[5:14])
                    count_valid += 1
            if (string.find(data, 'IINST1 ') != -1):
                if (data[7:10].isdigit() == True):
                    teleinfo['iinst1'] = int(data[7:10])
                    count_valid += 1
            if (string.find(data, 'IINST2 ') != -1):
                if (data[7:10].isdigit() == True):
                    teleinfo['iinst2'] = int(data[7:10])
                    count_valid += 1
            if (string.find(data, 'IINST3 ') != -1):
                if (data[7:10].isdigit() == True):
                    teleinfo['iinst3'] = int(data[7:10])
                    count_valid += 1
            if (string.find(data, 'PAPP ') != -1):
                if (data[5:10].isdigit() == True):
                    teleinfo['papp'] = int(data[5:10])
                    count_valid += 1
            
            if (count_valid == 5):
                reading = False
                teleinfo['valid'] = 1
                
        logger.info(teleinfo)
        createti(
          datetime.datetime.now(), 
          teleinfo['base'],
          teleinfo['papp'],
          teleinfo['iinst1'],
          teleinfo['iinst2'],
          teleinfo['iinst3'])

       
except KeyboardInterrupt:
    logger.debug('KeyboardInterrupt')
    try:
        ser.close()
        logger.debug('serial.close()')
        sys.exit(0)
    except SystemExit:
        logger.debug('SystemExit')
        os._exit(0)
