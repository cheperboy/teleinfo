import os, sys, argparse, string, datetime
import logging, logging.config
import serial
from serial.serialutil import SerialException

PORT = '/dev/ttyS0'
BAUDRATE = 1200
STOPBITS = serial.STOPBITS_ONE
BYTESIZE = serial.SEVENBITS

currentpath = os.path.abspath(os.path.dirname(__file__)) # /home/pi/Development/teleinfo/tiscript
projectpath = os.path.dirname(currentpath)               # /home/pi/Development/teleinfo
envpath = os.path.dirname(projectpath)                   # /home/pi/Development
envname = os.path.basename(envpath)                      # Development

#logfile_base = '/home/pi/Development/teleinfo/tiscript/log/teleinfo.py'
logfile_base = projectpath + '/log/tiscript'

api = projectpath + '/teleinfoapp/'
sys.path.append(api)
from api import createti
'''
logging.critical(os.path.basename(__file__))
logging.error("ERROR")
logging.warning("WARNING")
logging.info("INFO")
logging.debug("DEBUG")
'''

def main():
    logger.info('Start')
    EDFserial = serial.Serial(port = PORT,baudrate = BAUDRATE, stopbits = STOPBITS, bytesize = BYTESIZE)

    try:
        while True:
            teleinfo = readPort(EDFserial)
            createti(
                      datetime.datetime.now(), 
                      teleinfo['base'],
                      teleinfo['papp'],
                      teleinfo['iinst1'],
                      teleinfo['iinst2'],
                      teleinfo['iinst3']
                    )
    except KeyboardInterrupt:
        logger.debug('KeyboardInterrupt')
        try:
            EDFserial.close()
            logger.debug('serial.close()')
            sys.exit(0)
        except SystemExit:
            logger.debug('SystemExit')
            os._exit(0)

def readPort(EDFserial):
    logger.debug('readSerial()')
    teleinfo = dict([('papp', -1), ('base', -1), ('iinst1', -1), ('iinst2', -1), ('iinst3', -1), ('valid', -1)])
    reading = True #End of frame found / all datas are set
    count_valid = 0
    while (reading == True):
        try:
            data = EDFserial.readline()
        except SerialException:
            logger.error('SerialException, closing port and EXIT', exc_info=True)
            EDFserial.close()
            sys.exit(0)

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
    return (teleinfo)


if __name__ == '__main__':
    
    # PARSE ARGS
    parser = argparse.ArgumentParser(description = "Rpi gets teleinfo from EDF serial output", epilog = "" )
    parser.add_argument("-v",
                          "--verbose",
                          help="increase output verbosity",
                          action="store_true")
    args = parser.parse_args()

    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.CRITICAL
    
    # SET LOGGER
    logger = logging.getLogger(__name__)
    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": "%(asctime)s | %(name)s | %(filename)s | %(funcName)s | %(levelname)s | %(message)s"
            }
        },

        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": loglevel,
                "formatter": "simple",
                "stream": "ext://sys.stdout"
            },

            "info_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "simple",
                "filename": logfile_base + "_info.log",
                "maxBytes": 100000,
                "backupCount": 3,
                "encoding": "utf8"
            },

            "error_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "simple",
                "filename": logfile_base + "_errors.log",
                "maxBytes": 100000,
                "backupCount": 3,
                "encoding": "utf8"
            }
        },

        "loggers": {
            "my_module": {
                "level": "ERROR",
                "handlers": ["console"],
                "propagate": "no"
            }
        },

        "root": {
            "level": "INFO",
            "handlers": ["console", "info_file_handler", "error_file_handler"]
        }
    })

    # CALL MAIN
    main()
