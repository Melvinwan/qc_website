# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect
from .construct_object import construct_object

from .forms import LaserForm, RFSoCForm, CaylarForm, MercuryForm
from staticfiles.XMLGenerator import xml_config_to_dict, dict_to_xml_file

from django.contrib import messages

def laser_page_view(request):
    # Load the data from the laser XML file
    toptica_host = xml_config_to_dict("staticfiles/toptica.xml")

    if request.method == 'POST':
        form = LaserForm(request.POST)
        if form.is_valid():
            toptica_host["host"] = form.cleaned_data['laser_host']
            toptica_host["port"] = form.cleaned_data['laser_port']
            dict_to_xml_file(toptica_host, "staticfiles/toptica.xml")

            # Add success message to the Django messages framework
            messages.success(request, 'Changes saved successfully!')

            # Redirect to the laser page to reload the page with the updated values
            return redirect('laser_page')

    else:
        # Initialize the form with the current laser information
        form = LaserForm(initial={
            'laser_host': toptica_host["host"] if toptica_host["host"] is not None else '',
            'laser_port': toptica_host["port"] if toptica_host["port"] is not None else '',
        })

    # Assign the variables with the initial values
    laser_host = toptica_host["host"] if toptica_host["host"] is not None else ''
    laser_port = toptica_host["port"] if toptica_host["port"] is not None else ''

    return render(request, 'home/laser.html', {
        'form': form,
        'laser_host': laser_host,
        'laser_port': laser_port,
    })

def caylar_page_view(request):
    # Load the data from the magnet XML file
    caylar_host = xml_config_to_dict("staticfiles/caylar.xml")

    if request.method == 'POST':
        form = LaserForm(request.POST)
        if form.is_valid():
            caylar_host["host"] = form.cleaned_data['magnet_host']
            caylar_host["port"] = form.cleaned_data['magnet_port']
            dict_to_xml_file(caylar_host, "staticfiles/caylar.xml")

            # Add success message to the Django messages framework
            messages.success(request, 'Changes saved successfully!')

            # Redirect to the magnet page to reload the page with the updated values
            return redirect('caylar_page')

    else:
        # Initialize the form with the current magnet information
        form = CaylarForm(initial={
            'magnet_host': caylar_host["host"] if caylar_host["host"] is not None else '',
            'magnet_port': caylar_host["port"] if caylar_host["port"] is not None else '',
        })

    # Assign the variables with the initial values
    magnet_host = caylar_host["host"] if caylar_host["host"] is not None else ''
    magnet_port = caylar_host["port"] if caylar_host["port"] is not None else ''

    return render(request, 'home/caylar.html', {
        'form': form,
        'magnet_host': magnet_host,
        'magnet_port': magnet_port,
    })

def rfsoc_page_view(request):
    # Load the data from the rfsoc XML file
    xilinx_host = xml_config_to_dict("staticfiles/xilinx_host.xml")

    if request.method == 'POST':
        form = LaserForm(request.POST)
        if form.is_valid():
            xilinx_host["host"] = form.cleaned_data['rfsoc_host']
            xilinx_host["port"] = form.cleaned_data['rfsoc_port']
            dict_to_xml_file(xilinx_host, "staticfiles/xilinx_host.xml")

            # Add success message to the Django messages framework
            messages.success(request, 'Changes saved successfully!')

            # Redirect to the rfsoc page to reload the page with the updated values
            return redirect('rfsoc_page')

    else:
        # Initialize the form with the current rfsoc information
        form = RFSoCForm(initial={
            'rfsoc_host': xilinx_host["host"] if xilinx_host["host"] is not None else '',
            'rfsoc_port': xilinx_host["port"] if xilinx_host["port"] is not None else '',
        })

    # Assign the variables with the initial values
    rfsoc_host = xilinx_host["host"] if xilinx_host["host"] is not None else ''
    rfsoc_port = xilinx_host["port"] if xilinx_host["port"] is not None else ''

    return render(request, 'home/rfsoc.html', {
        'form': form,
        'rfsoc_host': rfsoc_host,
        'rfsoc_port': rfsoc_port,
    })

def mercury_page_view(request):
    # Load the data from the cryostat XML file
    mercury_host = xml_config_to_dict("staticfiles/mercuryITC.xml")

    if request.method == 'POST':
        form = MercuryForm(request.POST)
        if form.is_valid():
            mercury_host["host"] = form.cleaned_data['cryostat_host']
            mercury_host["port"] = form.cleaned_data['cryostat_port']
            dict_to_xml_file(mercury_host, "staticfiles/mercuryITC.xml")

            # Add success message to the Django messages framework
            messages.success(request, 'Changes saved successfully!')

            # Redirect to the cryostat page to reload the page with the updated values
            return redirect('mercury_page')

    else:
        # Initialize the form with the current cryostat information
        form = LaserForm(initial={
            'cryostat_host': mercury_host["host"] if mercury_host["host"] is not None else '',
            'cryostat_port': mercury_host["port"] if mercury_host["port"] is not None else '',
        })

    # Assign the variables with the initial values
    cryostat_host = mercury_host["host"] if mercury_host["host"] is not None else ''
    cryostat_port = mercury_host["port"] if mercury_host["port"] is not None else ''

    return render(request, 'home/mercury.html', {
        'form': form,
        'cryostat_host': cryostat_host,
        'cryostat_port': cryostat_port,
    })

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    RFSoC, Laser, Caylar, mercuryITC = construct_object()
    html_template = loader.get_template('home/index.html')
    if RFSoC.try_connect():
        rfsoc_status = "ON"
    else:
        rfsoc_status = "OFF"

    if Laser.try_connect():
        laser_status = "ON"
    else:
        laser_status = "OFF"

    if mercuryITC.try_connect():
        mercury_status = "ON"
    else:
        mercury_status = "OFF"

    if Caylar.try_connect():
        caylar_status = "ON"
    else:
        caylar_status = "OFF"

    return render(request, 'home/index.html', {'rfsoc_status':rfsoc_status, 'laser_status':laser_status,'caylar_status':caylar_status,'mercury_status':mercury_status})
    # return HttpResponse(html_template.render(context, request, {'rfsoc_status':"ON"}))
def status(request):
    RFSoC, Laser, Caylar, mercuryITC = construct_object()

    if RFSoC.try_connect():
        rfsoc_status = "ON"
    else:
        rfsoc_status = "OFF"

    if Laser.try_connect():
        laser_status = "ON"
    else:
        laser_status = "OFF"

    if mercuryITC.try_connect():
        mercury_status = "ON"
    else:
        mercury_status = "OFF"

    if Caylar.try_connect():
        caylar_status = "ON"
    else:
        caylar_status = "OFF"

    status = {
        'rfsoc_status': rfsoc_status,
        'laser_status': laser_status,
        'mercury_status': mercury_status,
        'caylar_status': caylar_status,
    }

    return JsonResponse(status)

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
