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
# Application to schedule using crontab

# Get data from NetAtmo
authorization = lnetatmo.ClientAuth()
leSentier = lnetatmo.PublicData(authorization) # see how to change default coordinates in module lnetatmo.

# Insert data in database
query = 'INSERT INTO MEASURES (Epoch, Value, Unit, Station) VALUES (%s, %s, 1, 1)' % ( leSentier.getTime_serverEpoch(), leSentier.get24h() )
result = query_db(query, one=False)
print (result)

print (u'Valeur mesurée au Sentier = %smm, le %s.' % ( leSentier.get24h(), leSentier.getTime_serverEpoch() ))