#coding=utf-8

# Documentation: https://wtforms.readthedocs.io/en/latest/

from flask_wtf import Form
from wtforms import StringField, IntegerField
from wtforms import DateField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField


class Intervalle(Form):
    dateFrom = DateField(label='Depuis', validators=[DataRequired()], format='%Y-%m-%d')
    dateTo = DateField(label='Au', validators=[DataRequired()], format='%Y-%m-%d')

class CorrelateRainSelect(Form):
    Period = IntegerField(label='Nombre de jours', default='14', description=u'Nombre de jours à compter de la date du jour', validators=[DataRequired()])