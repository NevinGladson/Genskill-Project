import psycopg2
import click 
from flask import current_app, g
from flask.cli import with_appcontext

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
    if 'db' not in g: 
        dbname = current_app.config['DATABASE'] 
        g.db = psycopg2.connect(f"dbname={dbname}")
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
