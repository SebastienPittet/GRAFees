# encoding: utf-8
from flask import flash
from flask import render_template
from flask import redirect # redirect http

import pygal
from pygal.style import LightGreenStyle
from grafees import app
import lnetatmo
import time
import grafees_forms



@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
                           title = 'GRAFees')	

@app.route('/pygal')
def graph():
    return redirect('http://www.blog.pythonlibrary.org/2015/04/16/using-pygal-graphs-in-flask/')
	# return pygal.Bar().add('1', [1, 3, 3, 7]).add('2', [1, 6, 6, 4]).render()

@app.route('/chart')
def test():
    hist_chart = pygal.HorizontalStackedBar(Show_legend=True,
                                            legend_box_size=18,
                                            print_values=True,
                                            rounded_bars=2,
                                            style=LightGreenStyle)
    hist_chart.title = "Remarquable sequences"
    hist_chart.x_title = "Some Numbers"
    hist_chart.x_labels = map(str, range(11))
    hist_chart.add('Fibonacci', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55])
    hist_chart.add('Padovan', [1, 1, 1, 2, 2, 3, 4, 5, 7, 9, 12]) 
    chart = hist_chart.render(is_unicode=True)
    return render_template('chart.html', chart=chart )
	
@app.route('/netatmo')
def currentTemp():
    authorization = lnetatmo.ClientAuth()
    devList = lnetatmo.DeviceList(authorization)

    tempIndoor = devList.lastData()['Indoor']['Temperature']
    tempOutdoor = devList.lastData()['Outdoor']['Temperature']

    bar_chart = pygal.Bar(x_label_rotation=30,
                          print_values=True,
                          rounded_bars=2,
                          style=LightGreenStyle,
                          width=300,
                          x_title = "Locations",
                          y_title = "Current Degrees",
                          legend_at_bottom=True)
    bar_chart.title = "Current Temp. @ Ballaigues"
    bar_chart.add('Indoor', tempIndoor)
    bar_chart.add('Outdoor', tempOutdoor)
    chart = bar_chart.render(is_unicode=True)
    return render_template('chart.html', chart=chart)
    
@app.route('/AVGtemp', methods=('GET', 'POST'))
def AVGtemp():
    # http://flask.pocoo.org/docs/0.11/patterns/wtforms/#in-the-view

    selectIntervalle = grafees_forms.Intervalle()
    
    if selectIntervalle.validate_on_submit():
        dateFromEpoch = int(time.mktime(time.strptime(str(selectIntervalle.dateFrom.data),"%Y-%m-%d")))     
        dateToEpoch = int(time.mktime(time.strptime(str(selectIntervalle.dateTo.data),"%Y-%m-%d")))

        if dateFromEpoch < dateToEpoch:
            # Create graph
            # Get data from NetAtmo
            authorization = lnetatmo.ClientAuth()
            dev = lnetatmo.DeviceList(authorization)
            
            for module, moduleData in dev.lastData(exclude=3600).items():
                for sensor, value in moduleData.items():
                    # Get Temperature and Humidity with GETMEASURE web service (1 sample every 30min)
                    resp = dev.getMeasure( device_id='70:ee:50:05:cc:ac',   # Replace with your values  
                                            module_id='02:00:00:05:c2:96',  #    "      "    "    "
                                            scale="30min",
                                            mtype="Temperature",
                                            date_begin=dateFromEpoch,
                                            date_end=dateToEpoch)
            
            values = [(int(k),v[0]) for k,v in resp['body'].items()]
            values.sort() # as values provided by netatmo are not sorted by default /!\
            xtime, ytemp = zip(*values) # split the lists
            
            hist_chart = pygal.Bar(Show_legend=True,
                                        legend_box_size=18,
                                        print_values=False,
                                        rounded_bars=2,
                                        style=LightGreenStyle)
            hist_chart.title = "Temperature in Ballaigues between %s and %s" % (str(selectIntervalle.dateFrom.data), str(selectIntervalle.dateTo.data))
            hist_chart.x_title = "Moyenne sur la période = " + str(sum(ytemp)/len(ytemp)) + "°C"
            hist_chart.x_labels = xtime
            hist_chart.add('Température °C', ytemp)
            chart = hist_chart.render(is_unicode=True)

            debugText = ""           
            return render_template('chart.html', chart=chart, debugText=debugText)      
    debugText = ""    
    return render_template('form.html', form=selectIntervalle, debugText=debugText)
    

