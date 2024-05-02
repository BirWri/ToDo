import os
import sqlite3
import requests
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

app = Flask(__name__)  # create the application instance :)
app.config.from_object(__name__)  # load config from this file , flaskr.py

# Load default config and override config from an environment variable
# TODO use for db path http://flask.pocoo.org/docs/0.12/config/#instance-folders
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

# FLASKR_SETTINGS points to a config file
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def http_post_request_to_postman():
    """Sends an http post request to Postman-Echo with a specific apy-key. Returns status code"""

    postman_api_endpoint = "https://postman-echo.com/post"
    postman_representation_data = {'api_key': 'aufhiuew65653'}
    postman_representation_request = requests.post(url=postman_api_endpoint, data=postman_representation_data)

    # Prints the responses from Postman for testing
    #print(postman_representation_request)
    #print(postman_representation_request.json())

    return postman_representation_request.status_code


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('SELECT title, text FROM entries ORDER BY id DESC')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)


@app.route('/api/search', methods=['GET'])
def search_results():
    #Establish connection to the db and show all
    db = get_db()
    cur = db.execute('SELECT title, text FROM entries')
    entries = cur.fetchall()
    return "yay"


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)

    title = request.form['title']
    text = request.form['text']

    db = get_db()
    db.execute('INSERT INTO entries (title, text) VALUES (?, ?)',
               [title, text])
    db.commit()

    # Send representation to postman-echo and returns the response code
    postman_api_response = http_post_request_to_postman()

    if postman_api_response == 200:
        print("Postman response 200")
    else:
        print("Postman response is not 200")

    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))
