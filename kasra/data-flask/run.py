# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from   flask        import redirect, Response
from   flask_migrate import Migrate
from   flask_minify  import Minify
from   sys import exit

from apps.config import config_dict
from apps import create_app, db

from wlan_script import *
from bt_script import *
from summary_script import *
from network_graph import *

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
