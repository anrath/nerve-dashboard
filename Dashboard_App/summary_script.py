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
from pyvis.network import Network
from functools import reduce
import numpy as np
# from IPython.display import display, HTML
from datetime import datetime
import warnings
from io import BytesIO
import base64

# Opening JSON files / Data imports
with open('all.json', 'r') as openfile:
    all = json.load(openfile)

with open('phydot11_accesspoints.json', 'r') as openfile:
    aps = json.load(openfile)

with open('phy-Bluetooth.json', 'r') as openfile:
    blue = json.load(openfile)

with open('phy-IEEE802.11.json', 'r') as openfile:
    wlan = json.load(openfile)

#------------------------------------------------------------------------------------------------------------------

# Collecting data on all devices
all_df = pd.DataFrame()

for device in all:   
    try:
        x = [device['dot11.device']['dot11.device.probed_ssid_map'][0]['dot11.probedssid.ssid']]
    except KeyError:
        x = "None"
    all_data = {
        "key": [device['kismet.device.base.key']], 
        "device_name": [device['kismet.device.base.name']],
        "device_type": [device['kismet.device.base.type']],
        "num_packets": [device['kismet.device.base.packets.total']],
        "manuf": [device['kismet.device.base.manuf']], 
        "macaddr": [device['kismet.device.base.macaddr']],
        "channel": [device['kismet.device.base.channel']],
        "first_seen": [device['kismet.device.base.first_time']], 
        "last_seen": [device['kismet.device.base.last_time']],
        "server_uuid": [device['kismet.server.uuid']],
        "network": x
    }
    
    all_df = pd.concat([all_df, pd.DataFrame(all_data)], ignore_index=True)

# Collecting data on wlan devices
wlan_df = pd.DataFrame()

for device in wlan:
    try:
        x = [device['dot11.device']['dot11.device.probed_ssid_map'][0]['dot11.probedssid.ssid']]
    except KeyError:
        x = "None"    
    wlan_data = {
        "key": [device['kismet.device.base.key']], 
        "device_name": [device['kismet.device.base.name']],
        "device_type": [device['kismet.device.base.type']],
        "num_packets": [device['kismet.device.base.packets.total']],
        "manuf": [device['kismet.device.base.manuf']], 
        "macaddr": [device['kismet.device.base.macaddr']],
        "channel": [device['kismet.device.base.channel']],
        "first_seen": [device['kismet.device.base.first_time']], 
        "last_seen": [device['kismet.device.base.last_time']],
        "server_uuid": [device['kismet.server.uuid']],
        "network": x
    }
    
    wlan_df = pd.concat([wlan_df, pd.DataFrame(wlan_data)], ignore_index=True)

# Collecting data on bluetooth devices
blue_df = pd.DataFrame()

for device in blue:    
    blue_data = {
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
    
    blue_df = pd.concat([blue_df, pd.DataFrame(blue_data)], ignore_index=True)

# Collecting data on access points
aps_df = pd.DataFrame()

for device in aps:    
    aps_data = {
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
    
    aps_df = pd.concat([aps_df, pd.DataFrame(aps_data)], ignore_index=True)

#------------------------------------------------------------------------------------------------------------------
#FUNCTIONS: 

#get all df 
def get_all_df():
    return all_df

#get wlan df 
def get_summary_wlan_df():
    return wlan_df

#get blue df 
def get_blue_df():
    return blue_df

#get aps df 
def get_aps_df():
    return aps_df

# get graph of device counts
def get_dev_counts():
    devs = ['Total Devices', 'WLAN Devices', 'Bluetooth Devices', 'Access Points']
    devs_counts = [len(all_df), len(wlan_df), len(blue_df), len(aps_df)]
    x = np.char.array(devs)
    y = np.array(devs_counts)
    #fig = plt.figure()
    fig, ax = plt.subplots(figsize = (6,4))
    fig.patch.set_facecolor('#E8E5DA')
    yvalues = 0.1 + np.arange(len(devs_counts))
    plt.bar(x, y, color='green', figure=fig)
    yvalues += 0.4
    return fig

# get network data graph

# get manufacturer counts graph
def get_manuf_counts():
    dev_manuf = all_df['manuf'].value_counts().index.tolist()
    dev_manuf_counts = all_df['manuf'].value_counts().tolist()
    if(dev_manuf[0] == "Unknown"):
        dev_manuf.pop(0)
        dev_manuf_counts.pop(0)
    x = np.char.array(dev_manuf)
    y = np.array(dev_manuf_counts)
    fig, ax = plt.subplots(figsize = (6,7))
    plt.xticks(rotation=90)
    fig.set_tight_layout(True)
    fig.patch.set_facecolor('#E8E5DA')
    plt.bar(x, y, figure=fig)
    # fig = all_df['manuf'].value_counts().plot(kind='bar', ylabel="Number of Devices", xlabel="Manufacturer")
    return fig

# get manufacturer count percentage pie chart
def get_manuf_count_piechart():
    # manufacturers = all_df['manuf'].value_counts().index.tolist()
    # man_counts = all_df['manuf'].value_counts().tolist()

    # x = np.char.array(manufacturers)
    # y = np.array(man_counts)
    # percents = 100.*y/y.sum()
    # fig, ax = plt.subplots(figsize = (6,4))
    # fig.patch.set_facecolor('#E8E5DA')
    # plt.pie(y, figure=fig)
    # labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(x, percents)]

    # sort_legend = True
    # if sort_legend:
    #     fig, labels, dummy =  zip(*sorted(zip(fig, labels, y),
    #                                         key=lambda x: x[2],
    #                                         reverse=True))

    # plt.legend(fig, labels, loc='upper right', bbox_to_anchor=(-0.1, 1.),
    #         fontsize=8, title='Device Manufacturers')

    # #plt.savefig('piechart.png', bbox_inches='tight')
    # #fig = 'piechart.png'
    # return fig
    fig, ax = plt.subplots(figsize = (8,7))
    fig.set_tight_layout(True)
    fig.patch.set_facecolor('#E8E5DA')
    
    fig = all_df[~all_df["manuf"].str.contains('Unknown', na=False)]['manuf'].value_counts().plot(kind='pie', legend=True, title="Device Manufacturers", labeldistance=None, ylabel="Frequency Distribution of Device Manufacturer") #autopct="%1.0f%%"
    
    fig.legend(loc='upper right', bbox_to_anchor=(-0.1, 1.),
            fontsize=8, title='Device Manufacturers')
    #plt.ylabel("Frequency Distribution of Device Manufacturer", size = 10)

    return fig

# get device type percentage pie chart
def get_dev_type_piechart():
    # dev_types = all_df['device_type'].value_counts().index.tolist()
    # dev_type_counts = all_df['device_type'].value_counts().tolist()

    # x = np.char.array(dev_types)
    # y = np.array(dev_type_counts)
    # percents = 100.*y/y.sum()
    # patches, texts = plt.pie(y)
    # labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(x, percents)]

    # sort_legend = True
    # if sort_legend:
    #     patches, labels, dummy =  zip(*sorted(zip(patches, labels, y),
    #                                         key=lambda x: x[2],
    #                                         reverse=True))

    # plt.legend(patches, labels, loc='upper right', bbox_to_anchor=(-0.1, 1.),
    #         fontsize=8, title='Device Types')

    # plt.savefig('type_piechart.png', bbox_inches='tight')
    # fig = 'type_piechart.png'
    # return fig
    fig, ax = plt.subplots(figsize = (7,6))
    fig.patch.set_facecolor('#E8E5DA')

    fig = all_df[~all_df["device_type"].str.contains('Unknown', na=False)]['device_type'].value_counts().plot(kind='pie', legend=True, title="Device Types", labeldistance=None) #autopct="%1.0f%%"
    fig.legend(loc='upper right', bbox_to_anchor=(1.2, 1.),
            fontsize=8, title='Device Types')

    plt.ylabel("Frequency Distribution of Device Type", size = 10)

    return fig