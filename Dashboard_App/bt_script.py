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
with open('../api/devices/phy-Bluetooth.json') as openfile:
    bt = json.load(openfile)

#------------------------------------------------------------------------------------------------------------------

#WLAN data
bt_df = pd.DataFrame()

for device in bt:    
    bt_data = {
        "key": [device['kismet.device.base.key']], 
        "device_name": [device['kismet.device.base.name']],
        "device_type": [device['kismet.device.base.type']],
        "num_packets": [device['kismet.device.base.packets.total']],
        "manuf": [device['kismet.device.base.manuf']], 
        "macaddr": [device['kismet.device.base.macaddr']],
        "channel": [device['kismet.device.base.channel']],
        "first_seen": [device['kismet.device.base.first_time']], 
        "last_seen": [device['kismet.device.base.last_time']],
        "server_uuid": [device['kismet.server.uuid']]
    }
    
    bt_df = pd.concat([bt_df, pd.DataFrame(bt_data)], ignore_index=True)


#Time data 
bt_time_data = bt_df.copy()
diff = bt_time_data['last_seen'] - bt_time_data['first_seen']
hours = diff / 3600
bt_time_data['time_between (hours)'] = hours


#------------------------------------------------------------------------------------------------------------------

#FUNCTIONS:
def bt_params():
    params={"test": 1}
    #params['namedesc'] = bt_df[~bt_df["device_name"].str.contains(':', na=False)]['device_name'].value_counts().sum()
    #params['name_nondesc'] = bt_df[bt_df["device_name"].str.contains(':', na=False)]['device_name'].value_counts().sum()
    pjson = json.dumps(params)
    return pjson

#Device Type Bar Chart
def bt_devicetype_dist():
    fig, ax = plt.subplots(figsize = (6,6))

    fig = bt_time_data['device_type'].value_counts().plot(kind='bar')
    plt.xlabel('Device Type')
    plt.ylabel('Count')
    plt.title('Device Type Distribution')
    plt.close()
    plt.figure().clear()

    return fig

#Device Name Pie Chart
def bt_devicename_dist():
    fig_name = plt.subplots(figsize = (7,4))

    fig_name = bt_df[~bt_df["device_name"].str.contains(':', na=False)]['device_name'].value_counts().plot(kind='pie', legend=True, title="Device Names", labeldistance=None, ylabel='')
    fig_name.legend(bbox_to_anchor=(1, 1.02), loc='upper left')
    fig_name.set_title('Descriptive Device Names')
    plt.close()
    plt.figure().clear()

    return fig_name

#Device Manufacturer Pie Chart
def bt_manuf_dist():

    fig_m = bt_df[~bt_df["manuf"].str.contains('Unknown', na=False)]['manuf'].value_counts().plot(kind='pie')
    fig_m.legend(bbox_to_anchor=(1, 1.02), loc='upper left')
    fig_m.set_title('Manufacturer Distribution')
    plt.close()
    plt.figure().clear()

    return fig_m

'''

#Device Manufacturer Pie Chart
def wlan_manuf_dist():
    fig, ax = plt.subplots(figsize = (6,4))
    fig.patch.set_facecolor('#E8E5DA')

    fig = wlan_df[~wlan_df["manuf"].str.contains('Unknown', na=False)]['manuf'].value_counts().plot(kind='pie', legend=True, title="Device Manufacturers", labeldistance=None) #autopct="%1.0f%%"
    fig.legend(bbox_to_anchor=(1, 2.15), loc='upper left')

    plt.ylabel("Frequency Dist of Device Manufacturer", size = 10)

    return fig

#Graph of time_between (last_seen - first_seen) for each device
def time_data_graph():
    fig, ax = plt.subplots(figsize = (6,4))
    fig.patch.set_facecolor('#E8E5DA')

    fig = time_data.reset_index().plot(x="index",  y=["time_between (hours)"], xticks=[], kind="bar", rot=0)
    plt.ylabel("Graph of time between for each device", size = 10)

    return fig

#Scatter plot of time : num-packets
def time_pck_scatter():
    fig, ax = plt.subplots(figsize = (6,4))
    fig.patch.set_facecolor('#E8E5DA')

    fig = time_data.plot.scatter('time_between (hours)', 'num_packets')
    plt.ylabel("Scatter Plot of time between vs # packets", size = 10)

    return fig

#Histogram of packet data
def pck_hist():
    fig, ax = plt.subplots(figsize = (6,4))
    fig.patch.set_facecolor('#E8E5DA')

    fig = wlan_df['num_packets'].hist(bins=20)
    plt.ylabel("Histogram of Packet Data", size = 10)

    return fig


'''