# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound

from wlan_script import *
from bt_script import *
from network_graph import *

@blueprint.route('/index')
@login_required
def index():

    return render_template('home/index.html', segment='index')


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'


        if 'wlan' in template and 'realtime' not in template:
             # Detect the current page
            segment = get_segment(request)
            params = wlan_params(template[5:-5])

            # Serve the file (if exists) from app/templates/home/FILE.html
            return render_template("home/" + template, segment=segment, PageTitle = "WLAN Visuals",
                           params=params) 

        if 'wlan' in template and 'realtime' in template:
             # Detect the current page
            segment = get_segment(request)
            create_wlan_graphs(template[5:-5])
            params = wlan_params(template[5:-5])

            # Serve the file (if exists) from app/templates/home/FILE.html
            return render_template("home/" + template, segment=segment, PageTitle = "WLAN Visuals",
                           params=params)

        if 'bt' in template and 'realtime' not in template:
             # Detect the current page
            segment = get_segment(request)
            params = bt_params(template[3:-5])

            # Serve the file (if exists) from app/templates/home/FILE.html
            return render_template("home/" + template, segment=segment, PageTitle = "Bluetooth Visuals",
                           params=params)       

        if 'bt' in template and 'realtime' in template:
             # Detect the current page
            segment = get_segment(request)
            create_bt_graphs(template[3:-5])
            params = bt_params(template[3:-5])

            # Serve the file (if exists) from app/templates/home/FILE.html
            return render_template("home/" + template, segment=segment, PageTitle = "Bluetooth Visuals",
                           params=params)

        if template == 'ssid_realtime.html':
             # Detect the current page
            create_ssid_graph('realtime')
            segment = get_segment(request)
            # Serve the file (if exists) from app/templates/home/FILE.html
            return render_template("home/" + template, segment=segment)
           
        else:
            # Detect the current page
            segment = get_segment(request)

            # Serve the file (if exists) from app/templates/home/FILE.html
            return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except Exception as e:
        print("\n\n\n\n working:")
        print(e)
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
