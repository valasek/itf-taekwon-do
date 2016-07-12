# -*- coding: utf-8 -*-
"""
    ITF competition
    ~~~~~~~~
    ITF competition portal is written in Flask and sqlite3.
    :copyright: (c) 2016 by Stanislav Valášek, valasek@gmail.com.
    :license: GPL v3, see LICENSE for more details.
"""

# all the imports
import forms
import os, sqlite3
from flask import Flask, jsonify, request, session, g, redirect, url_for, abort, render_template, flash
# from flask_debugtoolbar import DebugToolbarExtension


# set for jinga2 templates encofing
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# create our little application :)
app = Flask(__name__)
app.config.from_object('config')

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, app.config['DATABASE_NAME']),
))


# the toolbar is only enabled in debug mode:
# app.debug = True
# toolbar = DebugToolbarExtension(app)
# toolbar.init_app(app)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the current application context."""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(exception):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


def seed_db():
    db = get_db()
    with app.open_resource('seed.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print 'Initialized the database.'
    seed_db()
    print 'Seeded the database.'


@app.cli.command('seeddb')
def seeddb_command():
    """Seed the database."""
    seed_db()
    print 'Seeded the database.'


def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv


def get_team_id():
    """Get team ID"""
    db = get_db()
    team_id = query_db('''SELECT teams.id FROM teams INNER JOIN users ON users.team_id = teams.id WHERE users.id= ?''', [session['user_id']], one=True)
    app.logger.info("Got team ID: %s", team_id['id'])
    return team_id['id']


@app.before_request
def before_request():
    g.user = None
    if 'email' in session:
        g.user = query_db('SELECT * FROM users WHERE email = ?', [session['email']], one=True)


@app.route('/')
def show_competitors():
    # select data from  DB
    db = get_db()
    cur = db.execute('SELECT * from competition')
    competition = cur.fetchall()
    cur = db.execute('SELECT count(competitors.id) as competing_members FROM competitors INNER JOIN member_competition ON member_competition.member_id = competitors.id WHERE competitors.team_id = ?', [session['team_id']])
    competing_members = cur.fetchone()

    return render_template('competitions.html', competition=competition[0], competing_members=competing_members[0])


@app.route('/edit', methods=['POST', 'GET'])
def edit_competitor():
    if not session.get('logged_in'):
        abort(401)
    # select data from  DB
    db = get_db()
    cur = db.execute('SELECT teams.name FROM teams INNER JOIN users ON users.team_id = teams.id WHERE users.id= ?',
                     [session['user_id']])
    member = cur.fetchall()

    return render_template('member.html', member=member)


@app.route('/add', methods=['POST'])
def add_competitor():
    app.logger.info('Route: /add')
    if not session.get('logged_in'):
        abort(401)
    error = None
    if request.method == 'POST':
        if not request.form['itf_id']:
            flash('Zadejte IDT ID')
        elif not request.form['first_name']:
            flash('Zadejte jméno')
        elif not request.form['last_name']:
            flash('Zadejte příjmení')
        elif not request.form['birthdate']:
            flash('Zadejte datum narození')
        # elif not request.form['sex']:
        #    flash('Zadejte pohlaví')
        elif not request.form['weight']:
            flash('Zadejte váhu')
        elif not request.form['level']:
            flash('Zadejte úroveň')
        else:
            db = get_db()
            db.execute('INSERT INTO competitors (itf_id, first_name, last_name, birthdate, sex, weight, level, team_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (
            request.form['itf_id'], request.form['first_name'], request.form['last_name'], request.form['birthdate'], "Muz", request.form['weight'], request.form['level'], session['team_id']))
            # db.execute('insert into competitors (itf_id, first_name, last_name, sex, birthdate, weight, level, team_id) values (?, ?, ?, ?, ?, ?, ?, ?)',
            #          [request.form['itf_id'], [request.form['first_name']], [request.form['last_name']], [request.form['sex']], [request.form['birthdate']], [request.form['weight']], [request.form['level']], [session['team_id']])
            pass
            db.commit()
            flash('Nový soutěžící úspěšně přidán')

    # select data from  DB
    db = get_db()
    cur = db.execute('SELECT teams.name FROM teams INNER JOIN users ON users.team_id = teams.id WHERE users.id= ?', [session['user_id']])
    member = cur.fetchall()

    return render_template('member.html', member=member)


@app.route('/_delete_member')
def delete_member():
    app.logger.info("CALL: _delete_member")
    id = request.args.get('id', 0, type=int)
    db = get_db()
    cur = db.execute('DELETE FROM competitors where itf_id = ?', [id])
    db.commit()
    flash('Člen vymazán.')
    return jsonify(1)


@app.route('/_add_to_competition')
def add_member_to_competition():
    app.logger.info("CALL: _add_to_competition")
    dict = request.args.getlist("id[]")
    app.logger.info(dict)
    db = get_db()
    for id in dict:
        #app.logger.info(id)
        cur = db.execute('INSERT INTO member_competition (member_id, competition_id) VALUES (?, ?)', (id, "1"))
    db.commit()
    #flash('Člen vymazán.')
    return jsonify(1)


@app.route('/members', methods=['POST', 'GET'])
def view_competitors():
    app.logger.info("CALL: view_competitors")
    db = get_db()
    # Select members for the team
    cur = db.execute('SELECT itf_id, first_name, last_name, sex, birthdate, level FROM competitors where team_id = ? ORDER BY id DESC', [session['team_id']])
    competitors = cur.fetchall()
    if not session.get('logged_in'):
        abort(401)
    if request.method == 'POST':
        app.logger.info("post")
    else:
        app.logger.info("get")

    return render_template('members.html', competitors=competitors)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Logs the user in."""
    error = None
    if request.method == 'POST':
        user = query_db('''SELECT * FROM users WHERE email = ?''', [request.form['email']], one=True)
        if user is None:
            error = 'Invalid username'
        elif user['pw_hash'] != request.form['password']:
            error = 'Invalid password'
        else:
            flash('Byl jste úspěšně přihlášen')
            session['logged_in'] = True
            session['user_id'] = user['id']
            session['is_admin'] = user['is_admin']
            session['email'] = user['email']
            session['team_id'] = user['team_id']
            return redirect(url_for('show_competitors'))

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    """Logs the user out."""
    session.pop('logged_in', None)
    session.pop('email', None)
    flash('Byli jste odhlášeni')
    return redirect(url_for('show_competitors'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    app.logger.info('Route: /register')
    form = forms.RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        db = get_db()
        db.execute('INSERT INTO teams (name) VALUES (?)', ([form.team.data]))
        db.commit()
        session['team_id'] = get_team_id()
        db.execute('INSERT INTO users (first_name, last_name, email, pw_hash, team_id, is_admin) VALUES (?, ?, ?, ?, ?, ?)',
            (form.first_name.data, form.last_name.data, form.email.data, form.password.data, session['team_id'], 0))
        db.commit()
        #SQLAlchemy code
        #user = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
        #db_session.add(user)
        flash('Registrace proběhla úspěšně.')
        return redirect(url_for('show_competitors'))
    return render_template('register.html', form=form)


if __name__ == "__main__":
    app.run()
