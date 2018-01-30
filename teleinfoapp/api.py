import os
import sys
basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(basedir,'app'))
from app import db
from app.models import Teleinfo
from datetime import datetime

def createti(timestamp, base, papp, iinst1, iinst2, iinst3):
    ret = 'NOK'
    teleinfo = Teleinfo()
    teleinfo.timestamp = timestamp
    teleinfo.base = base
    teleinfo.papp = papp
    teleinfo.iinst1 = iinst1
    teleinfo.iinst2 = iinst2
    teleinfo.iinst3 = iinst3

    try:
        db.session.add(teleinfo)
        db.session.commit()
        ret = 'OK'
    except exc.SQLAlchemyError as e:
        ret = 'Not Ok'
    return ret

#print createti(datetime.now(), 3, 2, 2, 2, 3)