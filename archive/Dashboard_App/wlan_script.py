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

#------------------------------------------------------------------------------------------------------------------

#WLAN data
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


#Time data 
#getting time data associated with a specific device (id'd by macaddr)
time_data = wlan_df[["macaddr",  "num_packets", "first_seen", "last_seen"]]
diff = time_data['last_seen'] - time_data['first_seen']
hours = diff / 3600
time_data['time_between (hours)'] = hours

#converting unix timestamp to a readable string version for viewing
for i in time_data['first_seen'].values:
    new_i = datetime.utcfromtimestamp(int(i)).strftime('%Y-%m-%d %H:%M:%S')
    time_data['first_seen'].replace(i, new_i, inplace = True)
for i in time_data['last_seen'].values:
    new_i = datetime.utcfromtimestamp(int(i)).strftime('%Y-%m-%d %H:%M:%S')
    time_data['last_seen'].replace(i, new_i, inplace = True)


#------------------------------------------------------------------------------------------------------------------

#FUNCTIONS:

#get WLAN df 
def get_wlan_df():
    return wlan_df

#Device Type Bar Chart
def wlan_devicetype_dist():
    fig, ax = plt.subplots(figsize = (6,4))
    fig.patch.set_facecolor('#E8E5DA')

    fig = wlan_df['device_type'].value_counts(dropna=True).plot(kind='bar', rot=0)
    plt.ylabel("Frequency Dist of Device Types", size = 10)

    return fig

#Device Name Pie Chart
def wlan_devicename_dist():
    fig, ax = plt.subplots(figsize = (6,4))
    fig.patch.set_facecolor('#E8E5DA')

    fig = wlan_df['device_name'].value_counts(dropna=True).plot(kind='pie',legend=True, title="Device Names", labeldistance=None) #autopct="%1.0f%%"
    plt.ylabel("Frequency Dist of Device Names", size = 10)

    return fig

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
