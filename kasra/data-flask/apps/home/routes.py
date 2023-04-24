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

        if template == 'wlan.html':
             # Detect the current page
            segment = get_segment(request)

            # Serve the file (if exists) from app/templates/home/FILE.html
            return render_template("home/" + template, segment=segment, PageTitle = "WLAN Table",
                           table=[get_wlan_df().head().to_html(classes='data')], titles= get_wlan_df().columns.values)

        if template == 'bt_campus.html':
             # Detect the current page
            segment = get_segment(request)
            params = bt_params()

            # Serve the file (if exists) from app/templates/home/FILE.html
            return render_template("home/" + template, segment=segment, PageTitle = "Bluetooth Visuals",
                           params=params)       
               
        else:
            # Detect the current page
            segment = get_segment(request)

            # Serve the file (if exists) from app/templates/home/FILE.html
            return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
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
