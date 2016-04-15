from flask import render_template
from flask import redirect # redirect http
import pygal
from pygal.style import LightGreenStyle
from grafees import app

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