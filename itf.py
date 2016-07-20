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
from flask_sqlalchemy import SQLAlchemy
from config import configure_app


# set for jinga2 templates encofing
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# create appl
app = Flask(__name__,
    instance_path=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'instance'),
    instance_relative_config=True)

configure_app(app)

# Load default config and override config from an environment variable
#app.config.update(dict(
#    DATABASE=os.path.join(app.root_path, app.config['DATABASE_NAME']),
#))

db = SQLAlchemy(app)
from models import MemberCompetition, Matsogi, Tull, Wirok, Tki, TeamMembers, Teams, Competitions, Levels, Sex, Users

# the toolbar is only enabled in debug mode:
# app.debug = True
# toolbar = DebugToolbarExtension(app)
# toolbar.init_app(app)


@app.teardown_appcontext
def close_db(exception):
    """Closes the database again at the end of the request."""
    # ToDo: Close SQLAlchemy session/conection
    #if hasattr(g, 'sqlite_db'):
    #    g.sqlite_db.close()


def init_db():
    app.logger.debug("init_db started")
    # SQLAlchemy seed
    import seed
    app.logger.debug("init_db finished")


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print 'Initialized and seeded the database.'


@app.before_request
def before_request():
    g.user = None
    if 'email' in session:
        g.user = Users.query.filter_by(email=session['email']).first()


@app.route('/')
def show_competitors():
    init_db()ng
    competition = Competitions.query.all()
    return render_template('competitions.html', competition=competition[0])


@app.route('/competition-members')
def show_competition_members():
    # select data from  DB
    db_old = get_db()
    cur = db_old.execute('SELECT * FROM competitors JOIN member_competition ON competitors.id = member_competition.member_id WHERE competition_id = ?', [session['competition_id']])
    competitors = cur.fetchall()
    cur = db_old.execute('SELECT * FROM competition WHERE id = ?', [session['competition_id']])
    competition = cur.fetchall()

    return render_template('competition-members.html', competitors=competitors, competition=competition[0])


@app.route('/edit', methods=['POST', 'GET'])
def edit_competitor():
    if not session.get('logged_in'):
        abort(401)
    # select data from  DB
    # db_old = get_db()
    # cur = db_old.execute('SELECT teams.name FROM teams INNER JOIN users ON users.team_id = teams.id WHERE users.id= ?', [session['user_id']])
    # member = cur.fetchall()
    member = db.session.query(Teams.team).join(TeamMembers).filter(TeamMembers.id==session['user_id']).all()

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
            db_old = get_db()
            db_old.execute('INSERT INTO competitors (itf_id, first_name, last_name, birthdate, sex, weight, level, team_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (
            request.form['itf_id'], request.form['first_name'], request.form['last_name'], request.form['birthdate'], "Muz", request.form['weight'], request.form['level'], session['team_id']))
            pass
            db_old.commit()
            flash('Nový soutěžící úspěšně přidán')

    # select data from  DB
    db_old = get_db()
    cur = db_old.execute('SELECT teams.name FROM teams INNER JOIN users ON users.team_id = teams.id WHERE users.id= ?', [session['user_id']])
    member = cur.fetchall()

    return render_template('member.html', member=member)


@app.route('/_delete_member')
def delete_member():
    app.logger.info("CALL: _delete_member")
    id = request.args.get('id', 0, type=int)
    db_old = get_db()
    cur = db_old.execute('DELETE FROM competitors where itf_id = ?', [id])
    db_old.commit()
    flash('Člen vymazán.')
    return jsonify(1)


@app.route('/_add_to_competition')
def add_member_to_competition():
    app.logger.info("CALL: _add_to_competition")
    dict = request.args.getlist("id[]")
    app.logger.info(dict)
    db_old = get_db()
    for id in dict:
        cur = db_old.execute('INSERT INTO member_competition (member_id, competition_id) VALUES (?, ?)', (id, session['competition_id']))
    db_old.commit()
    return jsonify(1)


@app.route('/members', methods=['POST', 'GET'])
def view_competitors():
    app.logger.info("CALL: view_competitors")
    competitors = TeamMembers.query.filter_by(team_id=session['team_id'])
    is_signed_in = {}
    for competitor in competitors:
        is_signed = MemberCompetition.query.filter_by(member_id=competitor.id)
        if is_signed.first() != None:
            is_signed_in[competitor.itf_id] = "checked"
    if not session.get('logged_in'):
        abort(401)
    if request.method == 'GET':
        show_competition_sign_in = request.args.get('show')
    return render_template('members.html', competitors=competitors, show_competition_sign_in=show_competition_sign_in, is_signed_in=is_signed_in)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Logs the user in."""
    error = None
    if request.method == 'POST':
        user = Users.query.filter_by(email=request.form['email']).first()
        if user is None:
            error = 'Invalid username'
        elif user.pw_hash != request.form['password']:
            error = 'Invalid password'
        else:
            flash('Byl jste úspěšně přihlášen')
            session['logged_in'] = True
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            session['email'] = user.email
            session['team_id'] = user.team_id
            session['competition_id'] = "1"
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
        team = Teams(form.team.data)
        db.session.add(team)
        db.session.commit()
        session['team_id'] = team.id
        user = Users(form.first_name.data, form.last_name.data, form.email.data, form.password.data, session['team_id'], 0)
        db.session.add(user)
        db.session.commit()
        flash('Registrace proběhla úspěšně.')
        return redirect(url_for('show_competitors'))
    return render_template('register.html', form=form)


if __name__ == "__main__":
    app.run()
