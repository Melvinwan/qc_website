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
from .construct_object import construct_object, construct_connect_caylar,construct_connect_itc,construct_connect_rfsoc,construct_connect_toptica

from .forms import LaserForm, RFSoCConfigForm, CaylarForm, MercuryForm
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
            toptica_host["wavelength_act"] = form.cleaned_data['wavelength_act']
            toptica_host["scan_end"] = form.cleaned_data['scan_end']
            toptica_host["scan_start"] = form.cleaned_data['scan_start']
            toptica_host["scan_freq"] = form.cleaned_data['scan_freq']
            toptica_host["scan_offset"] = form.cleaned_data['scan_offset']
            dict_to_xml_file(toptica_host, "staticfiles/toptica.xml")
            Update_Laser = construct_connect_toptica()
            Update_Laser.update_all_xml("staticfiles/toptica.xml")
            # Add success message to the Django messages framework
            messages.success(request, 'Changes saved successfully!')

            # Redirect to the laser page to reload the page with the updated values
            return redirect('laser_page')

    else:
        # Initialize the form with the current laser information
        form = LaserForm(initial={
            'laser_host': toptica_host["host"] if toptica_host["host"] is not None else '',
            'laser_port': toptica_host["port"] if toptica_host["port"] is not None else '',
            'wavelength_act': toptica_host["wavelength_act"] if toptica_host["wavelength_act"] is not None else '',
            'scan_end': toptica_host["scan_end"] if toptica_host["scan_end"] is not None else '',
            'scan_start': toptica_host["scan_start"] if toptica_host["scan_start"] is not None else '',
            'scan_freq': toptica_host["scan_freq"] if toptica_host["scan_freq"] is not None else '',
            'scan_offset': toptica_host["scan_offset"] if toptica_host["scan_offset"] is not None else '',
        })

    # Assign the variables with the initial values
    laser_host = toptica_host["host"] if toptica_host["host"] is not None else ''
    laser_port = toptica_host["port"] if toptica_host["port"] is not None else ''
    wavelength_act = toptica_host["wavelength_act"] if toptica_host["wavelength_act"] is not None else ''
    scan_end = toptica_host["scan_end"] if toptica_host["scan_end"] is not None else ''
    scan_start = toptica_host["scan_start"] if toptica_host["scan_start"] is not None else ''
    scan_freq = toptica_host["scan_freq"] if toptica_host["scan_freq"] is not None else ''
    scan_offset = toptica_host["scan_offset"] if toptica_host["scan_offset"] is not None else ''

    return render(request, 'home/laser.html', {
        'form': form,
        'laser_host': laser_host,
        'laser_port': laser_port,
        'wavelength_act': wavelength_act,
        'scan_end': scan_end,
        'scan_start': scan_start,
        'scan_freq': scan_freq,
        'scan_offset': scan_offset,
    })


# views.py
def caylar_page_view(request):
    # Load the data from the magnet XML file
    caylar_host = xml_config_to_dict("staticfiles/caylar.xml")

    if request.method == 'POST':
        form = CaylarForm(request.POST)
        if form.is_valid():
            caylar_host["host"] = form.cleaned_data['caylar_host']
            caylar_host["port"] = form.cleaned_data['caylar_port']
            caylar_host["current"] = form.cleaned_data['caylar_current']
            caylar_host["field"] = form.cleaned_data['caylar_field']
            dict_to_xml_file(caylar_host, "staticfiles/caylar.xml")

            # Add success message to the Django messages framework
            messages.success(request, 'Changes saved successfully!')

            # Redirect to the magnet page to reload the page with the updated values
            return redirect('caylar_page')

    else:
        # Initialize the form with the current magnet information
        form = CaylarForm(initial={
            'caylar_host': caylar_host["host"] if caylar_host["host"] is not None else '',
            'caylar_port': caylar_host["port"] if caylar_host["port"] is not None else '',
            'caylar_current': caylar_host["current"] if caylar_host["current"] is not None else '',
            'caylar_field': caylar_host["field"] if caylar_host["field"] is not None else '',
        })

    # Assign the variables with the initial values
    magnet_host = caylar_host["host"] if caylar_host["host"] is not None else ''
    magnet_port = caylar_host["port"] if caylar_host["port"] is not None else ''
    magnet_current = caylar_host["current"] if caylar_host["current"] is not None else ''
    magnet_field = caylar_host["field"] if caylar_host["field"] is not None else ''

    return render(request, 'home/caylar.html', {
        'form': form,
        'magnet_host': magnet_host,
        'magnet_port': magnet_port,
        'magnet_current': magnet_current,
        'magnet_field': magnet_field,
    })


def rfsoc_page_view(request):
    # Load the data from the rfsoc XML file
    xilinx_host = xml_config_to_dict("staticfiles/xilinx_host.xml")
    rfsoc_config = xml_config_to_dict("staticfiles/xilinx.xml")
    if request.method == 'POST':
        form = RFSoCConfigForm(request.POST)
        if form.is_valid():
            # Update RFSoC host and port
            xilinx_host["host"] = form.cleaned_data['rfsoc_host']
            xilinx_host["username"] = form.cleaned_data['rfsoc_username']
            xilinx_host["password"] = form.cleaned_data['rfsoc_password']
            xilinx_host["port"] = form.cleaned_data['rfsoc_port']
            dict_to_xml_file(xilinx_host, "staticfiles/xilinx_host.xml")

            # Update General configuration
            rfsoc_config["adc_trig_offset"] = form.cleaned_data['adc_trig_offset']
            rfsoc_config["soft_avgs"] = form.cleaned_data['soft_avgs']
            rfsoc_config["relax_delay"] = form.cleaned_data['relax_delay']
            rfsoc_config["readout_length"] = form.cleaned_data['readout_length']
            rfsoc_config["pulse_freq"] = form.cleaned_data['pulse_freq']
            rfsoc_config["reps"] = form.cleaned_data['reps']

            # Update EOM configuration
            rfsoc_config["EOM"]["out_ch"] = form.cleaned_data['eom_outch']
            rfsoc_config["EOM"]["freq_seq"] = form.cleaned_data['eom_freqseq']
            rfsoc_config["EOM"]["time_seq"] = form.cleaned_data['eom_timeseq']
            rfsoc_config["EOM"]["length"] = form.cleaned_data['eom_length']
            rfsoc_config["EOM"]["pulse_freq"] = form.cleaned_data['eom_pulsefreq']
            rfsoc_config["EOM"]["zone"] = form.cleaned_data['eom_zone']
            rfsoc_config["EOM"]["mode"] = form.cleaned_data['eom_mode']

            # Update Frequency A configuration
            rfsoc_config["EOM"]["freqA"]["res_phase"] = form.cleaned_data['freqA_res_phase']
            rfsoc_config["EOM"]["freqA"]["pulse_gain"] = form.cleaned_data['freqA_pulse_gain']
            rfsoc_config["EOM"]["freqA"]["pulse_freq"] = form.cleaned_data['freqA_pulse_freq']

            # Update Frequency B configuration
            rfsoc_config["EOM"]["freqB"]["res_phase"] = form.cleaned_data['freqB_res_phase']
            rfsoc_config["EOM"]["freqB"]["pulse_gain"] = form.cleaned_data['freqB_pulse_gain']
            rfsoc_config["EOM"]["freqB"]["pulse_freq"] = form.cleaned_data['freqB_pulse_freq']

            # Update AOM configuration
            rfsoc_config["AOM"]["length"] = form.cleaned_data['aom_length']
            rfsoc_config["AOM"]["pins"] = form.cleaned_data['aom_pins']
            rfsoc_config["AOM"]["time"] = form.cleaned_data['aom_time']

            # Update the rfsoc.xml file
            dict_to_xml_file(rfsoc_config, "staticfiles/rfsoc.xml")

            # Add success message to the Django messages framework
            messages.success(request, 'Changes saved successfully!')

            # Redirect to the rfsoc page to reload the page with the updated values
            return redirect('rfsoc_page')

    else:
        # Initialize the form with the current rfsoc information

        form = RFSoCConfigForm(initial={
            'rfsoc_host': xilinx_host["host"],
            'rfsoc_port': xilinx_host["port"],
            'rfsoc_username': xilinx_host["username"],
            'rfsoc_password': xilinx_host["password"],
            'adc_trig_offset': rfsoc_config["adc_trig_offset"],
            'soft_avgs': rfsoc_config["soft_avgs"],
            'relax_delay': rfsoc_config["relax_delay"],
            'readout_length': rfsoc_config["readout_length"],
            'pulse_freq': rfsoc_config["pulse_freq"],
            'reps': rfsoc_config["reps"],
            'eom_outch': rfsoc_config["EOM"]["out_ch"],
            'eom_freqseq': rfsoc_config["EOM"]["freq_seq"],
            'eom_timeseq': rfsoc_config["EOM"]["time_seq"],
            'eom_length': rfsoc_config["EOM"]["length"],
            'eom_pulsefreq': rfsoc_config["EOM"]["pulse_freq"],
            'eom_zone': rfsoc_config["EOM"]["zone"],
            'eom_mode': rfsoc_config["EOM"]["mode"],
            'freqA_res_phase': rfsoc_config["EOM"]["freqA"]["res_phase"],
            'freqA_pulse_gain': rfsoc_config["EOM"]["freqA"]["pulse_gain"],
            'freqA_pulse_freq': rfsoc_config["EOM"]["freqA"]["pulse_freq"],
            'freqB_res_phase': rfsoc_config["EOM"]["freqB"]["res_phase"],
            'freqB_pulse_gain': rfsoc_config["EOM"]["freqB"]["pulse_gain"],
            'freqB_pulse_freq': rfsoc_config["EOM"]["freqB"]["pulse_freq"],
            'aom_length': rfsoc_config["AOM"]["length"],
            'aom_pins': rfsoc_config["AOM"]["pins"],
            'aom_time': rfsoc_config["AOM"]["time"],
        })

    return render(request, 'home/rfsoc.html', {
        'form': form,
    })


def mercury_page_view(request):
    # Load the data from the cryostat XML file
    mercury_host = xml_config_to_dict("staticfiles/mercuryITC.xml")

    if isinstance(mercury_host, str):
        mercury_host = {}

    if request.method == 'POST':
        form = MercuryForm(request.POST)
        if form.is_valid():
            mercury_host["host"] = form.cleaned_data['mercury_host']
            mercury_host["port"] = form.cleaned_data['mercury_port']
            mercury_host["heater_power"] = form.cleaned_data['mercury_heater_power']
            mercury_host["ITC_temperature"] = form.cleaned_data['mercury_itc_temperature']
            dict_to_xml_file(mercury_host, "staticfiles/mercuryITC.xml")

            # Add success message to the Django messages framework
            messages.success(request, 'Changes saved successfully!')

            # Redirect to the cryostat page to reload the page with the updated values
            return redirect('mercury_page')

    else:
        # Initialize the form with the current cryostat information
        form = MercuryForm(initial={
            'mercury_host': mercury_host.get("host", ""),
            'mercury_port': mercury_host.get("port", ""),
            'mercury_heater_power': mercury_host.get("heater_power", ""),
            'mercury_itc_temperature': mercury_host.get("ITC_temperature", ""),
        })

    # Assign the variables with the initial values
    cryostat_host = mercury_host.get("host", "")
    cryostat_port = mercury_host.get("port", "")

    return render(request, 'home/mercury.html', {
        'form': form,
        'mercury_host': cryostat_host,
        'mercury_port': cryostat_port,
        'mercury_heater_power': mercury_host.get("heater_power", ""),
        'mercury_itc_temperature': mercury_host.get("ITC_temperature", ""),
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
