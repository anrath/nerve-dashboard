#Flask imports
import os
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
import requests

bt_df = pd.DataFrame()
bt_time_data = pd.DataFrame()

#------------------------------------------------------------------------------------------------------------------

#FUNCTIONS:

def bt_params():
    params={}
    params['name_desc'] = int(bt_df[~bt_df["device_name"].str.contains(':', na=False)]['device_name'].value_counts().sum())
    params['name_nondesc'] = int(bt_df[bt_df["device_name"].str.contains(':', na=False)]['device_name'].value_counts().sum())
    params['manuf_unknown'] = int(bt_df[~bt_df["manuf"].str.contains('Unknown', na=False)]['manuf'].value_counts().sum())
    params['manuf_known'] = int(bt_df[bt_df["manuf"].str.contains('Unknown', na=False)]['manuf'].value_counts().sum())
    params['num_devices'] = len(bt_df. index)
    return params

#Device Type Bar Chart
def bt_devicetype_dist(bt_time_data, file_name="bt_devicetype_dist.png"):
    fig, ax = plt.subplots(figsize = (6,4))
    fig.patch.set_facecolor('#E8E5DA')

    fig = bt_time_data['device_type'].value_counts().plot(kind='bar')
    plt.xlabel('Device Type')
    plt.ylabel('Count')
    plt.title('Device Type Distribution')
    
    plt.savefig(f'{IMG_PATH}/{file_name}')
    return fig

#Device Name Pie Chart
def bt_devicename_dist(bt_df, file_name="bt_devicename_dist.png"):
    fig, ax = plt.subplots(figsize = (6,4))
    fig.patch.set_facecolor('#E8E5DA')

    fig = bt_df[~bt_df["device_name"].str.contains(':', na=False)]['device_name'].value_counts().plot(kind='pie', legend=True, title="Device Names", labeldistance=None, ylabel='')
    fig.legend(bbox_to_anchor=(1, 1.02), loc='upper left')
    fig.set_title('Descriptive Device Names')
    
    plt.savefig(f'{IMG_PATH}/{file_name}')
    return fig

#Device Manufacturer Pie Chart
def bt_manuf_dist(bt_df, file_name="bt_manuf_dist.png"):
    fig, ax = plt.subplots(figsize = (6,4))
    fig.patch.set_facecolor('#E8E5DA')

    fig = bt_df[~bt_df["manuf"].str.contains('Unknown', na=False)]['manuf'].value_counts().plot(kind='pie', legend=True, title="Device Manufacturers", labeldistance=None, ylabel='')
    fig.legend(bbox_to_anchor=(1, 1.02), loc='upper left')
    fig.set_title('Manufacturer Distribution')

    plt.savefig(f'{IMG_PATH}/{file_name}')
    return fig

#Histogram of packet data
def bt_pck_hist(bt_df, file_name="bt_pck_hist.png"):
    fig, ax = plt.subplots(figsize = (6,4))
    fig.patch.set_facecolor('#E8E5DA')

    fig = bt_df['num_packets'].hist(bins=20)
    fig.set_title('Histogram of Packets')

    plt.savefig(f'{IMG_PATH}/{file_name}')
    return fig

#Zoomed histogram of packet data
def zoomed_bt_pck_hist(bt_df, file_name="zoomed_bt_pck_hist.png"):
    fig, ax = plt.subplots(figsize = (6,4))
    fig.patch.set_facecolor('#E8E5DA')

    fig = bt_df[bt_df['num_packets']<200]['num_packets'].hist(bins=20)
    fig.set_title('Zoomed Histogram of Packets')

    plt.savefig(f'{IMG_PATH}/{file_name}')
    return fig

#Graph of num_packets vs time between
def pck_vs_time(bt_time_data, file_name="pck_vs_time.png"):
    fig, ax = plt.subplots(figsize = (6,4))
    fig.patch.set_facecolor('#E8E5DA')

    bt_time_data.plot.scatter('time_between (hours)', 'num_packets')

    plt.savefig(f'{IMG_PATH}/{file_name}')
    return fig

def create_bt_graphs(sub_path):
    if sub_path == 'realtime':
        user_password = "http://sniffer:sniffer@"
        server_ip = "172.26.99.45:2501/"

        # Retrieved from: 
        # endpoint = "/devices/views/all_views.json"
        bluetooth_VIEWID = "phy-Bluetooth"

        endpoint = f"/devices/views/{bluetooth_VIEWID}/devices.json"
        x = requests.get(user_password + server_ip + endpoint, headers={"KISMET": "E62F6C667B3CF269798AC58E0D811D85"})
        bt = x.json()
        bt_df = pd.DataFrame(bt)
        bt_df = bt_df[['kismet.device.base.key', 'kismet.device.base.name', 'kismet.device.base.type', 'kismet.device.base.packets.total', 'kismet.device.base.manuf', 'kismet.device.base.macaddr', 'kismet.device.base.channel', 'kismet.device.base.first_time', 'kismet.device.base.last_time']]
        bt_df.rename(columns={
            'kismet.device.base.key': 'key', 
            'kismet.device.base.name': 'device_name', 
            'kismet.device.base.type': 'device_type', 
            'kismet.device.base.packets.total': 'num_packets', 
            'kismet.device.base.manuf': 'manuf', 
            'kismet.device.base.macaddr': 'macaddr', 
            'kismet.device.base.channel': 'channel', 
            'kismet.device.base.first_time': 'first_seen', 
            'kismet.device.base.last_time': 'last_seen',
            }, inplace=True)
    
    else:
        bt_df = pd.read_json(f'{DATA_PATH}/{sub_path}/phy-Bluetooth.json')
        bt_df = bt_df[['kismet.device.base.key', 'kismet.device.base.name', 'kismet.device.base.type', 'kismet.device.base.packets.total', 'kismet.device.base.manuf', 'kismet.device.base.macaddr', 'kismet.device.base.channel', 'kismet.device.base.first_time', 'kismet.device.base.last_time']]
        bt_df.rename(columns={
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
    # bt_time_data = bt_df.copy()
    # diff = bt_time_data['last_seen'] - bt_time_data['first_seen']
    # hours = hours = diff / 3600
    # bt_time_data['time_between (hours)'] = hours

    #Time data 
    #getting time data associated with a specific device (id'd by macaddr)
    bt_time_data = bt_df.copy()
    if sub_path == 'realtime':
        bt_time_data['first_seen'] = bt_time_data.apply(lambda row: datetime.utcfromtimestamp(row['first_seen']), axis=1)
        bt_time_data['last_seen'] = bt_time_data.apply(lambda row: datetime.utcfromtimestamp(row['last_seen']), axis=1)
    diff = bt_time_data['last_seen'] - bt_time_data['first_seen']
    hours = diff.apply(lambda x: x.total_seconds() / 3600)
    bt_time_data['time_between (hours)'] = hours

    #converting unix timestamp to a readable string version for viewing
    bt_time_data['first_seen'] = bt_time_data.apply(lambda row: row['first_seen'].strftime('%Y-%m-%d %H:%M:%S'), axis=1)
    bt_time_data['last_seen'] = bt_time_data.apply(lambda row: row['last_seen'].strftime('%Y-%m-%d %H:%M:%S'), axis=1)

    bt_devicetype_dist(bt_time_data, f'bt_devicetype_dist_{sub_path}.png')
    bt_devicename_dist(bt_df, f'bt_devicename_dist_{sub_path}.png')
    bt_manuf_dist(bt_df, f'bt_manuf_dist_{sub_path}.png')
    bt_pck_hist(bt_df, f'bt_pck_hist_{sub_path}.png')
    zoomed_bt_pck_hist(bt_df, f'zoomed_bt_pck_hist_{sub_path}.png')
    pck_vs_time(bt_time_data, f'pck_vs_time_{sub_path}.png')


#------------------------------------------------------------------------------------------------------------------
DATA_PATH = './data'
DATA_SUB_PATH = ['campus', 'flats']
IMG_PATH = './apps/static/assets/images/bt'


for sub_path in DATA_SUB_PATH:
    create_bt_graphs(sub_path)
