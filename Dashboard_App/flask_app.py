"""  HOW TO HOST PANDAS AND MATPLOTLIB ONLINE TEMPLATE"""

#Flask imports
from flask import Flask, render_template, send_file, make_response, url_for, Response

#Pandas and Matplotlib
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.image as mpimg
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#other requirements
import io
import json
# from IPython.display import display, HTML
from datetime import datetime
import warnings
from io import BytesIO
import base64

from wlan_script import wlan_devicetype_dist, get_wlan_df, wlan_devicename_dist, wlan_manuf_dist, time_data_graph, time_pck_scatter, pck_hist
from bt_script import *


app = Flask(__name__)

#Pandas Page -- Currently displays WLAN data
@app.route('/')
@app.route('/wlan_table_data', methods=("POST", "GET"))
def GK():
    return render_template('wlan_table_data.html',
                           PageTitle = "WLAN Table",
                           table=[get_wlan_df().head().to_html(classes='data')], titles= get_wlan_df().columns.values)


#Matplotlib page
@app.route('/wlan_visuals', methods=("POST", "GET"))
def mpl():
    return render_template('wlan_visuals.html',
                           PageTitle = "WLAN Visuals")

@app.route('/net-graph', methods=("POST", "GET"))
def ng():
    return render_template('net-graph.html',
                           PageTitle = "Network Graph")

params=bt_params()
@app.route('/bt_visuals', methods=("POST", "GET"))
def bt():
    return render_template('bt_visuals.html',
                           PageTitle = "Bluetooth Visuals", params=params)


#------------------------------------------------------------------------------------------------------------------

# WLAN CHARTS (still have to figure out if there is a way to get these all into another file)

@app.route('/wlan_devicetype_dist.png')
def plot_wlan_devicetype_dist():
    fig = wlan_devicetype_dist()
    output = io.BytesIO()
    FigureCanvas(fig.figure).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/wlan_devicename_dist.png')
def plot_wlan_devicename_dist():
    fig = wlan_devicename_dist()
    output = io.BytesIO()
    FigureCanvas(fig.figure).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/wlan_manuf_dist.png')
def plot_wlan_manuf_dist():
    fig = wlan_manuf_dist()
    output = io.BytesIO()
    FigureCanvas(fig.figure).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/time_data_graph.png')
def plot_time_data_graph():
    fig = time_data_graph()
    output = io.BytesIO()
    FigureCanvas(fig.figure).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/time_pck_scatter.png')
def plot_time_pck_scatter():
    fig = time_pck_scatter()
    output = io.BytesIO()
    FigureCanvas(fig.figure).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/pck_hist.png')
def plot_pck_hist():
    fig = pck_hist()
    output = io.BytesIO()
    FigureCanvas(fig.figure).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

#END WLAN CHARTS

#------------------------------------------------------------------------------------------------------------------

# BLUETOOTH CHARTS

@app.route('/bt_devicetype_dist.png')
def plot_bt_devicetype_dist():
    fig = bt_devicetype_dist()
    output = io.BytesIO()
    FigureCanvas(fig.figure).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/bt_devicename_dist.png')
def plot_bt_devicename_dist():
    fig_name = bt_devicename_dist()
    output = io.BytesIO()
    FigureCanvas(fig_name.figure).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/bt_manuf_dist.png')
def plot_bt_manuf_dist():
    fig_manuf = bt_manuf_dist()
    output = io.BytesIO()
    FigureCanvas(fig_manuf.figure).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


#END BLUETOOTH CHARTS

#------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run(debug = True)
