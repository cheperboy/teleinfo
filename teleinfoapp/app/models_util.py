from app import db
from app.models import Teleinfo, TeleinfoMinute, TeleinfoHour
from datetime import datetime, timedelta
from flask_appbuilder import Model

class TICommon():
    @classmethod
    def create(self, cls, objet, timestamp, base, papp, iinst1, iinst2, iinst3):
        ret = 'NOK'
        objet.timestamp = timestamp
        objet.base = base
        objet.papp = papp
        objet.iinst1 = iinst1
        objet.iinst2 = iinst2
        objet.iinst3 = iinst3
        try:
            db.session.add(objet)
            db.session.commit()
            ret = 'OK'
        except exc.SQLAlchemyError as e:
            ret = 'Not Ok'
        return ret

    @classmethod
    def get_last(self, cls):
        return(db.session.query(cls).order_by(cls.id.desc()).first())

    @classmethod
    def get_between_date(self, cls, begin, end):
        out = db.session.query(cls) \
                        .filter(cls.timestamp > datetime(begin.year, begin.month, begin.day, begin.hour, begin.minute)) \
                        .filter(cls.timestamp < datetime(end.year, end.month, end.day, end.hour, end.minute)) \
                        .order_by(cls.id.desc()) \
                        .all()
        return out
        
class TIMinute():
    @classmethod
    def create(self, timestamp, base, papp, iinst1, iinst2, iinst3):
        objet = TeleinfoMinute()
        return(TICommon().create(TeleinfoMinute, objet, timestamp, base, papp, iinst1, iinst2, iinst3))

    @classmethod
    def get_last(self):
        return(TICommon().get_last(TeleinfoMinute))

    @classmethod
    def get_between_date(self, begin, end):
        return(TICommon().get_between_date(TeleinfoMinute, begin, end))
    
class TIHour():
    @classmethod
    def create(self, timestamp, base, papp, iinst1, iinst2, iinst3):
        objet = TeleinfoHour()
        return(TICommon().create(TeleinfoHour, objet, timestamp, base, papp, iinst1, iinst2, iinst3))

    @classmethod
    def get_last(self):
        return(TICommon().get_last(TeleinfoHour))

    @classmethod
    def get_between_date(self, begin, end):
        return(TICommon().get_between_date(TeleinfoHour, begin, end))
    
class TI():
    @classmethod
    def create(self, timestamp, base, papp, iinst1, iinst2, iinst3):
        objet = Teleinfo()
        return(TICommon().create(Teleinfo, objet, timestamp, base, papp, iinst1, iinst2, iinst3))

    @classmethod
    def get_last(self):
        return(TICommon().get_last(Teleinfo))

    @classmethod
    def get_between_date(self, begin, end):
        return(TICommon().get_between_date(Teleinfo, begin, end))
    
