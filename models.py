# -*- coding: utf-8 -*-
# app/models.py
from itf import db


class Sex(db.Model):
    __tablename__ = "dic_sex"
    
    # Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sex = db.Column(db.String(20))

    def __init__(self, sex):
        self.sex = sex

    def __repr__(self):
        return '<sex {}>'.format(self.sex)


class Levels(db.Model):
    __tablename__ = 'dic_levels'

    # Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    level = db.Column(db.String(20))

    def __init__(self, level):
        self.level = level

    def __repr__(self):
        return '<level {}>'.format(self.level)


class MemberCompetition(db.Model):
    __tablename__ = "member_competition"

    # Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    member_id = db.Column(db.Integer, db.ForeignKey('team_members.id'))
    competition_id = db.Column(db.Integer)
    matsogi_id = db.Column(db.Integer, db.ForeignKey('dic_matsogi.id'))
    tull_id = db.Column(db.Integer, db.ForeignKey('dic_tull.id'))
    wirok_id = db.Column(db.Integer, db.ForeignKey('dic_wirok.id'))
    tki_id = db.Column(db.Integer, db.ForeignKey('dic_tki.id'))
    trainee = db.Column(db.Boolean)
    coach = db.Column(db.Boolean)

    def __init__(self, member_id, competition_id, matsogi_id, tull_id, wirok_id, tki_id, trainee, coach):
        self.member_id = member_id
        self.competition_id = competition_id
        self.matsogi_id = matsogi_id
        self.tull_id = tull_id
        self.wirok_id = wirok_id
        self.tki_id = tki_id
        self.trainee = trainee
        self.coach = coach

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Matsogi(db.Model):
    __tablename__ = 'dic_matsogi'

    # Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    matsogi = db.Column(db.String(50))
    sex = db.Column(db.String, db.ForeignKey('dic_sex.id'))

    def __init__(self, matsogi, sex):
        self.matsogi = matsogi
        self.sex = sex

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Tull(db.Model):
    __tablename__ = 'dic_tull'

    # Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tull = db.Column(db.String(50))
    sex = db.Column(db.String, db.ForeignKey('dic_sex.id'))

    def __init__(self, tull, sex):
        self.tull = tull
        self.sex = sex

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Wirok(db.Model):
    __tablename__ = 'dic_wirok'

    # Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wirok = db.Column(db.String(50))
    sex = db.Column(db.String, db.ForeignKey('dic_sex.id'))

    def __init__(self, wirok, sex):
        self.wirok = wirok
        self.sex = sex

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Tki(db.Model):
    __tablename__ = 'dic_tki'

    # Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tki = db.Column(db.String(50))
    sex = db.Column(db.String, db.ForeignKey('dic_sex.id'))

    def __init__(self, tki, sex):
        self.tki = tki
        self.sex = sex

    def __repr__(self):
        return '<id {}>'.format(self.id)


class TeamMembers(db.Model):
    __tablename__ = 'team_members'

    # Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    itf_id = db.Column(db.Integer)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    sex_id = db.Column(db.String, db.ForeignKey('dic_sex.id'))
    birthdate = db.Column(db.Date)
    weight = db.Column(db.Integer)
    level_id = db.Column(db.Integer, db.ForeignKey('dic_levels.id'))
    level = db.relationship('Levels', backref=db.backref('team_members', lazy='joined'))
    sex = db.relationship('Sex', backref=db.backref('team_members', lazy='joined'))

    def __init__(self, itf_id, team_id, first_name, last_name, sex_id, birthdate, weight, level_id):
        self.itf_id = itf_id
        self.team_id = team_id
        self.first_name = first_name
        self.last_name = last_name
        self.sex_id = sex_id
        self.birthdate = birthdate
        self.weight = weight
        self.level_id = level_id

    def __repr__(self):
        return '<last_name {}>'.format(self.last_name)


class Teams(db.Model):
    __tablename__ = 'teams'

    # Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team = db.Column(db.String(50))

    def __init__(self, team):
        self.team = team

    def __repr__(self):
        return '<team {}>'.format(self.team)


class Users(db.Model):
    __tablename__ = 'users'

    # Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    pw_hash = db.Column(db.String(100))
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    is_admin = db.Column(db.Boolean)

    def __init__(self, first_name, last_name, email, pw_hash, team_id, is_admin):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.pw_hash = pw_hash
        self.team_id = team_id
        self.is_admin = is_admin

    def __repr__(self):
        return '<last_name {}>'.format(self.last_name)


class Competitions(db.Model):
    __tablename__ = 'competitions'

    # Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200))
    location = db.Column(db.String(200))
    date = db.Column(db.String(200))
    deadline = db.Column(db.String(200))
    fee = db.Column(db.Integer)
    instructions_url = db.Column(db.String(200))
    langlong = db.Column(db.String(50))

    def __init__(self, name, location, date, deadline, fee, instructions_url, langlong):
        self.name = name
        self.location = location
        self.date = date
        self.deadline = deadline
        self.fee = fee
        self.instructions_url = instructions_url
        self.langlong = langlong

    def __repr__(self):
        return '<name {}>'.format(self.name)
