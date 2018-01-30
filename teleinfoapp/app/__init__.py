import logging
from flask import Flask
from flask_appbuilder import SQLA, AppBuilder

"""
 Logging configuration
"""

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_object('config')
db = SQLA(app)
appbuilder = AppBuilder(app, db.session)


"""
from sqlalchemy.engine import Engine
from sqlalchemy import event

#Only include this for SQLLite constraints
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # Will force sqllite contraint foreign keys
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
"""

from app import models, views

"""
CLI Usage
cd app/ directory
export FLASK_APP=__init__.py
flask archive_minute
"""
import click
from teleinfo_archive import process_archive_minute, process_archive_hour
@app.cli.command()
def archive_minute():
    click.echo('Process archive minute')
    process_archive_minute()

@app.cli.command()
def archive_hour():
    click.echo('Process archive hour')
    process_archive_hour()

from models_util import TIMinute
@app.cli.command()
def test():
    click.echo('test')
    #click.echo(db.session.query(models.Teleinfo).filter(models.Teleinfo.iinst1 > 19).count())
    click.echo('get_last_minute')
    print(str(TIMinute.get_last_minute().timestamp))
    click.echo('get_last')
    print(str(TIMinute.get_last().timestamp))

