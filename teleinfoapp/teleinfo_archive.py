'''
Summary:
python script used to store average values (Minutes, Hour, ...) of Teleino SQLA Database.
supposed to be run every 10 minutes by cron

CLI Usage :
workon venv
python teleinfo_archive.py --archive_hour

CRON Config :
python teleinfo_archive.py --archive_hour

Description
Database Model and usefull models methods are imported from teleinfoapp (app.models and app.models_util)
Le fait d'appeler l'option --archive_hour provoque d'abord l'appel de archive_minute

'''


import os, sys, argparse
import logging, logging.config

from app import db
from app.models import Teleinfo, TeleinfoMinute, TeleinfoHour
from datetime import datetime, timedelta
from app.models_util import TIHour, TIMinute, TI

currentpath = os.path.abspath(os.path.dirname(__file__)) # /home/pi/Development/teleinfo/teleinfoapp
projectpath = os.path.dirname(currentpath)               # /home/pi/Development/teleinfo
envpath = os.path.dirname(projectpath)                   # /home/pi/Development
envname = os.path.basename(envpath)                      # Development

logfile_base = projectpath + '/log/tiarchive'


def process_archive_hour():
    logger.debug('process_archive_hour()')
    # defini date de debut et de fin 
    # begin = (date du dernier record de la base Archive) + 1 heure
    # end = (maintenant) - 1 heure
    
    # if TeleinfoHour is empty then we start with the first TeleinfoMinute record (oldest)
    if TIHour.get_last() == None:
        begin = TIMinute.get_first().timestamp.replace(minute=0, second=0, microsecond=0)

    # else TeleinfoHour is NOT empty then we start with the last TeleinfoHour record (newest)
    else:
        begin = (TIHour.get_last().timestamp + timedelta(minutes=60)).replace(minute=0, second=0, microsecond=0)
    
    # we finish with the last TeleinfoMinute record (just 1 hour older than the last one to be sure to have a complete hour)
    end = TIMinute.get_last().timestamp.replace(minute=0, second=0, microsecond=0)
    logger.info('Hour to archive ' + str(begin) + ' -> ' + str(end))
    if ((begin + timedelta(minutes=60)) > end):
        logger.info('\tWaiting more records')

    # while some old Logs to Archive
    while ((begin + timedelta(minutes=60)) <= end):
        record_hour(begin)
        begin = begin + timedelta(minutes=60)

def record_hour(begin):
    logger.debug('record_hour('+ str(begin) +')')
    #fake begin/end
#    begin = datetime.now() - timedelta(minutes=3)
    
    end = begin + timedelta(minutes=60)
    logger.info('Archiving hour ' + str(begin) + ' -> ' + str(end))
    base = 0
    papp = 0
    iinst1 = 0
    iinst2 = 0
    iinst3 = 0
    # get logs
    logs = TIMinute.get_between_date(begin, end)
    nb_logs = len(logs)
    logger.debug('nb_logs ' + str(nb_logs))
    if nb_logs>0:
        for log in logs:
            if log.base > base: base = log.base # valeur la plus elevee de la serie
            papp += log.papp
            iinst1 += log.iinst1
            iinst2 += log.iinst2
            iinst3 += log.iinst3
        timestamp = begin
        # calcule des moyennes sur les series
        papp = papp / nb_logs
        iinst1 = iinst1 / nb_logs
        iinst2 = iinst2 / nb_logs
        iinst3 = iinst3 / nb_logs
        # Save to db
        ret = TIHour.create(begin, base, papp, iinst1, iinst2, iinst3)
        logger.debug('ret : ' + str(ret))


#run every 15 min
def process_archive_minute():
    # defini date de debut et de fin 
    # begin = (date du dernier record de la base Archive) + 1 minute
    # end = (maintenant) - 1 minute
    
    # if TeleinfoMinute is empty then we start with the first Teleinfo record (oldest)
    if TIMinute.get_last() == None:
        #TODO : should be replaced by TI.get_first()
        #begin = db.session.query(Teleinfo).filter().order_by(Teleinfo.id.asc()).first().timestamp.replace(second=0, microsecond=0) 
        begin = TI.get_first().timestamp.replace(second=0, microsecond=0) 

    # else TeleinfoMinute is NOT empty then we start with the last TeleinfoMinute record (newest)
    else:
        begin = (TIMinute.get_last().timestamp + timedelta(minutes=1)).replace(second=0, microsecond=0)
    
    # we finish with the last Teleinfo record (replace second to zero to avoid incomplete current minute)
    end = (TI.get_last().timestamp).replace(second=0, microsecond=0)
    logger.info('Minute to archive ' + str(begin) + ' -> ' + str(end))
    
    if ((begin + timedelta(minutes=1)) > end):
        logger.info('\tWaiting more records')
    # while some old Logs to Archive
    while ((begin + timedelta(minutes=1)) <= end):
        record_minute(begin)
        begin = begin + timedelta(minutes=1)

#ASC : plus ancient 
#DESC : plus recent
'''
recupere dans la base Logs l'ensenmble des objets dont la date est comprise entre 
begin et (begin + 1 minute)
Calcule des moyennes et enregistre
'''
def record_minute(begin):
    logger.debug('\t\trecord minute')
    #fake begin/end
#    begin = datetime.now() - timedelta(minutes=3)
    
    end = begin + timedelta(minutes=1)
    logger.info('Archiving minute ' + str(begin) + ' -> ' + str(end))
    #print('\t\tminute ' + str(begin) + ' -> ' + str(end))
    base = 0
    papp = 0
    iinst1 = 0.0
    iinst2 = 0.0
    iinst3 = 0.0
    # get logs
    logs = TI.get_between_date(begin, end)
    nb_logs = len(logs)
    logger.debug('\t\t\tnb_logs=' + str(nb_logs))
    if nb_logs>0:
        for log in logs:
            if log.base > base: base = log.base # valeur la plus elevee de la serie
            papp += log.papp
            iinst1 += float(log.iinst1)
            iinst2 += float(log.iinst2)
            iinst3 += float(log.iinst3)
        timestamp = begin
        # calcule des moyennes sur les serie
        papp = papp / nb_logs
        iinst1 = iinst1 / nb_logs
        iinst2 = iinst2 / nb_logs
        iinst3 = iinst3 / nb_logs
        # Save to db
        ret = TIMinute.create(begin, base, papp, iinst1, iinst2, iinst3)
        logger.debug('\t\t\tret = ' + str(ret))


if __name__ == '__main__':
    
    # PARSE ARGS
    parser = argparse.ArgumentParser(description = "Archive Teleinfo in Minute and Hour db", epilog = "" )
    parser.add_argument("-v",
                          "--verbose",
                          help="increase output verbosity",
                          action="store_true")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--archive_hour", action="store_true")
    group.add_argument("--archive_minute", action="store_true")
    args = parser.parse_args()

    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.ERROR
    
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
    logger.info('START (last TI recrod = ' + str(TI.get_last().timestamp))
    if args.archive_minute:
        process_archive_minute()
    if args.archive_hour:
        process_archive_minute()
        process_archive_hour()
    