#!/usr/bin/python

# SEE http://banjolanddesign.com/logging-well-depth-with-a-raspberry-pi.html

# Python 2.7.9
# RPI act as Master and Arduino act as slave (USB Link)
# Todo : implement timeouts to get out of while() statement if connection is down. SEE : https://pythonadventures.wordpress.com/2012/12/08/raise-a-timeout-exception-after-x-seconds/

BASE = "/home/pi/currentlog/"
LOG = "log/currentlog_script.log"

import os
import sys
sys.path.append(os.path.join(BASE,'website/app'))
from well_model import log_data
import serial
import time
import datetime
import zlib

#___________
#           |
# CONSTANTS |
#___________|


# ----- LOG File -----
ERROR_LOG_FILENAME = os.path.join(BASE, LOG)
# ----- Num capteurs -----
numCapteurs = 2

# ----- Serial Port Config -----
SERIAL_PORT = "/dev/ttyACM0"
BAUDRATE = 9600

# ----- LOG Messages -----
LOG_ERROR = "ERROR messages are different"
LOG_TIMEOUT = "ERROR Response too long"

# ----- Packet start/end -----
startMarker = 60
endMarker = 62
# ----- defined commands -----
commandUPTIME = "<UPTIME>"
commandVALUE = "<VALUE>"
commandVALUES = "<VALUES>"
# ----- Commands not used in production ------
commandREADY = "<ISREADY>" # check if Arduino is Alive
commandREBOOT = "<REBOOT>" #Reboot Arduino

#___________
#           |
# FUNCTIONS |
#___________|

#send a char[] over serial port
def sendToArduino(trame):
    ser.write(trame)

def save_values(values):
    log_data(datetime.datetime.now(), values[0], values[1])
    print str(datetime.datetime.now())+" INFO value 1 : "+values[0] + " value 2 : " + values[1]
    logError("INFO "+str(values))

# read packet on serial port. 
# packet begin with startMarker "<"
# packet end with endMarker ">"
def getTrameFromArduino():
  global startMarker, endMarker
  trame = ""
  inchar = "z" # any value that is not an end- or startMarker
  byteCount = -1 # to allow for the fact that the last increment will be one too many
  
  # wait for the start character
  while  ord(inchar) != startMarker: 
    inchar = ser.read()
#    print inchar

  # save data until the end marker is found
  while ord(inchar) != endMarker:
    if ord(inchar) != startMarker:
      trame = trame + inchar 
      byteCount += 1
    inchar = ser.read()  
 #   print inchar
#  print "trame " + trame
  return(trame)

def sendCommand(command):
    sendToArduino(command)

# receive response from Arduino
# last value shall be sum of other values (check)
# return
# - list of values
# - None if consistancy not OK
def getValues():
    values = list()
    while ser.inWaiting() == 0:
        pass
    trame = getTrameFromArduino()
    trameValues = trame.split(";")[0]
    trameCRC = trame.split(";")[1]

    values = trameValues.split(",")
    if checkCRC(values, trameCRC):
        return values
    logError(LOG_ERROR);
    print LOG_ERROR
    return None

# Open serial port
def initSerial(serPort, baudRate):
    global ser
    ser = serial.Serial(serPort, baudRate)
    time.sleep(2) # give time for Arduino to reboot (else serial connection doesnet work)

def logError(message) :
    with open(ERROR_LOG_FILENAME,'a+') as f:
        f.write(str(datetime.datetime.now())+" "+message+"\n")

def checkCRC(values, arduinoCRC):
    sum = 0
    for value in values :
        sum += int(value)
    if (int(sum) == int(arduinoCRC)) :
        return True
    return False
    

#______________
#              |
# MAIN PROGRAM |
#______________|

#open serial port
ser = serial.Serial()
initSerial(SERIAL_PORT, BAUDRATE)

#get value from Arduino and save it to Database
sendCommand(commandVALUES)
values = getValues()

if values is not None:
    save_values(values)

ser.close #close connection

