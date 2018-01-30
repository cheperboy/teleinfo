from flask import render_template
from flask_appbuilder import ModelView, AppBuilder, expose, BaseView, has_access
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.charts.views import DirectByChartView
from app import db, appbuilder
from .models import Teleinfo, TeleinfoMinute, TeleinfoHour
from datetime import datetime, timedelta

def pretty_hour(value):
    return value.strftime("%H:%M")

def pretty_date(value):
    return value.strftime("%d/%m %Hh")

'''
return passed date formatted for URL like this '2018-01-28+15%3A17%3A51'
'''
def deltaminute(min):
    date = datetime.now() - timedelta(minutes=min)
    out = date.strftime("%Y-%m-%d+%H%%3A%M%%3A%S")
    return out

'''
return URL like this 
'/teleinfophaseschartview/chart/0?_flt_1_timestamp=2018-01-28+15%3A17%3A51'
'''
def get_url(min, klass):
    return '/' + klass + '/chart/0?_flt_1_timestamp=' + deltaminute(min)

"""
CUSTOM
"""
class TeleinfoCustomView(BaseView):

    default_view = 'test'

    @expose('/insertt/')
    @has_access
    def insertt(self):
        param1 = 'insertt'
        teleinfo = Teleinfo()
        teleinfo.timestamp = datetime.now()
        teleinfo.base = 1
        teleinfo.papp = 1
        teleinfo.iinst1 = 20
        teleinfo.iinst2 = 1
        teleinfo.iinst3 = 1

        try:
            db.session.add(teleinfo)
            db.session.commit()
            param1 = 'OK'
        except exc.SQLAlchemyError as e:
            param1 = 'Not Ok'

        self.update_redirect()
        return self.render_template('method3.html',
							   param1 = param1)

    @expose('/test/')
    @has_access
    def test(self):
        param1 = 'test'
        ti= db.session.query(Teleinfo).filter(Teleinfo.iinst1 > 19).count()
        ti= db.session.query(Teleinfo).filter(Teleinfo.iinst1 > -1).order_by(Teleinfo.id.asc()).first()
        param1 = str(ti)
        
        return self.render_template('method3.html',
							   param1 = param1)


"""
TABLE
"""
class TeleinfoModelView(ModelView):
    datamodel = SQLAInterface(Teleinfo)
    list_columns = ['timestamp','base', 'papp', 'iinst1', 'iinst2', 'iinst3']

class TeleinfoMinuteModelView(ModelView):
    datamodel = SQLAInterface(TeleinfoMinute)
    list_columns = ['timestamp','base', 'papp', 'iinst1', 'iinst2', 'iinst3']

class TeleinfoHourModelView(ModelView):
    datamodel = SQLAInterface(TeleinfoHour)
    list_columns = ['timestamp','base', 'papp', 'iinst1', 'iinst2', 'iinst3']

"""
CHART Phase
"""
class TeleinfoPhasesChartView(DirectByChartView):
    datamodel = SQLAInterface(Teleinfo)
    chart_title = 'Phases'
    chart_type = 'LineChart'
    definitions = [
    {
        'label': 'phase',
        'group': 'timestamp',
        'formatter': pretty_hour,
        'series': ['iinst1', 'iinst2', 'iinst3']
    }
]
class TeleinfoMinutePhasesChartView(DirectByChartView):
    datamodel = SQLAInterface(TeleinfoMinute)
    chart_title = 'Phases'
    chart_type = 'LineChart'
    definitions = [
    {
        'label': 'phase',
        'group': 'timestamp',
        'formatter': pretty_hour,
        'series': ['iinst1', 'iinst2', 'iinst3']
    }
]
class TeleinfoHourPhasesChartView(DirectByChartView):
    datamodel = SQLAInterface(TeleinfoHour)
    chart_title = 'Phases'
    chart_type = 'LineChart'
    definitions = [
    {
        'label': 'phase',
        'group': 'timestamp',
        'formatter': pretty_date,
        'series': ['iinst1', 'iinst2', 'iinst3']
    }
]

"""
CHART Puissance
"""
class TeleinfoPuissanceChartView(DirectByChartView):
    datamodel = SQLAInterface(Teleinfo)
    chart_title = 'Puissance'
    chart_type = 'LineChart'
    definitions = [
    {
        'group': 'timestamp',
        'formatter': pretty_hour,
        'series': ['papp']
    }    
]       
class TeleinfoMinutePuissanceChartView(DirectByChartView):
    datamodel = SQLAInterface(TeleinfoMinute)
    chart_title = 'Puissance'
    chart_type = 'LineChart'
    definitions = [
    {
        'group': 'timestamp',
        'formatter': pretty_hour,
        'series': ['papp']
    }    
]      
class TeleinfoHourPuissanceChartView(DirectByChartView):
    datamodel = SQLAInterface(TeleinfoHour)
    chart_title = 'Puissance'
    chart_type = 'LineChart'
    definitions = [
    {
        'group': 'timestamp',
        'formatter': pretty_date,
        'series': ['papp']
    }    
]
       
"""
CHART Total
"""        
class TeleinfoTotalChartView(DirectByChartView):
    datamodel = SQLAInterface(Teleinfo)
    chart_title = 'total'
    chart_type = 'LineChart'
    definitions = [
    {
        'label': 'phase',
        'group': 'timestamp',
        'formatter': pretty_hour,
        'series': ['base']
    }
]
class TeleinfoHourTotalChartView(DirectByChartView):
    datamodel = SQLAInterface(TeleinfoHour)
    chart_title = 'total'
    chart_type = 'LineChart'
    definitions = [
    {
        'label': 'phase',
        'group': 'timestamp',
        'formatter': pretty_date,
        'series': ['base']
    }
]

""" Menu Conso EDF """
#appbuilder.add_view(TeleinfoCustomView, "test", category='Teleinfo')
appbuilder.add_view(TeleinfoPhasesChartView, "Phases sec", icon="fa-bar-chart", category="Conso EDF")
appbuilder.add_view(TeleinfoMinutePhasesChartView, "Phases minute", icon="fa-bar-chart", category="Conso EDF")
appbuilder.add_view(TeleinfoHourPhasesChartView, "Phases heure", icon="fa-bar-chart", category="Conso EDF")
appbuilder.add_view(TeleinfoPuissanceChartView, "Puissance sec", icon="fa-bar-chart", category="Conso EDF")
appbuilder.add_view(TeleinfoMinutePuissanceChartView, "Puissance heure", icon="fa-bar-chart", category="Conso EDF")
appbuilder.add_view(TeleinfoHourPuissanceChartView, "Puissance heure", icon="fa-bar-chart", category="Conso EDF")
appbuilder.add_view(TeleinfoTotalChartView, "Total sec", icon="fa-bar-chart", category="Conso EDF")
appbuilder.add_view(TeleinfoHourTotalChartView, "Total heure", icon="fa-bar-chart", category="Conso EDF")

""" Menu Admin Table """
appbuilder.add_view(TeleinfoModelView, "Teleinfo", icon = "fa-table", category = "Admin Teleinfo")
appbuilder.add_view(TeleinfoMinuteModelView, "TeleinfoMinute", icon = "fa-table", category = "Admin Teleinfo")
appbuilder.add_view(TeleinfoHourModelView, "TeleinfoHour", icon = "fa-table", category = "Admin Teleinfo")

""" Menu Chart Phase """
appbuilder.add_link("15 minutes", 
                    href=get_url(15, 'teleinfophaseschartview'), 
                    icon="fa-bar-chart",
                    category='Phase')

appbuilder.add_link("1 heure", 
                    href=get_url(60, 'teleinfominutephaseschartview'), 
                    icon="fa-bar-chart",
                    category='Phase')

appbuilder.add_link("12 heures", 
                    href=get_url(720, 'teleinfohourphaseschartview'), 
                    icon="fa-bar-chart",
                    category='Phase')

appbuilder.add_link("24 heures", 
                    href=get_url(1440, 'teleinfohourphaseschartview'), 
                    icon="fa-bar-chart",
                    category='Phase')

""" Menu Chart Puissance """
appbuilder.add_link("15 minutes", 
                    href=get_url(15, 'teleinfopuissancechartview'), 
                    icon="fa-bar-chart",
                    category='Puissances')

appbuilder.add_link("1 heure", 
                    href=get_url(60, 'teleinfominutepuissancechartview'), 
                    icon="fa-bar-chart",
                    category='Puissances')

appbuilder.add_link("12 heures", 
                    href=get_url(720, 'teleinfohourpuissancechartview'), 
                    icon="fa-bar-chart",
                    category='Puissances')

appbuilder.add_link("24 heures", 
                    href=get_url(1440, 'teleinfohourpuissancechartview'), 
                    icon="fa-bar-chart",
                    category='Puissances')




"""
    Application wide 404 error handler
"""
@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404

db.create_all()
