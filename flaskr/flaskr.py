import os
import sqlite3
import requests
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, jsonify

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


def http_post_request_to_postman(new_entry_title):
    """Sends a http post request to Postman-Echo with a specific apy-key. Returns status code"""
    postman_api_endpoint = "https://postman-echo.com/post"
    postman_representation_data = {'new_entry_title': new_entry_title}
    postman_representation_request = requests.post(url=postman_api_endpoint, data=postman_representation_data)

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


@app.route('/api/search')
def search_results():
    # Get the query parameter
    q = request.args.get('q')

    # Throw an error if no parameters provided
    if not q:
        return '"error":"No query parameter provided"', 400

    # Initiate connect with the database
    db = get_db()

    # SQL query to find titles that are similar to q
    cur = db.execute('SELECT * FROM entries WHERE title LIKE ?', ('%' + q + '%',))

    # Fetch all the rows that match the query
    rows = cur.fetchall()

    # A list to store the fetched db rows converted to dictionary
    results = []
    for row in rows:
        results.append(dict(row))

    # The list of results is then converted to JSON
    return jsonify(results)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)

    # Assign variables to inputs from the user
    title = request.form['title']
    text = request.form['text']

    db = get_db()
    db.execute('INSERT INTO entries (title, text) VALUES (?, ?)',
               [title, text])
    db.commit()

    # Use the title of the new entry as the representative to be sent to Postman-Echo
    postman_api_status = http_post_request_to_postman(new_entry_title=title)

    # Check and communicate the response of the Postman-Echo request
    if postman_api_status == 200:
        print("Postman response 200")
    else:
        print("Error with Postman")

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
