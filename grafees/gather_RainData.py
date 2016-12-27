#!/usr/bin/python
# encoding: utf-8

# all the imports
import os
import sqlite3
import lnetatmo

# configuration
DATABASE = os.path.join(os.getcwd(), 'grafees.db')

###############################################################################
# Some functions to handle database

def connect_db():
    return sqlite3.connect(DATABASE)

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit() 

def query_db(query, args=(), one=False):
    cur = connect_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

###############################################################################
# Application to schedule using crontab (each 60min)

# Get data from NetAtmo
authorization = lnetatmo.ClientAuth()
area_leSentier = lnetatmo.PublicData(authorization) # see how to change default coordinates in module lnetatmo.

timestamps = area_leSentier.getTimeforMeasure()
locations = area_leSentier.getLocations()
rain_measures = area_leSentier.get24h()
rain60min = area_leSentier.get60min()

for station in locations:
    #print timestamps[station]
    #print locations[station]
    #print rain_measures
    #print rain60min[station]

    query = 'INSERT INTO MEASURES (Epoch, Value, Unit, Station) VALUES (%s, %s, 1, 1)' % ( timestamps[station], rain60min[station] )

    # Insert data in database
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    conn.close()
    
    print (u'Valeur mesurée au Sentier = %smm, le %s.' % ( rain60min[station], timestamps[station] ))

    #print( query_db('SELECT * FROM MEASURES', one=False) )
