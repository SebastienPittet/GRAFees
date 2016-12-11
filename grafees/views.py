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
import lcavelink



@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
                           title = u'GRAFées - Groupe Exploration Fées')	

@app.route('/pygal')
def graph():
    return redirect('http://www.blog.pythonlibrary.org/2015/04/16/using-pygal-graphs-in-flask/')
	# return pygal.Bar().add('1', [1, 3, 3, 7]).add('2', [1, 6, 6, 4]).render()

@app.route('/TempBallaigues')
def currentTemp():
    authorization = lnetatmo.ClientAuth()
    devList = lnetatmo.DeviceList(authorization)

    tempIndoor = devList.lastData()['Indoor']['Temperature']
    tempOutdoor = devList.lastData()['Outdoor']['Temperature']

    bar_chart = pygal.Bar(x_label_rotation=30,
                          print_values=True,
                          rounded_bars=2,
                          style=LightGreenStyle,
                          x_title = "Locations",
                          y_title = "Current Degrees",
                          legend_at_bottom=True)
    bar_chart.title = "Current Temp. @ Ballaigues"
    bar_chart.add('Indoor', tempIndoor)
    bar_chart.add('Outdoor', tempOutdoor)
    chart = bar_chart.render(is_unicode=True)
    return render_template('chart.html', chart=chart, title=u'Orée des Bois : en live')
    
@app.route('/AVGtemp', methods=('GET', 'POST'))
def AVGtemp():
    # http://flask.pocoo.org/docs/0.11/patterns/wtforms/#in-the-view
    
    # Display a graph of Average Temperature at home

    selectIntervalle = grafees_forms.Intervalle()
    
    if selectIntervalle.validate_on_submit():
        dateFromEpoch = int(time.mktime(time.strptime(str(selectIntervalle.dateFrom.data),"%Y-%m-%d")))     
        dateToEpoch = int(time.mktime(time.strptime(str(selectIntervalle.dateTo.data),"%Y-%m-%d")))

        if dateFromEpoch < dateToEpoch:
            # Create graph
            # Get data from NetAtmo
            authorization = lnetatmo.ClientAuth()
            dev = lnetatmo.WeatherStationData(authorization)
            
            for module, moduleData in dev.lastData(exclude=3600).items():
                for sensor, value in moduleData.items():
                    # Get Temperature with GETMEASURE web service (1 sample every 30min)
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
            hist_chart.title = u"Température à Ballaigues période %s and %s" % (str(selectIntervalle.dateFrom.data), str(selectIntervalle.dateTo.data))
            hist_chart.x_title = u"Moyenne sur la période = " + str(sum(ytemp)/len(ytemp)).decode() + u"°C"
            hist_chart.x_labels = xtime
            hist_chart.add(u'Température °C', ytemp)
            chart = hist_chart.render().decode('utf-8')

            debugText = "" 
            return render_template('chart.html', chart=chart, title=u"Moyenne des températures", debugText=debugText)      
    debugText = ""    
    return render_template('form.html', form=selectIntervalle, title=u'Moyenne des températures', debugText=debugText)
    
@app.route('/CorrelateRain', methods=('GET', 'POST'))
def CorrelateRain():
    #Display a view of rain over the cave

    CorrelateRainForm = grafees_forms.CorrelateRainSelect()
    if CorrelateRainForm.validate_on_submit():
        number_days = int(CorrelateRainForm.Period.data)

        # Cave-link get a sample each 30min. => 48 samples per day
        LanceleauCavelinkURL = "http://www.cavelink.com/cl/da.php?s=142&g=20&w=100&l=" + str(number_days*48)
        Lanceleau = lcavelink.CaveLinkData(LanceleauCavelinkURL)
    
        authorization = lnetatmo.ClientAuth()
        dev = lnetatmo.PublicData(authorization) # see how to change default coordinates in module lnetatmo.
    
        hist_chart = pygal.Bar(Show_legend = True,
                             legend_box_size = 18,
                             dynamic_print_values = True,
                             rounded_bars = 2,
                             style = LightGreenStyle)
        hist_chart.title = u"Corrélation pluie au Brassus et Données Cave-Link"
        hist_chart.x_title = u"Dates au format Epoch"
        hist_chart.y_title = u"Niveau d'eau au dessus de la sonde"
        hist_chart.x_labels = Lanceleau.GetData().keys() # in epoch
        hist_chart.add(u"Lanceleau", Lanceleau.GetData().values())
        #hist_chart.add(u"Lac Glaisine", [1.2,0.8,0.5,05,0.4,3, 3,4,4.5])
        hist_chart.add(u"Pluie Brassus", dev.get24h(), secondary=True) #second axe
        chart = hist_chart.render().decode('utf-8')
        return render_template('chart.html', chart=chart, title='/!\ Rain Graph is in Developpment.', debugText = '')
    return render_template('CorrelateRainForm.html', form=CorrelateRainForm, title=u'Impact Pluie - Select historique', debugText='')