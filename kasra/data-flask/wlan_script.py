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
import os
# from IPython.display import display, HTML
from datetime import datetime
import warnings
from io import BytesIO
import base64

#------------------------------------------------------------------------------------------------------------------

#FUNCTIONS:

#get WLAN df 
def get_wlan_df():
    return wlan_df

#Device Type Bar Chart
def wlan_devicetype_dist(file_name="wlan_devicetype_dist.png"):
    fig, ax = plt.subplots(figsize = (6,4))
    fig.patch.set_facecolor('#E8E5DA')

    fig = wlan_df['device_type'].value_counts(dropna=True).plot(kind='bar', rot=0)
    plt.ylabel("Frequency Dist of Device Types", size = 10)

    plt.savefig(f'{IMG_PATH}/{file_name}')
    return fig

#Device Name Pie Chart
def wlan_devicename_dist(file_name="wlan_devicename_dist.png"):
    fig, ax = plt.subplots(figsize = (6,4))
    fig.patch.set_facecolor('#E8E5DA')

    fig = wlan_df['device_name'].value_counts(dropna=True).plot(kind='pie',legend=True, title="Device Names", labeldistance=None) #autopct="%1.0f%%"
    plt.ylabel("Frequency Dist of Device Names", size = 10)

    plt.savefig(f'{IMG_PATH}/{file_name}')
    return fig

#Device Manufacturer Pie Chart
def wlan_manuf_dist(file_name="wlan_manuf_dist.png"):
    fig, ax = plt.subplots(figsize = (6,4))
    fig.patch.set_facecolor('#E8E5DA')

    fig = wlan_df[~wlan_df["manuf"].str.contains('Unknown', na=False)]['manuf'].value_counts().plot(kind='pie', legend=True, title="Device Manufacturers", labeldistance=None) #autopct="%1.0f%%"
    fig.legend(bbox_to_anchor=(1, 2.15), loc='upper left')

    plt.ylabel("Frequency Dist of Device Manufacturer", size = 10)

    plt.savefig(f'{IMG_PATH}/{file_name}')
    return fig

#Graph of time_between (last_seen - first_seen) for each device
def time_data_graph(file_name="time_data_graph.png"):
    fig, ax = plt.subplots(figsize = (6,4))
    fig.patch.set_facecolor('#E8E5DA')

    fig = time_data.reset_index().plot(x="index",  y=["time_between (hours)"], xticks=[], kind="bar", rot=0)
    plt.ylabel("Graph of time between for each device", size = 10)

    plt.savefig(f'{IMG_PATH}/{file_name}')
    return fig

#Scatter plot of time : num-packets
def time_pck_scatter(file_name="time_pck_scatter.png"):
    fig, ax = plt.subplots(figsize = (6,4))
    fig.patch.set_facecolor('#E8E5DA')

    fig = time_data.plot.scatter('time_between (hours)', 'num_packets')
    plt.ylabel("Scatter Plot of time between vs # packets", size = 10)

    plt.savefig(f'{IMG_PATH}/{file_name}')
    return fig

#Histogram of packet data
def pck_hist(file_name="pck_hist.png"):
    fig, ax = plt.subplots(figsize = (6,4))
    fig.patch.set_facecolor('#E8E5DA')

    fig = wlan_df['num_packets'].hist(bins=20)
    plt.ylabel("Histogram of Packet Data", size = 10)


    plt.savefig(f'{IMG_PATH}/{file_name}')
    return fig


#------------------------------------------------------------------------------------------------------------------
DATA_PATH = './data'
DATA_SUB_PATH = ['campus', 'flats']
IMG_PATH = './apps/static/assets/images/wlan'

for sub_path in DATA_SUB_PATH:
    #Data imports

    #WLAN data
    wlan_df = pd.read_json(f'{DATA_PATH}/{sub_path}/phy-IEEE802.11.json')
    wlan_df = wlan_df[['kismet.device.base.key', 'kismet.device.base.name', 'kismet.device.base.type', 'kismet.device.base.packets.total', 'kismet.device.base.manuf', 'kismet.device.base.macaddr', 'kismet.device.base.channel', 'kismet.device.base.first_time', 'kismet.device.base.last_time']]
    wlan_df.rename(columns={
        'kismet.device.base.key': 'key', 
        'kismet.device.base.name': 'device_name', 
        'kismet.device.base.type': 'device_type', 
        'kismet.device.base.packets.total': 'num_packets', 
        'kismet.device.base.manuf': 'manuf', 
        'kismet.device.base.macaddr': 'macaddr', 
        'kismet.device.base.channel': 'channel', 
        'kismet.device.base.first_time': 'first_seen', 
        'kismet.device.base.last_time': 'last_seen'
        }, inplace=True)


    #Time data 
    #getting time data associated with a specific device (id'd by macaddr)
    time_data = wlan_df[["macaddr",  "num_packets", "first_seen", "last_seen"]]
    diff = time_data['last_seen'] - time_data['first_seen']
    hours = diff.apply(lambda x: x.total_seconds() / 3600)
    time_data['time_between (hours)'] = hours

    #converting unix timestamp to a readable string version for viewing
    time_data['first_seen'] = time_data.apply(lambda row: row['first_seen'].strftime('%Y-%m-%d %H:%M:%S'), axis=1)
    time_data['last_seen'] = time_data.apply(lambda row: row['last_seen'].strftime('%Y-%m-%d %H:%M:%S'), axis=1)


    if(not os.path.isfile(f'{IMG_PATH}/wlan_devicetype_dist_{sub_path}.png')):
        wlan_devicetype_dist(f'wlan_devicetype_dist_{sub_path}.png')

    if(not os.path.isfile(f'{IMG_PATH}/wlan_devicename_dist_{sub_path}.png')):
        wlan_devicename_dist(f'wlan_devicename_dist_{sub_path}.png')

    if(not os.path.isfile(f'{IMG_PATH}/wlan_manuf_dist_{sub_path}.png')):
        wlan_manuf_dist(f'wlan_manuf_dist_{sub_path}.png')

    if(not os.path.isfile(f'{IMG_PATH}/time_data_graph_{sub_path}.png')):
        time_data_graph(f'time_data_graph_{sub_path}.png')

    if(not os.path.isfile(f'{IMG_PATH}/time_pck_scatter_{sub_path}.png')):
        time_pck_scatter(f'time_pck_scatter_{sub_path}.png')

    if(not os.path.isfile(f'{IMG_PATH}/pck_hist_{sub_path}.png')):
        pck_hist(f'pck_hist_{sub_path}.png')
