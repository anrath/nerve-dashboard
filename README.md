# kismet-api-dashboard

## Setup
- If working in a virtual env: `pip install -r requirements.txt`
- Download the dataset or use the smaller version for testing code

## Datasets
- `./api/` -- Brown College run for ~3 hours
- `.api_campus_large.zip` -- Brown College run for ~2 days 
- `.api_flats.zip` -- Flats run for ~15 hours

## Website
- `./kasra/data-flask/` includes a templated Flask website
- `./kasra/data-flask/templates/home` -- includes the pages for `wlan.html` and `bluetooth.html`. `index.html` will include our summary statistics and a link to the network graph