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
with open('../api_campus_large/api/devices/all.json', 'r') as openfile:
    brown_all = json.load(openfile)

with open('../api_campus_large/api/devices/phydot11_accesspoints.json', 'r') as openfile:
    brown_aps = json.load(openfile)

with open('../api_campus_large/api/devices/phy-Bluetooth.json', 'r') as openfile:
    brown_blue = json.load(openfile)

with open('../api_campus_large/api/devices/phy-IEEE802.11.json', 'r') as openfile:
    brown_wlan = json.load(openfile)

with open('../api_flats/api_flats/devices/all.json', 'r') as openfile:
    flats_all = json.load(openfile)

with open('../api_flats/api_flats/devices/phydot11_accesspoints.json', 'r') as openfile:
    flats_aps = json.load(openfile)

with open('../api_flats/api_flats/devices/phy-Bluetooth.json', 'r') as openfile:
    flats_blue = json.load(openfile)

with open('../api_flats/api_flats/devices/phy-IEEE802.11.json', 'r') as openfile:
    flats_wlan = json.load(openfile)

#------------------------------------------------------------------------------------------------------------------

# Collecting data on all brown devices
brown_all_df = pd.DataFrame()

for device in brown_all:   
    try:
        x = [device['dot11.device']['dot11.device.probed_ssid_map'][0]['dot11.probedssid.ssid']]
    except KeyError:
        x = "None"
    brown_all_data = {
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
    
    brown_all_df = pd.concat([brown_all_df, pd.DataFrame(brown_all_data)], ignore_index=True)

# Collecting data on brown wlan devices
brown_wlan_df = pd.DataFrame()

for device in brown_wlan:
    try:
        x = [device['dot11.device']['dot11.device.probed_ssid_map'][0]['dot11.probedssid.ssid']]
    except KeyError:
        x = "None"    
    brown_wlan_data = {
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
    
    brown_wlan_df = pd.concat([brown_wlan_df, pd.DataFrame(brown_wlan_data)], ignore_index=True)

# Collecting data on brown bluetooth devices
brown_blue_df = pd.DataFrame()

for device in brown_blue:    
    brown_blue_data = {
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
    
    brown_blue_df = pd.concat([brown_blue_df, pd.DataFrame(brown_blue_data)], ignore_index=True)

# Collecting data on brown access points
brown_aps_df = pd.DataFrame()

for device in brown_aps:    
    brown_aps_data = {
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
    
    brown_aps_df = pd.concat([brown_aps_df, pd.DataFrame(brown_aps_data)], ignore_index=True)

# Collecting data on all flats devices
flats_all_df = pd.DataFrame()

for device in flats_all:   
    try:
        x = [device['dot11.device']['dot11.device.probed_ssid_map'][0]['dot11.probedssid.ssid']]
    except KeyError:
        x = "None"
    flats_all_data = {
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
    
    flats_all_df = pd.concat([flats_all_df, pd.DataFrame(flats_all_data)], ignore_index=True)

# Collecting data on flats wlan devices
flats_wlan_df = pd.DataFrame()

for device in flats_wlan:
    try:
        x = [device['dot11.device']['dot11.device.probed_ssid_map'][0]['dot11.probedssid.ssid']]
    except KeyError:
        x = "None"    
    flats_wlan_data = {
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
    
    flats_wlan_df = pd.concat([flats_wlan_df, pd.DataFrame(flats_wlan_data)], ignore_index=True)

# Collecting data on flats bluetooth devices
flats_blue_df = pd.DataFrame()

for device in flats_blue:    
    flats_blue_data = {
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
    
    flats_blue_df = pd.concat([flats_blue_df, pd.DataFrame(flats_blue_data)], ignore_index=True)

# Collecting data on flats access points
flats_aps_df = pd.DataFrame()

for device in flats_aps:    
    flats_aps_data = {
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
    
    flats_aps_df = pd.concat([flats_aps_df, pd.DataFrame(flats_aps_data)], ignore_index=True)

#------------------------------------------------------------------------------------------------------------------
#FUNCTIONS: 

#get brown all df 
def get_brown_all_df():
    return brown_all_df

#get brown wlan df 
def get_brown_summary_wlan_df():
    return brown_wlan_df

#get brown blue df 
def get_brown_blue_df():
    return brown_blue_df

#get brown aps df 
def get_brown_aps_df():
    return brown_aps_df

#get flats all df 
def get_flats_all_df():
    return flats_all_df

#get flats wlan df 
def get_flats_summary_wlan_df():
    return flats_wlan_df

#get flats blue df 
def get_flats_blue_df():
    return flats_blue_df

#get flats aps df 
def get_flats_aps_df():
    return flats_aps_df

# get graph of brown device counts
def get_brown_dev_counts():
    devs = ['Total Devices', 'WLAN Devices', 'Bluetooth Devices', 'Access Points']
    devs_counts = [len(brown_all_df), len(brown_wlan_df), len(brown_blue_df), len(brown_aps_df)]
    x = np.char.array(devs)
    y = np.array(devs_counts)
    #fig = plt.figure()
    fig, ax = plt.subplots(figsize = (7,4))
    fig.patch.set_facecolor('#E8E5DA')
    yvalues = 0.1 + np.arange(len(devs_counts))
    plt.bar(x, y, color='green', figure=fig)
    yvalues += 0.4
    return fig

# get network data graph

# get brown manufacturer counts graph
def get_brown_manuf_counts():
    dev_manuf = brown_all_df['manuf'].value_counts().index.tolist()
    dev_manuf_counts = brown_all_df['manuf'].value_counts().tolist()
    if(dev_manuf[0] == "Unknown"):
        dev_manuf.pop(0)
        dev_manuf_counts.pop(0)
    x = np.char.array(dev_manuf)
    y = np.array(dev_manuf_counts)
    fig, ax = plt.subplots(figsize = (8,7))
    plt.xticks(rotation=90)
    fig.set_tight_layout(True)
    fig.patch.set_facecolor('#E8E5DA')
    plt.bar(x, y, figure=fig)
    # fig = all_df['manuf'].value_counts().plot(kind='bar', ylabel="Number of Devices", xlabel="Manufacturer")
    return fig

# get brown manufacturer count percentage pie chart
def get_brown_manuf_count_piechart():
    fig, ax = plt.subplots(figsize = (9,10))
    fig.set_tight_layout(True)
    fig.patch.set_facecolor('#E8E5DA')
    
    fig = brown_all_df[~brown_all_df["manuf"].str.contains('Unknown', na=False)]['manuf'].value_counts().plot(kind='pie', legend=True, title="Device Manufacturers", labeldistance=None, ylabel="Frequency Distribution of Device Manufacturer") #autopct="%1.0f%%"
    
    fig.legend(loc='upper right', bbox_to_anchor=(-0.1, 1.),
            fontsize=8, title='Device Manufacturers')
    #plt.ylabel("Frequency Distribution of Device Manufacturer", size = 10)

    return fig

# get brown device type percentage pie chart
def get_brown_dev_type_piechart():
    fig, ax = plt.subplots(figsize = (7,6))
    fig.patch.set_facecolor('#E8E5DA')

    fig = brown_all_df[~brown_all_df["device_type"].str.contains('Unknown', na=False)]['device_type'].value_counts().plot(kind='pie', legend=True, title="Device Types", labeldistance=None) #autopct="%1.0f%%"
    fig.legend(loc='upper right', bbox_to_anchor=(1.2, 1.),
            fontsize=8, title='Device Types')

    plt.ylabel("Frequency Distribution of Device Type", size = 10)

    return fig

# get graph of flats device counts
def get_flats_dev_counts():
    devs = ['Total Devices', 'WLAN Devices', 'Bluetooth Devices', 'Access Points']
    devs_counts = [len(flats_all_df), len(flats_wlan_df), len(flats_blue_df), len(flats_aps_df)]
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

# get flats manufacturer counts graph
def get_flats_manuf_counts():
    dev_manuf = flats_all_df['manuf'].value_counts().index.tolist()
    dev_manuf_counts = flats_all_df['manuf'].value_counts().tolist()
    if(dev_manuf[0] == "Unknown"):
        dev_manuf.pop(0)
        dev_manuf_counts.pop(0)
    x = np.char.array(dev_manuf)
    y = np.array(dev_manuf_counts)
    fig, ax = plt.subplots(figsize = (6,7))
    plt.xticks(rotation=90)
    fig.set_tight_layout(True)
    fig.patch.set_facecolor('#E8E5DA')
    # plt.bar(x, y, figure=fig)
    plt.bar(x,y)
    # fig = all_df['manuf'].value_counts().plot(kind='bar', ylabel="Number of Devices", xlabel="Manufacturer")
    return fig

# get flats manufacturer count percentage pie chart
def get_flats_manuf_count_piechart():
    fig, ax = plt.subplots(figsize = (9,10))
    fig.set_tight_layout(True)
    fig.patch.set_facecolor('#E8E5DA')
    
    fig = flats_all_df[~flats_all_df["manuf"].str.contains('Unknown', na=False)]['manuf'].value_counts().plot(kind='pie', legend=True, title="Device Manufacturers", labeldistance=None, ylabel="Frequency Distribution of Device Manufacturer") #autopct="%1.0f%%"
    
    fig.legend(loc='upper right', bbox_to_anchor=(-0.1, 1.),
            fontsize=8, title='Device Manufacturers')
    #plt.ylabel("Frequency Distribution of Device Manufacturer", size = 10)

    return fig

# get flats device type percentage pie chart
def get_flats_dev_type_piechart():
    fig, ax = plt.subplots(figsize = (7,6))
    fig.patch.set_facecolor('#E8E5DA')

    fig = flats_all_df[~flats_all_df["device_type"].str.contains('Unknown', na=False)]['device_type'].value_counts().plot(kind='pie', legend=True, title="Device Types", labeldistance=None) #autopct="%1.0f%%"
    fig.legend(loc='upper right', bbox_to_anchor=(1.2, 1.),
            fontsize=8, title='Device Types')

    plt.ylabel("Frequency Distribution of Device Type", size = 10)

    return fig