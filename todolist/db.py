import psycopg2
import click 
from flask import current_app, g
from flask.cli import with_appcontext
import os

class User:
    def __init__(self, id, email, username, password_hash):
        self.id = id
        self.email = email
        self.username = username
        self.password_hash = password_hash

    # Implement the get_id method
    def get_id(self):
        return str(self.id)

    @property
    def is_authenticated(self):
        # Customize this method based on your application's logic
        return True

    @property
    def is_active(self):
        # Customize this method based on your application's logic
        return True



def get_db():
    def get_db():
     if 'db' not in g:
        # Use environment variables to configure the database connection
        dbname = os.getenv('DATABASE_NAME')
        dbuser = os.getenv('DATABASE_USER')
        dbpass = os.getenv('DATABASE_PASSWORD')
        dbhost = os.getenv('DATABASE_HOST', 'localhost')  # Default to localhost if not set
        dbport = os.getenv('DATABASE_PORT', '5432')      # Default PostgreSQL port is 5432
        dsn = f"dbname={dbname} user={dbuser} password={dbpass} host={dbhost} port={dbport}"
        g.db = psycopg2.connect(dsn)
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
        
def init_db():
    db = get_db()
    f = current_app.open_resource("sql/001_list.sql")
    sql_code = f.read().decode("ascii")
    cur = db.cursor()
    cur.execute(sql_code)
    cur.close()
    db.commit()
    close_db()
    
@click.command('initdb', help="initialise the database")
@with_appcontext   
def init_db_command():
    init_db()
    click.echo('DB initialised')


def init_app(app):
    app.teardown_appcontext(close_db) #hook
    app.cli.add_command(init_db_command)
