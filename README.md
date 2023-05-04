# NERVE-dashboard

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