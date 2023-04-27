# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from   flask        import redirect, Response
from   flask_migrate import Migrate
from   flask_minify  import Minify
from flask import request

from   sys import exit

from apps.config import config_dict
from apps import create_app, db

from wlan_script import *
from bt_script import *
from summary_script import *
from network_graph import *
from forms import SearchForm

# WARNING: Don't run with debug turned on in production!
DEBUG = (os.getenv('DEBUG', 'False') == 'True')

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:
    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app(app_config)

#------------------------------------------------------------------------------------------------------------------

# WLAN
create_wlan_graphs("campus")
create_wlan_graphs("flats")

# Bluetooth
create_bt_graphs("campus")
create_bt_graphs("flats")

# Summary
create_summary_graphs("campus")
create_summary_graphs("flats")
# Network
for sub_path in DATA_SUB_PATH:
    if (not os.path.isfile(f"{HTML_PATH}/ssid_{sub_path}.html")):
        create_ssid_graph(sub_path)

# REFRESH Realtime Data
@app.route('/wlanrefresh')
def wlanrefresh():
    create_wlan_graphs('realtime')
    return redirect("/wlan_realtime.html")

@app.route('/btrefresh')
def btrefresh():
    create_bt_graphs('realtime')
    return redirect("/bt_realtime.html")

@app.route('/sumrefresh')
def sumrefresh():
    create_summary_graphs('realtime')
    return redirect("/summary_realtime.html")

#END REFRESH Realtime Data


# @app.route('/search', methods=['GET', 'POST'])
# def search():
#     form = SearchForm()
#     # if request.method == 'POST' and form.validate_on_submit():
#         # return redirect((url_for('search_results', query=form.search.data)))  # or what you want
#     return render_template('query.html', form=form)
@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm(request.form) 
    message = "origmessage"
    if request.method == 'POST':
        alldf = create_summary_graphs('campus')
        search=request.form['search']
        print(str(search))
        print(alldf['macaddr'].tolist()[0:10])

        #check if macaddr in df
        if str(search) in alldf['macaddr'].tolist():
            row = alldf.loc[alldf['macaddr'] == str(search)]
            rowStr = row.to_string()
            # rowlist = row.astype(str).values.flatten().tolist()
            message = rowStr
            #message='testmessage'
            print(message)



        #empty form field after processing
        form.search.data = ""

    #     return redirect('/query.html', form=form)
    # elif request.method == 'GET':
    #     return redirect('/query.html', form=form)
    
    return render_template("home/" + 'query.html', form=form, message=message)


#------------------------------------------------------------------------------------------------------------------



Migrate(app, db)

if not DEBUG:
    Minify(app=app, html=True, js=False, cssless=False)
    
if DEBUG:
    app.logger.info('DEBUG            = ' + str(DEBUG)             )
    app.logger.info('Page Compression = ' + 'FALSE' if DEBUG else 'TRUE' )
    app.logger.info('DBMS             = ' + app_config.SQLALCHEMY_DATABASE_URI)
    app.logger.info('ASSETS_ROOT      = ' + app_config.ASSETS_ROOT )

if __name__ == "__main__":
    app.run()
