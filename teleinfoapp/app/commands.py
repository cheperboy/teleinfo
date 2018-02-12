import click
import os

@click.command()
def update_db():
    ls = 'ls -l ~/Development/db'
    remove = 'rm ~/Development/db/teleinfo*.db'
    update = 'cp ~/Production/db/teleinfo*.db ~/Development/db'
    click.echo(ls)
    click.echo(remove)
    os.system(remove)
    click.echo(update)
    os.system(update)
    click.echo(ls)

if __name__ == '__main__':
    update_db()
