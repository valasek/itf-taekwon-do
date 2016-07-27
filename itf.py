# -*- coding: utf-8 -*-
"""
    ITF competition
    ~~~~~~~~
    ITF competition portal is written in Flask and sqlite3.
    :copyright: (c) 2016 by Stanislav Valášek, valasek@gmail.com.
    :license: GPL v3, see LICENSE for more details.
"""

# all the imports
import os, datetime

from flask import Flask, jsonify, request, session, g, redirect, url_for, abort, render_template, flash

import forms
# from flask_debugtoolbar import DebugToolbarExtension
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
from model.models import db, MemberCompetition, TeamMembers, Teams, Competitions, Users, Sex, Levels, Tull, Matsogi, Tki, Wirok
from sqlalchemy import func


@app.teardown_appcontext
def close_db(exception):
    """Closes the database again at the end of the request."""
    # ToDo: Close SQLAlchemy session/conection
    # if hasattr(g, 'sqlite_db'):
    #    g.sqlite_db.close()


def init_db():
    app.logger.info("Entering init_db")
    # SQLAlchemy seed
    from model import seed


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    app.logger.info("Entering initdb_command")
    init_db()
    print 'Initialized and seeded the database.'


@app.before_request
def before_request():
    g.user = None
    if 'email' in session:
        g.user = Users.query.filter_by(email=session['email']).first()


@app.route('/')
def show_competitions():
    app.logger.info("Route /")
    init_db()
    competition = Competitions.query.all()
    members_in_team = db.session.query(Teams.id, Teams.team,func.count(Teams.id).label('members'),).join(TeamMembers).group_by(TeamMembers.team_id).all()
    enrolled_members = db.session.query(TeamMembers.team_id, func.count(TeamMembers.id).label('enrolled')).join(MemberCompetition).group_by(TeamMembers.team_id).all()
    return render_template('competitions.html', competition=competition[0], members_in_team=members_in_team, enrolled_members=enrolled_members)


@app.route('/competition-members')
def show_competition_members():
    app.logger.info("Route /competition-members")
    competition = Competitions.query.filter_by(id=session['competition_id'])
    competitors = db.session.query(TeamMembers).join(MemberCompetition).filter(TeamMembers.team_id == session['team_id']).all()
    competitors_count = len(competitors)
    total_fee = competitors_count * Competitions.query.first().fee
    tull_m = Tull.query.filter(Tull.sex_id==1).all()
    tull_f = Tull.query.filter(Tull.sex_id==2).all()
    matsogi_m = Matsogi.query.filter(Matsogi.sex_id==1).all()
    matsogi_f = Matsogi.query.filter(Matsogi.sex_id==2).all()
    wirok_m = Wirok.query.filter(Wirok.sex_id == 1).all()
    wirok_f = Wirok.query.filter(Wirok.sex_id == 2).all()
    tki_m = Tki.query.filter(Tki.sex_id == 1).all()
    tki_f = Tki.query.filter(Tki.sex_id == 2).all()
    return render_template('competition-members.html',
                           total_fee=total_fee,
                           competitors_count=competitors_count,
                           competitors=competitors,
                           competition=competition[0],
                           tull_m=tull_m, tull_f=tull_f,
                           matsogi_m=matsogi_m, matsogi_f=matsogi_f,
                           wirok_m=wirok_m, wirok_f=wirok_f,
                           tki_m=tki_m, tki_f=tki_f)


@app.route('/member/<int:itf_id>', methods=['POST', 'GET'])
def edit_team_member(itf_id):
    app.logger.info("Route /member/%s", itf_id)
    if not session.get('logged_in'):
        abort(401)
    # select data from  DB
    # db_old = get_db()
    # cur = db_old.execute('SELECT teams.name FROM teams INNER JOIN users ON users.team_id = teams.id WHERE users.id= ?', [session['user_id']])
    # member = cur.fetchall()
    member = TeamMembers.query.filter(TeamMembers.itf_id==itf_id).first()
    app.logger.info("Leaving /member/%s", itf_id)
    return render_template('member.html', member=member)


@app.route('/member/new', methods=['POST', 'GET'])
def add_member():
    app.logger.info('Route /member/new')
    if not session.get('logged_in'):
        abort(401)
    error = None
    if request.method == 'POST':
        if not request.form['itf_id']:
            flash('Zadejte ID ITF', 'alert-warning')
        elif not request.form['first_name']:
            flash('Zadejte jméno', 'alert-warning')
        elif not request.form['last_name']:
            flash('Zadejte příjmení', 'alert-warning')
        elif not request.form['birthdate']:
            flash('Zadejte datum narození', 'alert-warning')
        # elif not request.form['sex']:
        #    flash('Zadejte pohlaví')
        elif not request.form['weight']:
            flash('Zadejte váhu', 'alert-warning')
        elif not request.form['level']:
            flash('Zadejte úroveň', 'alert-warning')
        else:
            member = TeamMembers(request.form['itf_id'],
                                 session['team_id'],
                                 request.form['first_name'],
                                 request.form['last_name'],
                                 request.form['sex'],
                                 datetime.datetime.strptime(request.form['birthdate'], '%Y-%m-%d').date(),
                                 request.form['weight'],
                                 request.form['level'])
            db.session.add(member)
            db.session.commit()
            flash('Nový soutěžící úspěšně přidán', 'alert-suscess')

    member = None
    team = Teams.query.filter_by(id=session['team_id']).first()
    sex = Sex.query.all()
    level = Levels.query.all()
    return render_template('member.html', member=member, team=team, sex=sex, level=level)


@app.route('/_delete_member')
def delete_member():
    app.logger.info("Route _delete_member")
    id = request.args.get('id', 0, type=int)
    member = TeamMembers.query.filter_by(itf_id=id).first()
    db.session.delete(member)
    db.session.commit()
    flash('Člen vymazán.', 'alert-success')
    return jsonify(1)


@app.route('/_add_to_competition')
def add_member_to_competition():
    app.logger.info("Route _add_to_competition")
    dict = request.args.getlist("id[]")

    app.logger.info(dict)
    db_old = get_db()
    for id in dict:
        cur = db_old.execute('INSERT INTO member_competition (member_id, competition_id) VALUES (?, ?)', (id, session['competition_id']))
    db_old.commit()
    return jsonify(1)


@app.route('/members', methods=['POST', 'GET'])
def view_members():
    app.logger.info("Route /members")
    competitors = TeamMembers.query.filter_by(team_id=session['team_id'])
    is_signed_in = {}
    show_competition_sign_in = None
    for competitor in competitors:
        is_signed = MemberCompetition.query.filter_by(member_id=competitor.id)
        if is_signed.first() != None:
            is_signed_in[competitor.itf_id] = "checked"
    if not session.get('logged_in'):
        abort(401)
    if request.method == 'GET':
        show_competition_sign_in = request.args.get('show')
    team = Teams.query.filter_by(id=session['team_id']).first()
    return render_template('members.html',
                           competitors=competitors,
                           show_competition_sign_in=show_competition_sign_in,
                           is_signed_in=is_signed_in,
                           team=team.team)


@app.route('/login', methods=['GET', 'POST'])
def login():
    app.logger.info("Route /login")
    """Logs the user in."""
    error = None
    if request.method == 'POST':
        user = Users.query.filter_by(email=request.form['email']).first()
        if user is None:
            error = 'Invalid username'
        elif user.pw_hash != request.form['password']:
            error = 'Invalid password'
        else:
            flash(u'Byl jste úspěšně přihlášen', 'alert-info')
            session['logged_in'] = True
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            session['email'] = user.email
            session['team_id'] = user.team_id
            session['competition_id'] = "1"
            return redirect(url_for('show_competitions'))

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    app.logger.info("Route /logout")
    """Logs the user out."""
    session.pop('logged_in', None)
    session.pop('email', None)
    flash('Byli jste odhlášeni', 'alert-info')
    return redirect(url_for('show_competitions'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    app.logger.info('Route /register')
    form = forms.RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        team = Teams(form.team.data)
        db.session.add(team)
        db.session.commit()
        session['team_id'] = team.id
        user = Users(form.first_name.data,
                     form.last_name.data,
                     form.email.data,
                     form.password.data,
                     session['team_id'],
                     0)
        db.session.add(user)
        db.session.commit()
        flash('Registrace proběhla úspěšně.', 'alert-success')
        return redirect(url_for('show_competitions'))
    return render_template('register.html', form=form)

@app.route('/administration', methods=['GET', 'POST'])
def administration():
    app.logger.info("Route /administration")
    return render_template('administration.html')


if __name__ == "__main__":
    app.run()
