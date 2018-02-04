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

#logfile_base = '/home/pi/Development/teleinfo/tiscript/log/teleinfo.py'
logfile_base = projectpath + '/log/tiarchive'



#run every hour
def process_archive_hour():
    print "process_archive_hour"
    # defini date de debut et de fin 
    # begin = (date du dernier record de la base Archive) + 1 heure
    # end = (maintenant) - 1 heure
    
    # if TeleinfoHour is empty then we start with the first TeleinfoMinute record (oldest)
    if TIHour.get_last() == None:
        begin = db.session.query(TeleinfoMinute).filter().order_by(TeleinfoMinute.id.asc()).first().timestamp.replace(minute=0, second=0, microsecond=0)

    # else TeleinfoHour is NOT empty then we start with the last TeleinfoHour record (newest)
    else:
        begin = (TIHour.get_last().timestamp + timedelta(minutes=60)).replace(minute=0, second=0, microsecond=0)
    
    # we finish with the last TeleinfoMinute record (just 1 hour older than the last one to be sure to have a complete hour)
    end = db.session.query(TeleinfoMinute).order_by(TeleinfoMinute.id.desc()).first().timestamp  - timedelta(minutes=60)
    print "\tbegin="+str(begin)
    print "\tend="+str(end)
    
    # while some old Logs to Archive
    while ((begin + timedelta(minutes=60)) < end):
        record_hour(begin)
        begin = begin + timedelta(minutes=60)

def record_hour(begin):
    print "\t\trecord hour"
    #fake begin/end
#    begin = datetime.now() - timedelta(minutes=3)
    
    print "\t\tbegin="+str(begin)
    end = begin + timedelta(minutes=60)
    print "\t\tend="+str(end)
    base = 0
    papp = 0
    iinst1 = 0
    iinst2 = 0
    iinst3 = 0
    # get logs
    logs = TIMinute.get_between_date(begin, end)
    nb_logs = len(logs)
    print "\t\t\tnb_logs="+str(nb_logs)
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
        print "\t\t\t"+str(ret)


#run every 15 min
def process_archive_minute():
    print "process_archive_minute"
    # defini date de debut et de fin 
    # begin = (date du dernier record de la base Archive) + 1 minute
    # end = (maintenant) - 1 minute
    
    # if TeleinfoMinute is empty then we start with the first Teleinfo record (oldest)
    if TIMinute.get_last() == None:
        begin = db.session.query(Teleinfo).filter().order_by(Teleinfo.id.asc()).first().timestamp.replace(second=0, microsecond=0)

    # else TeleinfoMinute is NOT empty then we start with the last TeleinfoMinute record (newest)
    else:
        begin = (TIMinute.get_last().timestamp + timedelta(minutes=1)).replace(second=0, microsecond=0)
    
    # we finish with the last Teleinfo record (just on minute older than the last one to be sure to have a complete minute)
    end = db.session.query(Teleinfo).order_by(Teleinfo.id.desc()).first().timestamp  - timedelta(minutes=1)
    print "\tbegin="+str(begin)
    print "\tend="+str(end)
    
    # while some old Logs to Archive
    while ((begin + timedelta(minutes=1)) < end):
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
    print "\t\trecord minute"
    #fake begin/end
#    begin = datetime.now() - timedelta(minutes=3)
    
    print "\t\tbegin="+str(begin)
    end = begin + timedelta(minutes=1)
    print "\t\tend="+str(end)
    base = 0
    papp = 0
    iinst1 = 0.0
    iinst2 = 0.0
    iinst3 = 0.0
    # get logs
    logs = TI.get_between_date(begin, end)
    nb_logs = len(logs)
    print "\t\t\tnb_logs="+str(nb_logs)
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
        print "\t\t\t"+str(ret)


if __name__ == '__main__':
    
    # PARSE ARGS
    parser = argparse.ArgumentParser(description = "Rpi gets teleinfo from EDF serial output", epilog = "" )
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

    if args.archive_minute:
        process_archive_minute()
    if args.archive_hour:
        process_archive_minute()
        process_archive_hour()
    