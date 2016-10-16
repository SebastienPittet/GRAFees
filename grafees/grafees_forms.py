#coding=utf-8

from flask_wtf import Form
from wtforms import StringField
from wtforms import DateField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField


class Intervalle(Form):
    dateFrom = DateField('Date from', validators=[DataRequired()], format='%Y-%m-%d')
    dateTo = DateField('Date To', validators=[DataRequired()], format='%Y-%m-%d')