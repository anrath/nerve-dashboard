# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from   flask_migrate import Migrate
from   flask_minify  import Minify
from   sys import exit

from apps.config import config_dict
from apps import create_app, db

from wlan_script import *

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

# WLAN CHARTS (still have to figure out if there is a way to get these all into another file)

# @app.route('/wlan_devicetype_dist.png')
# def plot_wlan_devicetype_dist():
#     fig = wlan_devicetype_dist()
#     output = io.BytesIO()
#     FigureCanvas(fig.figure).print_png(output)
#     return Response(output.getvalue(), mimetype='image/png')

# @app.route('/wlan_devicename_dist.png')
# def plot_wlan_devicename_dist():
#     fig = wlan_devicename_dist()
#     output = io.BytesIO()
#     FigureCanvas(fig.figure).print_png(output)
#     return Response(output.getvalue(), mimetype='image/png')

# @app.route('/wlan_manuf_dist.png')
# def plot_wlan_manuf_dist():
#     fig = wlan_manuf_dist()
#     output = io.BytesIO()
#     FigureCanvas(fig.figure).print_png(output)
#     return Response(output.getvalue(), mimetype='image/png')

# @app.route('/time_data_graph.png')
# def plot_time_data_graph():
#     fig = time_data_graph()
#     output = io.BytesIO()
#     FigureCanvas(fig.figure).print_png(output)
#     return Response(output.getvalue(), mimetype='image/png')

# @app.route('/time_pck_scatter.png')
# def plot_time_pck_scatter():
#     fig = time_pck_scatter()
#     output = io.BytesIO()
#     FigureCanvas(fig.figure).print_png(output)
#     return Response(output.getvalue(), mimetype='image/png')

# @app.route('/pck_hist.png')
# def plot_pck_hist():
#     fig = pck_hist()
#     output = io.BytesIO()
#     FigureCanvas(fig.figure).print_png(output)
#     return Response(output.getvalue(), mimetype='image/png')

#END WLAN CHARTS

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
