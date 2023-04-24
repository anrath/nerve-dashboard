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
import requests

#------------------------------------------------------------------------------------------------------------------

#FUNCTIONS:

#get WLAN df 
def get_wlan_df():
    return wlan_df

#Device Type Bar Chart
def wlan_devicetype_dist(wlan_df, file_name="wlan_devicetype_dist.png"):
    fig, ax = plt.subplots(figsize = (6,4))
    fig.patch.set_facecolor('#E8E5DA')

    fig = wlan_df['device_type'].value_counts(dropna=True).plot(kind='bar', rot=0)
    plt.ylabel("Frequency Dist of Device Types", size = 10)

    plt.savefig(f'{IMG_PATH}/{file_name}')
    return fig

#Device Name Pie Chart
def wlan_devicename_dist(wlan_df, file_name="wlan_devicename_dist.png"):
    fig, ax = plt.subplots(figsize = (6,4))
    fig.patch.set_facecolor('#E8E5DA')

    fig = wlan_df['device_name'].value_counts(dropna=True).plot(kind='bar', rot=0)#(kind='pie',legend=True, title="Device Names", labeldistance=None) #autopct="%1.0f%%"
    # fig.legend(bbox_to_anchor=(2, 3.15), loc='upper left')
    plt.ylabel("Frequency Dist of Device Names", size = 10)

    plt.savefig(f'{IMG_PATH}/{file_name}')
    return fig

#Device Manufacturer Pie Chart
def wlan_manuf_dist(wlan_df, file_name="wlan_manuf_dist.png"):
    fig, ax = plt.subplots(figsize = (6,4))
    fig.patch.set_facecolor('#E8E5DA')

    fig = wlan_df[~wlan_df["manuf"].str.contains('Unknown', na=False)]['manuf'].value_counts().plot(kind='pie', legend=True, title="Device Manufacturers", labeldistance=None) #autopct="%1.0f%%"
    # fig.legend(bbox_to_anchor=(1, 2.15), loc='upper left')
    fig.legend(bbox_to_anchor = (1.25, 0.6), loc='center right')
    plt.tight_layout()

    plt.ylabel("Frequency Dist of Device Manufacturer", size = 10)

    plt.savefig(f'{IMG_PATH}/{file_name}')
    return fig

#Graph of time_between (last_seen - first_seen) for each device
def time_data_graph(time_data, file_name="time_data_graph.png"):
    fig, ax = plt.subplots(figsize = (6,4))
    fig.patch.set_facecolor('#E8E5DA')

    fig = time_data.reset_index().plot(x="index",  y=["time_between (hours)"], xticks=[], kind="bar", rot=0)
    plt.ylabel("Graph of time between for each device", size = 10)

    plt.savefig(f'{IMG_PATH}/{file_name}')
    return fig

#Scatter plot of time : num-packets
def time_pck_scatter(time_data, file_name="time_pck_scatter.png"):
    fig, ax = plt.subplots(figsize = (6,4))
    fig.patch.set_facecolor('#E8E5DA')

    fig = time_data.plot.scatter('time_between (hours)', 'num_packets', logx=True)
    plt.ylabel("Scatter Plot of time between vs # packets", size = 10)
    plt.xscale("log")

    plt.savefig(f'{IMG_PATH}/{file_name}')
    return fig

#Histogram of packet data
def pck_hist(wlan_df, file_name="pck_hist.png"):
    fig, ax = plt.subplots(figsize = (6,4))
    fig.patch.set_facecolor('#E8E5DA')

    fig = wlan_df['num_packets'].hist(bins=20)
    plt.ylabel("Histogram of Packet Data", size = 10)

    plt.savefig(f'{IMG_PATH}/{file_name}')
    return fig

def create_wlan_graphs(sub_path):
    if sub_path == 'realtime':
        user_password = "http://sniffer:sniffer@"
        server_ip = "172.26.99.45:2501/"

        # Retrieved from: 
        # endpoint = "/devices/views/all_views.json"
        IEEE802_11_VIEWID = "phy-IEEE802.11"

        endpoint = f"/devices/views/{IEEE802_11_VIEWID}/devices.json"
        x = requests.get(user_password + server_ip + endpoint, headers={"KISMET": "E62F6C667B3CF269798AC58E0D811D85"})
        wlan = x.json()
        wlan_df = pd.DataFrame(wlan)
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

    else:
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
    if sub_path == 'realtime':
        time_data['first_seen'] = time_data.apply(lambda row: datetime.utcfromtimestamp(row['first_seen']), axis=1)
        time_data['last_seen'] = time_data.apply(lambda row: datetime.utcfromtimestamp(row['last_seen']), axis=1)
    diff = time_data['last_seen'] - time_data['first_seen']
    hours = diff.apply(lambda x: x.total_seconds() / 3600)
    time_data['time_between (hours)'] = hours

    #converting unix timestamp to a readable string version for viewing
    time_data['first_seen'] = time_data.apply(lambda row: row['first_seen'].strftime('%Y-%m-%d %H:%M:%S'), axis=1)
    time_data['last_seen'] = time_data.apply(lambda row: row['last_seen'].strftime('%Y-%m-%d %H:%M:%S'), axis=1)


    wlan_devicetype_dist(wlan_df, f'wlan_devicetype_dist_{sub_path}.png')
    wlan_devicename_dist(wlan_df, f'wlan_devicename_dist_{sub_path}.png')
    wlan_manuf_dist(wlan_df, f'wlan_manuf_dist_{sub_path}.png')
    time_data_graph(time_data, f'time_data_graph_{sub_path}.png')
    time_pck_scatter(time_data, f'time_pck_scatter_{sub_path}.png')
    pck_hist(wlan_df, f'pck_hist_{sub_path}.png')

#------------------------------------------------------------------------------------------------------------------
DATA_PATH = './data'
DATA_SUB_PATH = ['campus', 'flats']
IMG_PATH = './apps/static/assets/images/wlan'

for sub_path in DATA_SUB_PATH:
    create_wlan_graphs(sub_path)
