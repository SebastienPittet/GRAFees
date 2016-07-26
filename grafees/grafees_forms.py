#coding=utf-8

from flask_wtf import Form
from wtforms import StringField
from wtforms import DateField
from wtforms.validators import DataRequired


class Intervalle(Form):
    dateFrom = DateField('Date from', validators=[DataRequired()], format='%d.%m.%Y')
    dateTo = DateField('Date To', validators=[DataRequired()], format='%d.%m.%Y')