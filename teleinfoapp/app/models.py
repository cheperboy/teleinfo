from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin, FileColumn, ImageColumn
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Query
"""
You can use the extra Flask-AppBuilder fields and Mixin's
AuditMixin will add automatic timestamp of created and modified by who
"""
class Teleinfo(Model):
    __bind_key__ = 'teleinfo'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    base = Column(Integer)
    papp = Column(Integer)
    iinst1 = Column(Integer)
    iinst2 = Column(Integer)
    iinst3 = Column(Integer)
    
    def __repr__(self):
        return str(self.timestamp)
    
    def to_dict(self):
        return {'id': self.id, 'timestamp': self.timestamp}
    
    def supp(self, param):
        return self.filter(Teleinfo.iinst > param)
        
class TeleinfoMinute(Model):
    __bind_key__ = 'teleinfo_minute'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    base = Column(Integer)
    papp = Column(Integer)
    iinst1 = Column(Float)
    iinst2 = Column(Float)
    iinst3 = Column(Float)

    def __repr__(self):
        return self.timestamp
        
class TeleinfoHour(Model):
    __bind_key__ = 'teleinfo_hour'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    base = Column(Integer)
    papp = Column(Integer)
    iinst1 = Column(Float)
    iinst2 = Column(Float)
    iinst3 = Column(Float)

    def __repr__(self):
        return self.timestamp
        
'''
https://stackoverflow.com/questions/15936111/sqlalchemy-can-you-add-custom-methods-to-the-query-object
'''
