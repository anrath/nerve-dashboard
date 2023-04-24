from pyvis.network import Network
import pandas as pd
import json
import os
import requests

def create_ssid_graph(sub_path):

    if sub_path == 'realtime':
        user_password = "http://sniffer:sniffer@"
        server_ip = "172.26.99.45:2501/"

        ap_endpoint = "/devices/views/phydot11_accesspoints/devices.json"
        ap_response = requests.get(user_password + server_ip + ap_endpoint, headers={"KISMET": "E62F6C667B3CF269798AC58E0D811D85"})
        ap_json = json.dumps(ap_response.json(), indent=4)

        wlan_endpoint = "/devices/views/phy-IEEE802.11/devices.json"
        wlan_response = requests.get(user_password + server_ip + wlan_endpoint, headers={"KISMET": "E62F6C667B3CF269798AC58E0D811D85"})
        wlan_json = json.dumps(wlan_response.json(), indent=4)

        ssid_endpoint = "/phy/phy80211/ssids/views/ssids.json"
        ssid_response = requests.get(user_password + server_ip + ssid_endpoint, headers={"KISMET": "E62F6C667B3CF269798AC58E0D811D85"})
        ssid_json = json.dumps(ssid_response.json(), indent=4)

        with open(f'{DATA_PATH}/realtime/phydot11_accesspoints.json', "w") as outfile:
            outfile.write(ap_json)

        with open(f'{DATA_PATH}/realtime/phy-IEEE802.11.json', "w") as outfile:
            outfile.write(wlan_json)
            
        with open(f'{DATA_PATH}/realtime/phy_phy80211_ssids_views_ssids.json', "w") as outfile:
            outfile.write(ssid_json)


    # Opening JSON files
    with open(f'{DATA_PATH}/{sub_path}/phydot11_accesspoints.json', 'r') as openfile:
        aps = json.load(openfile)

    with open(f'{DATA_PATH}/{sub_path}/phy_phy80211_ssids_views_ssids.json', 'r') as openfile:
        ssids = json.load(openfile)

    with open(f'{DATA_PATH}/{sub_path}/phy-IEEE802.11.json', 'r') as openfile:
        wlan = json.load(openfile)

    aps_df = pd.DataFrame()

    for ap in aps:
        try:
            ssid = ap['dot11.device']['dot11.device.responded_ssid_map'][0]['dot11.advertisedssid.ssid']
        except:
            try:
                ssid = ap['dot11.device']['dot11.device.advertised_ssid_map'][0]['dot11.advertisedssid.ssid']
            except:
                try:
                    ssid = ap['dot11.device']['dot11.device.probed_ssid_map'][0]['dot11.probedssid.ssid']
                except:
                    ssid = 'eduroam'
        ap_data = {
            "key": [ap['kismet.device.base.key']], 
            "manuf": [ap['kismet.device.base.manuf']], 
            "macaddr": [ap['kismet.device.base.macaddr']],
            "ssid": [ssid]
        }
        
        aps_df = pd.concat([aps_df, pd.DataFrame(ap_data)], ignore_index=True)

    # Attempt to fill in missing SSIDs
    for ssid in ssids:
        set1 = set(aps_df[aps_df['ssid']=='']['key'].values)
        list2 = ssid['dot11.ssidgroup.responding_devices']
        common = list(set1.intersection(list2))
        for val in common:
            ind = aps_df[aps_df['key']==val].index[0]
            # print(ind)
            aps_df.at[ind, 'ssid'] = ssid['dot11.ssidgroup.ssid']

    # Remove empty SSIDs
    aps_df = aps_df[aps_df['ssid']!='']

    wlan_df = pd.DataFrame()

    for device in wlan:

        wlan_data = {
            "ap": [device['dot11.device']['dot11.device.last_bssid']],
            "key": [device['kismet.device.base.key']], 
            "manuf": [device['kismet.device.base.manuf']], 
            "macaddr": [device['kismet.device.base.macaddr']],
            # "ssid": [ssid],
        }
        
        wlan_data = pd.DataFrame(wlan_data)

        wlan_df = pd.concat([wlan_df, wlan_data], ignore_index=True)
    wlan_df['ap_bool'] = False

    # Attempt to fill in missing APs
    for ap in aps:
        set1 = set(wlan_df[wlan_df['ap']=='00:00:00:00:00:00']['macaddr'].values)
        try:
            list2 = ap['dot11.device']['dot11.device.associated_client_map']
        except:
            continue
        common = list(set1.intersection(list2))
        for val in common:
            ind = wlan_df[wlan_df['macaddr']==val].index[0]
            # print(ind)
            wlan_df.at[ind, 'ap'] = ap['kismet.device.base.macaddr']

    # Driver Code
    ssids_df = pd.DataFrame()
    ssids_num = pd.DataFrame()
    columns = ['ssid', 'macaddr', 'manuf', 'ap_bool']

    for ssid in ssids:
        # ssid device numbers
        ssid_data = {
            "ssid": [ssid['dot11.ssidgroup.ssid']], 
            "num_probing": [ssid['dot11.ssidgroup.probing_devices_len']], 
            "num_responding": [ssid['dot11.ssidgroup.responding_devices_len']]
        }
        
        ssids_num = pd.concat([ssids_num, pd.DataFrame(ssid_data)], ignore_index=True)

        temp_res = pd.DataFrame(columns=columns)
        if (len(ssid['dot11.ssidgroup.responding_devices']) != 0):
            # responding devices devices nodes/edges
            temp_res = pd.DataFrame(ssid['dot11.ssidgroup.responding_devices'])
            temp_res['ssid'] = ssid['dot11.ssidgroup.ssid']
            temp_res.rename(columns={0: 'devices'}, inplace=True)
            temp_res = temp_res[['ssid', 'devices']]
            temp_res['ap_bool'] = True
            # Updating device keys with mac addresses
            temp_res = pd.merge(temp_res, aps_df.loc[:, ~aps_df.columns.isin(['ssid'])], left_on='devices', right_on='key', how='inner')
            temp_res = temp_res[columns]
        
        temp_prob = pd.DataFrame(columns=columns)
        if (len(ssid['dot11.ssidgroup.probing_devices']) != 0 and ssid['dot11.ssidgroup.ssid']!='eduroam'):
            # probing devices nodes/edges
            temp_prob = pd.DataFrame(ssid['dot11.ssidgroup.probing_devices'])
            temp_prob['ssid'] = ssid['dot11.ssidgroup.ssid']
            temp_prob.rename(columns={0: 'devices'}, inplace=True)
            temp_prob = temp_prob[['ssid', 'devices']]
            # Updating device keys with mac addresses
            temp_prob = pd.merge(temp_prob, wlan_df, left_on='devices', right_on='key', how='inner')
            temp_prob = temp_prob[columns]

        # concat all
        ssids_df = pd.concat([ssids_df, temp_res, temp_prob], ignore_index=True)

    # ssids_df = pd.concat([ssids_df, wlan_df], ignore_index=True)

    # Remove Aruba Networks HP devices
    wlan_df = wlan_df[wlan_df['manuf']!='Aruba Networks HP']
    # Remove empty devices with empty APs
    wlan_df = wlan_df[wlan_df['ap']!='00:00:00:00:00:00']

    wlan_df_sample = wlan_df.sample(n=min(len(wlan_df),1000))

    # Graph Setup
    net = Network(
        # notebook=True,
        # cdn_resources="remote",
        height="1080px", 
        width="100%", 
        bgcolor="#222222", 
        font_color="white",
        # select_menu=True,
        # filter_menu=True,
    )

    # Physics
    net.force_atlas_2based()

    images = {'Intel Corporation':'https://raw.githubusercontent.com/anrath/data/master/intel_logo.jpg', 
            'Apple':'https://raw.githubusercontent.com/anrath/data/master/apple_gray_logo.png', 
            'Aruba Networks HP':'https://raw.githubusercontent.com/anrath/data/master/aruba_logo.jpg'
            }

    # SSID-AP Edges

    sources = ssids_df['ssid']
    targets = ssids_df['macaddr']
    manuf = ssids_df['manuf']
    ap_bool = ssids_df['ap_bool']

    edge_data = zip(sources, targets, manuf, ap_bool)

    for e in edge_data:
        src = e[0]
        dst = e[1]
        manuf = e[2]
        ap_bool = e[3]

        net.add_node(src, src, title=src, group=1, shape='diamond')

        device_group = 2 if ap_bool else 3

        if (manuf in images.keys()):
            net.add_node(dst, dst, title=dst, group=device_group, shape='circularImage', image=images[manuf], brokenImage='circle')
        else:
            net.add_node(dst, dst, title=dst, group=device_group, shape='circularImage', image='https://raw.githubusercontent.com/anrath/data/master/blank.png', brokenImage='circle')
        net.add_edge(src, dst)

    # AP-Device Edges
    aps = wlan_df_sample['ap']
    devices = wlan_df_sample['macaddr']
    manuf = wlan_df_sample['manuf']
    # ap_bool = wlan_df['ap_bool']

    edge_data = zip(aps, devices, manuf)

    for e in edge_data:
        src = e[0]
        dst = e[1]
        manuf = e[2]

        # net.add_node(src, src, title=src, group=2, shape='diamond')
        net.add_node(src, src, title=src, group=2, shape='circularImage', image=images['Aruba Networks HP'], brokenImage='circle')

        device_group = 3

        if (manuf in images.keys()):
            net.add_node(dst, dst, title=dst, group=device_group, shape='circularImage', image=images[manuf], brokenImage='circle')
        else:
            net.add_node(dst, dst, title=dst, group=device_group, shape='circularImage', image='https://raw.githubusercontent.com/anrath/data/master/blank.png', brokenImage='circle')
        net.add_edge(src, dst)

    # Hover Text
    neighbor_map = net.get_adj_list()

    # add neighbor data to node hover data
    for node in net.nodes:
        node["title"] += " Neighbors:\n" + "\n".join(neighbor_map[node["id"]])
        node["value"] = len(neighbor_map[node["id"]])

    net.write_html(name=f"{HTML_PATH}/ssid_{sub_path}.html", notebook=False, local=True)


DATA_PATH = './data'
DATA_SUB_PATH = ['campus', 'flats']
HTML_PATH = './apps/templates/home'

ssid_dict = {}

for sub_path in DATA_SUB_PATH:
    if (not os.path.isfile(f"{HTML_PATH}/ssid_{sub_path}.html")):
        create_ssid_graph(sub_path)

# create_ssid_graph('realtime')