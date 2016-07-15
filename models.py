# -*- coding: utf-8 -*-
# app/models.py
from itf import db_new


class CompetitionCategories(db_new.Model):
    __tablename__ = 'competition_categories'

    # Columns
    id = db_new.Column(db_new.Integer, primary_key=True, autoincrement=True)
    competition_type = db_new.Column(db_new.String(50))
    name = db_new.Column(db_new.String())
    sex = db_new.Column(db_new.String)

    def __init__(self, competition_type, name, sex):
        self.competition_type = competition_type
        self.name = name
        self.sex = sex

    def __repr__(self):
        return '<id {}>'.format(self.id)
