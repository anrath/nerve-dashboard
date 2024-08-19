# NERVE-dashboard
When a hacker performs malicious actions, such as broadcasting a rogue SSID, on a wide-scale network, it may not always be obvious. However, suppose WLAN traffic data is able to be collected at multiple locations of that network’s reach. In that case, patterns can be observed over time, potentially leading to capturing various bad actors. We use a Raspberry Pi and Kismet, an open source network sniffing tool, to collect network data for our experiments.

## Setup
- If working in a virtual env: `pip install -r requirements.txt`
- Unzip the datasets

## Datasets
- `./archive/campus_small.zip` -- Brown College run for ~3 hours
- `./archive/api_campus_large.zip` -- Brown College run for ~2 days 
- `./archive/api_flats.zip` -- Flats run for ~15 hours

## Website
- `./nerve/` includes a templated Flask website. Execute `python run.py` to start the dashboard.
- `./nerve/templates/home` -- includes the pages for `wlan.html` and `bluetooth.html`. `index.html` will include our summary statistics and a link to the network graph
