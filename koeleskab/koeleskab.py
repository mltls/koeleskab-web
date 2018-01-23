import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, redirect

import random
import json

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'koeleskab.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('KOELESKAB_SETTINGS', silent=True)

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print("Initialized the database")

@app.route('/')
def red():
    return redirect('/1')

@app.route('/<int:k_id>')
def show_koeleskab(k_id):
    db = get_db()
    cur = db.execute('select * from koeleskab order by time')
    entries = cur.fetchall()
    return render_template('show_koeleskab.html', entries=entries, k_id=k_id)

@app.route('/random')
def return_random():
    return json.dumps(random.random())

@app.route('/sim_data')
def return_sim_data():
    a = [{'sale': random.random(), 'year': i} for i in range(100)]
    return json.dumps(a)
         
@app.route('/num_koeleskabs')
def return_num_koeleskab():
    r = 5
    return json.dumps(r)
