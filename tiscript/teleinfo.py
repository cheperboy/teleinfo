#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
logging.basicConfig(filename='/home/pi/teleinfo/tiscript/log/teleinfo.log',level=logging.DEBUG)
logging.info('Started')
import os
#basedir = os.path.abspath(os.path.dirname(__file__))
api = '/home/pi/teleinfo/teleinfoapp/'
import datetime
import serial
import string
import sys
sys.path.append(api)
from api import createti
logging.info('imported lib')

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
        logging.info('While')
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
                
        print teleinfo
        createti(
          datetime.datetime.now(), 
          teleinfo['base'],
          teleinfo['papp'],
          teleinfo['iinst1'],
          teleinfo['iinst2'],
          teleinfo['iinst3'])
        logging.info('while')

       
except KeyboardInterrupt:
    logging.info('KeyboardInterrupt')
    print 'Interrupted'
    try:
        ser.close()
        print 'closed'
        sys.exit(0)
    except SystemExit:
        print 'SystemExit'
        os._exit(0)


   
#ser = serial.Serial('/dev/ttyS0', baudrate=1200, bytesize=serial.SEVENBITS, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, timeout=0, rtscts=1)
