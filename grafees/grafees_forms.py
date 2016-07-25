#coding=utf-8

from flask_wtf import Form
from wtforms import StringField
from wtforms import DateField
from wtforms.validators import DataRequired


class Intervalle(Form):
    name = StringField('name', validators=[DataRequired()])
    dateFrom = DateField('Date from', validators=[DataRequired()])
    dateTo = DateField('Date To', validators=[DataRequired()])