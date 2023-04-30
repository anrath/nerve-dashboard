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
import requests

#------------------------------------------------------------------------------------------------------------------
#FUNCTIONS: 

#
def getSummaryDf():
    all_df = pd.DataFrame(all)
    all_df = all_df[['kismet.device.base.key', 'kismet.device.base.name', 'kismet.device.base.type', 'kismet.device.base.packets.total', 'kismet.device.base.manuf', 'kismet.device.base.macaddr', 'kismet.device.base.channel', 'kismet.device.base.first_time', 'kismet.device.base.last_time', 'kismet.server.uuid']] # 'dot11.device'
    all_df.rename(columns={
        'kismet.device.base.key': 'key', 
        'kismet.device.base.name': 'device_name', 
        'kismet.device.base.type': 'device_type', 
        'kismet.device.base.packets.total': 'num_packets', 
        'kismet.device.base.manuf': 'manuf', 
        'kismet.device.base.macaddr': 'macaddr', 
        'kismet.device.base.channel': 'channel', 
        'kismet.device.base.first_time': 'first_seen', 
        'kismet.device.base.last_time': 'last_seen',
        'kismet.server.uuid': 'server_uuid',
        # 'dot11.device': 'network',
        }, inplace=True)

#get all df 
def get_all_df(df):
    return df

#get wlan df 
def get_summary_wlan_df(df):
    return df

#get blue df 
def get_blue_df(df):
    return df

#get aps df 
def get_aps_df(df):
    return df

# get graph of device counts
def get_dev_counts(all_df, wlan_df, blue_df, aps_df, path):
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
    plt.savefig(f'./apps/static/assets/images/summary/dev_count_{path}.svg')
    plt.close()
    # return fig

# get network data graph

# get manufacturer counts graph
def get_manuf_counts(all_df, path):
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
    plt.yscale('log')

    # fig = all_df['manuf'].value_counts().plot(kind='bar', ylabel="Number of Devices", xlabel="Manufacturer")

    plt.savefig(f'./apps/static/assets/images/summary/manuf_count_bar_{path}.svg')

    plt.close()
    # return fig

# get manufacturer count percentage pie chart
def get_manuf_count_piechart(all_df, path):
    # fig, ax = plt.subplots(figsize = (8,7))
    # fig.set_tight_layout(True)
    # fig.patch.set_facecolor('#E8E5DA')
    
    # fig = all_df[~all_df["manuf"].str.contains('Unknown', na=False)]['manuf'].value_counts().plot(kind='pie', legend=True, title="Device Manufacturers", labeldistance=None, ylabel="Frequency Distribution of Device Manufacturer") #autopct="%1.0f%%"
    
    # fig.legend(loc='upper right', bbox_to_anchor=(-0.1, 1.),
    #         fontsize=8, title='Device Manufacturers')
    fig, ax = plt.subplots(figsize = (6,4))
    fig.patch.set_facecolor('#E8E5DA')

    fig = all_df[~all_df["manuf"].str.contains('Unknown', na=False)]['manuf'].value_counts().plot(kind='pie', legend=True, title="Device Manufacturers", labeldistance=None) #autopct="%1.0f%%"
    # fig.legend(bbox_to_anchor=(1, 2.15), loc='upper left')
    fig.legend(bbox_to_anchor = (1.0, 1.0), loc='upper left', fontsize="5")
    # plt.tight_layout()

    plt.ylabel("Frequency Dist of Device Manufacturer", size = 10)
 
    plt.savefig(f'./apps/static/assets/images/summary/manuf_count_pie_{path}.svg')

    plt.close()
    # return fig

# get device type percentage pie chart
def get_dev_type_piechart(all_df, path):
    fig, ax = plt.subplots(figsize = (7,6))
    fig.patch.set_facecolor('#E8E5DA')

    fig = all_df[~all_df["device_type"].str.contains('Unknown', na=False)]['device_type'].value_counts().plot(kind='pie', legend=True, title="Device Types", labeldistance=None) #autopct="%1.0f%%"
    fig.legend(loc='upper right', bbox_to_anchor=(1.2, 1.),
            fontsize=8, title='Device Types')

    plt.ylabel("Frequency Distribution of Device Type", size = 10)

    plt.savefig(f'./apps/static/assets/images/summary/dev_type_pie_{path}.svg')

    plt.close()
    # return fig

#------------------------------------------------------------------------------------------------------------------

# Collecting data on all devices(

def net_exist(network):
    try:
        x = network['dot11.device.probed_ssid_map'][0]['dot11.probedssid.ssid']
    except KeyError:
        x = "None"
    return x



def create_summary_graphs(path):

    if path == 'realtime':
        user_password = "http://sniffer:sniffer@"
        server_ip = "172.26.99.45:2501/"

        # Retrieved from: 
        # endpoint = "/devices/views/all_views.json"
        all_VIEWID = "all"
        aps_VIEWID = "phydot11_accesspoints"
        bluetooth_VIEWID = "phy-Bluetooth"
        wlan_VIEWID = "phy-IEEE802.11"

        all_endpoint = f"/devices/views/{all_VIEWID}/devices.json"
        all_x = requests.get(user_password + server_ip + all_endpoint, headers={"KISMET": "E62F6C667B3CF269798AC58E0D811D85"})
        all = all_x.json()
        all_df = pd.DataFrame(all)
        all_df = all_df[['kismet.device.base.key', 'kismet.device.base.name', 'kismet.device.base.type', 'kismet.device.base.packets.total', 'kismet.device.base.manuf', 'kismet.device.base.macaddr', 'kismet.device.base.channel', 'kismet.device.base.first_time', 'kismet.device.base.last_time', 'kismet.server.uuid', 'dot11.device']] # 'dot11.device'
        all_df.rename(columns={
            'kismet.device.base.key': 'key', 
            'kismet.device.base.name': 'device_name', 
            'kismet.device.base.type': 'device_type', 
            'kismet.device.base.packets.total': 'num_packets', 
            'kismet.device.base.manuf': 'manuf', 
            'kismet.device.base.macaddr': 'macaddr', 
            'kismet.device.base.channel': 'channel', 
            'kismet.device.base.first_time': 'first_seen', 
            'kismet.device.base.last_time': 'last_seen',
            'kismet.server.uuid': 'server_uuid',
            'dot11.device': 'dot11_device',
            }, inplace=True)
        
        aps_endpoint = f"/devices/views/{aps_VIEWID}/devices.json"
        aps_x = requests.get(user_password + server_ip + aps_endpoint, headers={"KISMET": "E62F6C667B3CF269798AC58E0D811D85"})
        aps = aps_x.json()
        aps_df = pd.DataFrame(aps)
        aps_df = aps_df[['kismet.device.base.key', 'kismet.device.base.name', 'kismet.device.base.type', 'kismet.device.base.packets.total', 'kismet.device.base.manuf', 'kismet.device.base.macaddr', 'kismet.device.base.channel', 'kismet.device.base.first_time', 'kismet.device.base.last_time', 'kismet.server.uuid']]
        aps_df.rename(columns={
            'kismet.device.base.key': 'key', 
            'kismet.device.base.name': 'device_name', 
            'kismet.device.base.type': 'device_type', 
            'kismet.device.base.packets.total': 'num_packets', 
            'kismet.device.base.manuf': 'manuf', 
            'kismet.device.base.macaddr': 'macaddr', 
            'kismet.device.base.channel': 'channel', 
            'kismet.device.base.first_time': 'first_seen', 
            'kismet.device.base.last_time': 'last_seen',
            'kismet.server.uuid': 'server_uuid',
            }, inplace=True)
        
        bt_endpoint = f"/devices/views/{bluetooth_VIEWID}/devices.json"
        bt_x = requests.get(user_password + server_ip + bt_endpoint, headers={"KISMET": "E62F6C667B3CF269798AC58E0D811D85"})
        bt = bt_x.json()
        bt_df = pd.DataFrame(bt)
        bt_df = bt_df[['kismet.device.base.key', 'kismet.device.base.name', 'kismet.device.base.type', 'kismet.device.base.packets.total', 'kismet.device.base.manuf', 'kismet.device.base.macaddr', 'kismet.device.base.channel', 'kismet.device.base.first_time', 'kismet.device.base.last_time', 'kismet.server.uuid']]
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
            'kismet.server.uuid': 'server_uuid',
            }, inplace=True)
        
        wlan_endpoint = f"/devices/views/{wlan_VIEWID}/devices.json"
        wlan_x = requests.get(user_password + server_ip + wlan_endpoint, headers={"KISMET": "E62F6C667B3CF269798AC58E0D811D85"})
        wlan = wlan_x.json()
        wlan_df = pd.DataFrame(wlan)
        wlan_df = wlan_df[['kismet.device.base.key', 'kismet.device.base.name', 'kismet.device.base.type', 'kismet.device.base.packets.total', 'kismet.device.base.manuf', 'kismet.device.base.macaddr', 'kismet.device.base.channel', 'kismet.device.base.first_time', 'kismet.device.base.last_time', 'kismet.server.uuid']] # 'dot11.device'
        wlan_df.rename(columns={
            'kismet.device.base.key': 'key', 
            'kismet.device.base.name': 'device_name', 
            'kismet.device.base.type': 'device_type', 
            'kismet.device.base.packets.total': 'num_packets', 
            'kismet.device.base.manuf': 'manuf', 
            'kismet.device.base.macaddr': 'macaddr', 
            'kismet.device.base.channel': 'channel', 
            'kismet.device.base.first_time': 'first_seen', 
            'kismet.device.base.last_time': 'last_seen',
            'kismet.server.uuid': 'server_uuid',
            # 'dot11.device': 'network',
            }, inplace=True)
    else:
        all_df = pd.read_json(f'{DATA_PATH}/{path}/all.json', orient='records')
        all_df = all_df[['kismet.device.base.key', 'kismet.device.base.name', 'kismet.device.base.type', 'kismet.device.base.packets.total', 'kismet.device.base.manuf', 'kismet.device.base.macaddr', 'kismet.device.base.channel', 'kismet.device.base.first_time', 'kismet.device.base.last_time', 'kismet.server.uuid', 'dot11.device']] #'dot11.device'
        all_df.rename(columns={
            'kismet.device.base.key': 'key', 
            'kismet.device.base.name': 'device_name', 
            'kismet.device.base.type': 'device_type', 
            'kismet.device.base.packets.total': 'num_packets', 
            'kismet.device.base.manuf': 'manuf', 
            'kismet.device.base.macaddr': 'macaddr', 
            'kismet.device.base.channel': 'channel', 
            'kismet.device.base.first_time': 'first_seen', 
            'kismet.device.base.last_time': 'last_seen',
            'kismet.server.uuid': 'server_uuid',
            'dot11.device': 'dot11_device',
            }, inplace=True)

        aps_df = pd.read_json(f'{DATA_PATH}/{path}/phydot11_accesspoints.json', orient='records')
        aps_df = aps_df[['kismet.device.base.key', 'kismet.device.base.name', 'kismet.device.base.type', 'kismet.device.base.packets.total', 'kismet.device.base.manuf', 'kismet.device.base.macaddr', 'kismet.device.base.channel', 'kismet.device.base.first_time', 'kismet.device.base.last_time', 'kismet.server.uuid']]
        aps_df.rename(columns={
            'kismet.device.base.key': 'key', 
            'kismet.device.base.name': 'device_name', 
            'kismet.device.base.type': 'device_type', 
            'kismet.device.base.packets.total': 'num_packets', 
            'kismet.device.base.manuf': 'manuf', 
            'kismet.device.base.macaddr': 'macaddr', 
            'kismet.device.base.channel': 'channel', 
            'kismet.device.base.first_time': 'first_seen', 
            'kismet.device.base.last_time': 'last_seen',
            'kismet.server.uuid': 'server_uuid',
            }, inplace=True)

        bt_df = pd.read_json(f'{DATA_PATH}/{path}/phy-Bluetooth.json', orient='records')
        bt_df = bt_df[['kismet.device.base.key', 'kismet.device.base.name', 'kismet.device.base.type', 'kismet.device.base.packets.total', 'kismet.device.base.manuf', 'kismet.device.base.macaddr', 'kismet.device.base.channel', 'kismet.device.base.first_time', 'kismet.device.base.last_time', 'kismet.server.uuid']]
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
            'kismet.server.uuid': 'server_uuid',
            }, inplace=True)
        
        wlan_df = pd.read_json(f'{DATA_PATH}/{path}/phy-IEEE802.11.json', orient='records')
        wlan_df = wlan_df[['kismet.device.base.key', 'kismet.device.base.name', 'kismet.device.base.type', 'kismet.device.base.packets.total', 'kismet.device.base.manuf', 'kismet.device.base.macaddr', 'kismet.device.base.channel', 'kismet.device.base.first_time', 'kismet.device.base.last_time', 'kismet.server.uuid']] #'dot11.device'
        wlan_df.rename(columns={
            'kismet.device.base.key': 'key', 
            'kismet.device.base.name': 'device_name', 
            'kismet.device.base.type': 'device_type', 
            'kismet.device.base.packets.total': 'num_packets', 
            'kismet.device.base.manuf': 'manuf', 
            'kismet.device.base.macaddr': 'macaddr', 
            'kismet.device.base.channel': 'channel', 
            'kismet.device.base.first_time': 'first_seen', 
            'kismet.device.base.last_time': 'last_seen',
            'kismet.server.uuid': 'server_uuid',
            # 'dot11.device': 'network',
            }, inplace=True)

    get_dev_counts(all_df, wlan_df, bt_df, aps_df, path)
    get_manuf_counts(all_df, path)
    get_manuf_count_piechart(all_df, path)
    get_dev_type_piechart(all_df, path)
   
    all_df_ap = all_df.copy()
    all_df_ap = all_df_ap[all_df_ap['device_type'] == 'Wi-Fi AP']
    all_df_client = all_df.copy()
    all_df_client = all_df_client[all_df_client['device_type'] == 'Wi-Fi Client']
    all_df_client['ap_macaddr'] = all_df_client.apply(lambda row: row['dot11_device']['dot11.device.last_bssid'], axis=1)

    def get_probed_ssid(x):
        try:
            probed_ssid_map = x['dot11.device.probed_ssid_map']
        except:
            return None
        
        probed_ssids = []
        for val in probed_ssid_map:
            probed_ssids.append(val['dot11.probedssid.ssid'])

        return probed_ssids

    def get_advertised_ssid(x):
        try:
            advertised_ssid = x['dot11.device.advertised_ssid_map'][0]['dot11.advertisedssid.ssid']
        except:
            return None

        return advertised_ssid
    with pd.option_context("mode.chained_assignment", None):
        all_df_client['probed_ssids'] = all_df_client.apply(lambda row: get_probed_ssid(row['dot11_device']), axis=1)
        all_df_client['probed_ssids_len'] = all_df_client.apply(lambda row: len(row['probed_ssids']) if row['probed_ssids']!=None else 0, axis=1)
        all_df_ap['advertised_ssid'] = all_df_ap.apply(lambda row: get_advertised_ssid(row['dot11_device']), axis=1)

    all_df = pd.merge(all_df_client, all_df_ap[['macaddr', 'advertised_ssid']], left_on='ap_macaddr', right_on='macaddr', how='left')
    del all_df['macaddr_y']
    del all_df['dot11_device']
    all_df.rename(columns={'macaddr_x': 'macaddr', 'advertised_ssid': 'connected_ssid'}, inplace=True)
    all_df.sort_values(by=['probed_ssids_len'], ascending=False)

    return all_df

#----------------------------------------------------------------------------------------------------------------------------------------
# GATHERING DATA
DATA_PATH = './data'
# DATA_SUB_PATH = ['campus', 'flats']
# IMG_PATH = './apps/static/assets/images/bt'
# Opening JSON files / Data imports