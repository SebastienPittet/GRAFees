#!flask/bin/python

# because of large applications
# http://flask.pocoo.org/docs/0.11/patterns/packages/#larger-applications

from grafees import app
app.run(debug=True, host='0.0.0.0')
