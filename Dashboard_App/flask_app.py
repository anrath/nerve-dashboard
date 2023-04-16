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


#Data imports
with open('phy-IEEE802.11.json') as openfile:
    wlan = json.load(openfile)

wlan_df = pd.DataFrame()

for device in wlan:    
    wlan_data = {
        "key": [device['kismet.device.base.key']], 
        "device_name": [device['kismet.device.base.name']],
        "device_type": [device['kismet.device.base.type']],
        "num_packets": [device['kismet.device.base.packets.total']],
        "manuf": [device['kismet.device.base.manuf']], 
        "macaddr": [device['kismet.device.base.macaddr']],
        "channel": [device['kismet.device.base.channel']],
        "first_seen": [device['kismet.device.base.first_time']], 
        "last_seen": [device['kismet.device.base.last_time']]

    }
    
    wlan_df = pd.concat([wlan_df, pd.DataFrame(wlan_data)], ignore_index=True)


# print(wlan_df.shape[0])
# #from GetFixtres import ECS_data
# ECS_data = pd.read_csv("/home/jasher4994/mysite/ECS_data.csv")
# #from GetFixtures2 import GK_roi
# GK_roi = pd.read_csv("/home/jasher4994/mysite/GK_roi.csv")


app = Flask(__name__)

#Pandas Page -- Currently displays WLAN data
@app.route('/')
@app.route('/pandas', methods=("POST", "GET"))
def GK():
    return render_template('pandas.html',
                           PageTitle = "Pandas",
                           table=[wlan_df.head().to_html(classes='data')], titles= wlan_df.columns.values)


#Matplotlib page
@app.route('/matplot', methods=("POST", "GET"))
def mpl():
    return render_template('matplot.html',
                           PageTitle = "Matplotlib")


@app.route('/plot.png')
def plot_png():
    fig = create_figure()

    # figfile = BytesIO()
    # fig.savefig(figfile, format='png')
    # fig.clf() # this will clear the image
    # figfile.seek(0)
    # figdata_png = base64.b64encode(figfile.getvalue())
    # return figdata_png.decode('UTF-8')

    # img_bytes = BytesIO()
    # fig.savefig(img_bytes)
    # img_bytes.seek(0)
    # return send_file(img_bytes, mimetype='image/png')

    # tmpfile = BytesIO()
    # fig.figure.savefig(tmpfile, format='png')
    # encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    # return encoded

    output = io.BytesIO()
    FigureCanvas(fig.figure).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig, ax = plt.subplots(figsize = (6,4))
    fig.patch.set_facecolor('#E8E5DA')
    # x = ECS_data.team
    # y = ECS_data.gw1
    # ax.bar(x, y, color = "#304C89")
    # plt.xticks(rotation = 30, size = 5)

    print(wlan_df['device_type'].value_counts())
    fig = wlan_df['device_type'].value_counts(dropna=True).plot(kind='bar', rot=0)
    # plt.show()
    plt.ylabel("Frequency Dist of Device Types", size = 10)

    fig = wlan_df['device_type'].value_counts(dropna=True).plot(kind='bar', rot=0)


    return fig


if __name__ == '__main__':
    app.run(debug = True)