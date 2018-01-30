import click
from teleinfo_minute import process_archive_minute

@app.cli.command()
def test():
    """Initialize the database."""
    click.echo('Init the db')
    click.echo(db.session.query(models.Teleinfo).filter(models.Teleinfo.iinst1 > 19).count())
    process_archive_minute()