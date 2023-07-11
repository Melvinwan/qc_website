# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect
from .construct_object import construct_object, construct_caylar,construct_itc,construct_rfsoc,construct_toptica
from django.forms.formsets import formset_factory
from .forms import LaserForm, RFSoCConfigForm, CaylarForm, MercuryForm, ExperimentForm, LaserFormConfig, LaserFormIP, RFSoCEOMSequenceForm, RFSoCAOMSequenceForm
from staticfiles.XMLGenerator import xml_config_to_dict, dict_to_xml_file

from django.contrib import messages
from datetime import datetime
import subprocess
import os
# def restart_server(request):
#     # Stop the current runserver process
#     subprocess.call(["pkill", "-f", "runserver"])

#     # Start a new runserver process
#     subprocess.Popen(["python", "manage.py", "runserver"])

#     # Redirect to a new URL or template
#     return redirect('home')  # Replace 'home' with the appropriate URL pattern name or URL path
def laser_page_view(request):
    # Load the data from the laser XML file

    Update_Laser = construct_toptica()
    connected = Update_Laser.try_connect()
    toptica_host = xml_config_to_dict("staticfiles/toptica.xml")
    context = {}
    if connected:
        Update_Laser.update_all_xml("staticfiles/toptica.xml")
        context["wavelength_act"] = Update_Laser.report_ctl_wavelength_act()
        context["scan_end"] =  Update_Laser.report_scan_end()
        context["scan_start"] =  Update_Laser.report_scan_start()
        context["scan_freq"] =  Update_Laser.report_scan_frequency()
        context["scan_offset"] =  Update_Laser.report_scan_offset()
        toptica_host["time_update"] =  datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        dict_to_xml_file(toptica_host, "staticfiles/toptica.xml")
        toptica_host = xml_config_to_dict("staticfiles/toptica.xml")
    else:
        info = "Last time connected "+toptica_host["time_update"]+" because not connected with the device!"
        # info = "Parameter has not updated since "+toptica_host["time_update"]+" because not connected with the device!"
        messages.info(request, info)

    if request.method == 'POST':
        if "updateall" in request.POST:
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
                if connected:
                    Update_Laser.try_connect()
                    Update_Laser.update_all_xml("staticfiles/toptica.xml")
                    Update_Laser.disconnect()
                    messages.success(request, 'Changes saved successfully in Toptica!')
                else:
                    # Add success message to the Django messages framework
                    messages.success(request, 'Changes saved successfully in XML!')

                # Redirect to the laser page to reload the page with the updated values
                return redirect('laser_page')
            else:
                messages.warning(request, 'Cannot be updated!')
                return redirect('laser_page')
        elif "updateip" in request.POST:
            form = LaserFormIP(request.POST)
            if form.is_valid():

                toptica_host["host"] = form.cleaned_data['laser_host']
                toptica_host["port"] = form.cleaned_data['laser_port']
                dict_to_xml_file(toptica_host, "staticfiles/toptica.xml")
                # Add success message to the Django messages framework
                messages.success(request, 'Changes saved successfully in XML!')
                # Redirect to the laser page to reload the page with the updated values
                return redirect('laser_page')
            else:
                messages.warning(request, 'Cannot be updated!')
                return redirect('laser_page')
        elif "updateconfig" in request.POST:
            form = LaserFormConfig(request.POST)
            if form.is_valid():
                toptica_host["wavelength_act"] = form.cleaned_data['wavelength_act']
                toptica_host["scan_end"] = form.cleaned_data['scan_end']
                toptica_host["scan_start"] = form.cleaned_data['scan_start']
                toptica_host["scan_freq"] = form.cleaned_data['scan_freq']
                toptica_host["scan_offset"] = form.cleaned_data['scan_offset']
                dict_to_xml_file(toptica_host, "staticfiles/toptica.xml")
                if connected:
                    Update_Laser.try_connect()
                    Update_Laser.update_all_xml("staticfiles/toptica.xml")
                    Update_Laser.disconnect()
                    messages.success(request, 'Changes saved successfully in Toptica!')
                else:
                    # Add success message to the Django messages framework
                    messages.success(request, 'Changes saved successfully in XML!')

                # Redirect to the laser page to reload the page with the updated values
                return redirect('laser_page')
            else:
                messages.warning(request, 'Cannot be updated!')
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

    context["connected"] = connected
    context["form"] = form
    Update_Laser.disconnect()

    return render(request, 'home/laser.html', context)


# views.py
def caylar_page_view(request):
    # Load the data from the magnet XML file
    Update_caylar = construct_caylar()
    connected = Update_caylar.try_connect()
    caylar_host = xml_config_to_dict("staticfiles/caylar.xml")
    if connected:
        Update_caylar.update_all_xml("staticfiles/caylar.xml")
        caylar_host["current"] = Update_caylar.current()
        caylar_host["field"] =  Update_caylar.field()
        caylar_host["time_update"] =  datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        dict_to_xml_file(caylar_host, "staticfiles/caylar.xml")
        caylar_host = xml_config_to_dict("staticfiles/caylar.xml")
    else:
        info = "Parameter has not updated since "+caylar_host["time_update"]+" because not connected with the device!"
        messages.info(request, info)

    if request.method == 'POST':
        form = CaylarForm(request.POST)
        if form.is_valid():
            caylar_host["host"] = form.cleaned_data['caylar_host']
            caylar_host["port"] = form.cleaned_data['caylar_port']
            caylar_host["current"] = form.cleaned_data['caylar_current']
            caylar_host["field"] = form.cleaned_data['caylar_field']
            dict_to_xml_file(caylar_host, "staticfiles/caylar.xml")

            if connected:
                Update_caylar.update_all_xml("staticfiles/caylar.xml")
                messages.success(request, 'Changes saved successfully in Caylar!')
            else:
                # Add success message to the Django messages framework
                messages.success(request, 'Changes saved successfully in XML!')

            # Redirect to the magnet page to reload the page with the updated values
            return redirect('caylar_page')
        else:
            messages.warning(request, 'Cannot be updated!')
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
    Update_rfsoc = construct_rfsoc()
    connected = False
    # connected = Update_rfsoc.try_connect()

    xilinx_host = xml_config_to_dict("staticfiles/xilinx_host.xml")
    #IF FILE IS NOT FOUND MAYBE CAN BUILD ONE
    rfsoc_config = xml_config_to_dict("staticfiles/xilinx.xml")
    if connected:
        Update_rfsoc.build_config(rfsoc_config)
        Update_rfsoc.get_config()
        rfsoc_config = xml_config_to_dict("staticfiles/xilinx.xml")
        xilinx_host["time_update"] =  datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        dict_to_xml_file(xilinx_host, "staticfiles/xilinx_host.xml")
    else:
        info = "Parameter has not updated since "+xilinx_host["time_update"]+" because not connected with the device!"
        messages.info(request, info)

    FormsetChannel = formset_factory(RFSoCEOMSequenceForm, extra=0)
    FormsetAOM = formset_factory(RFSoCAOMSequenceForm, extra=0)

    if request.method == 'POST':
        form = RFSoCConfigForm(request.POST)
        Formset0 = FormsetChannel(request.POST,prefix='formset0')
        Formset1 = FormsetAOM(request.POST,prefix='formset1')

        if all([form.is_valid(),Formset0.is_valid(),Formset1.is_valid()]):
            channel0=[]
            frequency0=[]
            phase0=[]
            gain0=[]
            time0 = []
            length0 = []
            for form0 in Formset0:
                if form0.cleaned_data.get('channel0')!=None:
                    channel0.append([int(x) for x in form0.cleaned_data.get('channel0')])
                if form0.cleaned_data.get('time0')!=None:
                    time0.append(form0.cleaned_data.get('time0'))
                if form0.cleaned_data.get('length0')!=None:
                    length0.append(form0.cleaned_data.get('length0'))
                if form0.cleaned_data.get('frequency0')!=None:
                    frequency0.append(form0.cleaned_data.get('frequency0'))
                if form0.cleaned_data.get('phase0')!=None:
                    phase0.append(form0.cleaned_data.get('phase0'))
                if form0.cleaned_data.get('gain0')!=None:
                    gain0.append(form0.cleaned_data.get('gain0'))
            rfsoc_config["EOM"]["channel_seq0"] = channel0
            rfsoc_config["EOM"]["freq_seq0"] = frequency0
            rfsoc_config["EOM"]["phase_seq0"] = phase0
            rfsoc_config["EOM"]["gain_seq0"] = gain0
            rfsoc_config["EOM"]["time_seq0"] = time0
            rfsoc_config["EOM"]["lengthseq0"] = length0
            time1 = []
            length1 = []
            pins1 = []
            for form1 in Formset1:

                if form1.cleaned_data.get('time1')!=None:
                    time1.append(form1.cleaned_data.get('time1'))
                if form1.cleaned_data.get('length1')!=None:
                    length1.append(form1.cleaned_data.get('length1'))
                if form1.cleaned_data.get('aom_pins')!=None:
                    pins1.append([int(x) for x in form1.cleaned_data.get('aom_pins')])
            rfsoc_config["AOM"]["time_seq1"] = time1
            rfsoc_config["AOM"]["pins_seq1"] = pins1
            rfsoc_config["AOM"]["lengthseq1"] = length1
            # Update RFSoC host and port
            xilinx_host["host"] = form.cleaned_data['rfsoc_host']
            xilinx_host["username"] = form.cleaned_data['rfsoc_username']
            xilinx_host["password"] = form.cleaned_data['rfsoc_password']
            xilinx_host["port"] = form.cleaned_data['rfsoc_port'] if form.cleaned_data['rfsoc_port'] is not None else ''
            xilinx_host["time_update"] =  datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            dict_to_xml_file(xilinx_host, "staticfiles/xilinx_host.xml")

            # Update General configuration
            rfsoc_config["adc_trig_offset"] = form.cleaned_data['adc_trig_offset']
            rfsoc_config["soft_avgs"] = form.cleaned_data['soft_avgs']
            rfsoc_config["relax_delay"] = form.cleaned_data['relax_delay']
            rfsoc_config["readout_length"] = form.cleaned_data['readout_length']
            rfsoc_config["pulse_freq"] = form.cleaned_data['pulse_freq']
            rfsoc_config["reps"] = form.cleaned_data['reps']

            # Update EOM configuration
            rfsoc_config["EOM"]["length0"] = form.cleaned_data['eom_length0']
            rfsoc_config["EOM"]["length1"] = form.cleaned_data['eom_length1']
            rfsoc_config["EOM"]["zone0"] = form.cleaned_data['eom_zone0']
            rfsoc_config["EOM"]["mode0"] = form.cleaned_data['eom_mode0']
            rfsoc_config["EOM"]["zone1"] = form.cleaned_data['eom_zone1']
            rfsoc_config["EOM"]["mode1"] = form.cleaned_data['eom_mode1']

            # Update the rfsoc.xml file
            dict_to_xml_file(rfsoc_config, "staticfiles/xilinx.xml")

            if connected:
                Update_rfsoc.build_config(rfsoc_config)
                messages.success(request, 'Changes saved successfully in RFSoC!')
            else:
                # Add success message to the Django messages framework
                messages.success(request, 'Changes saved successfully in XML!')
            # Add success message to the Django messages framework
            messages.success(request, 'Changes saved successfully!')

            # Redirect to the rfsoc page to reload the page with the updated values
            return redirect('rfsoc_page')
        else:
            messages.warning(request, 'Cannot be updated!')
            return redirect('rfsoc_page')
    else:
        form = RFSoCConfigForm()
        initial_data0 = [{'time0': t, 'channel0': ''.join(map(str,c)), 'length0': l, 'frequency0':f,'phase0':p,'gain0':g} for t, c, l,f,p,g in zip(rfsoc_config["EOM"]["time_seq0"], rfsoc_config["EOM"]["channel_seq0"], rfsoc_config["EOM"]["lengthseq0"], rfsoc_config["EOM"]["freq_seq0"], rfsoc_config["EOM"]["phase_seq0"], rfsoc_config["EOM"]["gain_seq0"])]
        initial_data1 = [{'time1': t, 'aom_pins': p, 'length1': l} for t, p, l in zip(rfsoc_config["AOM"]["time_seq1"], rfsoc_config["AOM"]["pins_seq1"], rfsoc_config["AOM"]["lengthseq1"])]
        if len(initial_data0)!=0:
            Formset0 = FormsetChannel(initial=initial_data0,prefix='formset0')
        else:
            FormsetChannel = formset_factory(RFSoCEOMSequenceForm)
            Formset0 = FormsetChannel(prefix='formset0')
        if len(initial_data1)!=0:
            Formset1 = FormsetAOM(initial=initial_data1,prefix='formset1')
        else:
            FormsetAOM = formset_factory(RFSoCAOMSequenceForm)
            Formset1 = FormsetAOM(prefix='formset1')

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
            'eom_length0': rfsoc_config["EOM"]["length0"],
            'eom_length1': rfsoc_config["EOM"]["length1"],
            'eom_zone0': rfsoc_config["EOM"]["zone0"],
            'eom_mode0': rfsoc_config["EOM"]["mode0"],
            'eom_zone1': rfsoc_config["EOM"]["zone1"],
            'eom_mode1': rfsoc_config["EOM"]["mode1"],
        })
    context = {
        "form": form,
        "formset0": Formset0,
        "formset1": Formset1
    }
    return render(request, 'home/rfsoc.html', context)


def mercury_page_view(request):
    # Load the data from the cryostat XML file
    Update_mercury = construct_itc()
    connected = Update_mercury.try_connect()
    mercury_host = xml_config_to_dict("staticfiles/mercuryITC.xml")
    if connected:
        Update_mercury.update_all_xml("staticfiles/mercuryITC.xml")
        mercury_host["current"] = Update_mercury.current()
        mercury_host["field"] =  Update_mercury.field()
        mercury_host["time_update"] =  datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        dict_to_xml_file(mercury_host, "staticfiles/mercuryITC.xml")
        mercury_host = xml_config_to_dict("staticfiles/mercuryITC.xml")
    else:
        info = "Parameter has not updated since "+mercury_host["time_update"]+" because not connected with the device!"
        messages.info(request, info)
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

            if connected:
                Update_mercury.update_all_xml("staticfiles/mercuryITC.xml")
                messages.success(request, 'Changes saved successfully in MercuryITC!')
            else:
                # Add success message to the Django messages framework
                messages.success(request, 'Changes saved successfully in XML!')

            # Redirect to the cryostat page to reload the page with the updated values
            return redirect('mercury_page')
        else:
            messages.warning(request, 'Cannot be updated!')
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

GRFSoC = None
GLaser = None
GCaylar = None
GmercuryITC = None
def start_experiment(request):
    global GRFSoC
    global GLaser
    global GCaylar
    global GmercuryITC
    choosed_device = request.POST.getlist('selected_devices[]')
    choosed_device.append("RFSoC")
    off_device = ["Laser", "RFSoC", "Mercury", "Caylar"]
    on_device = []
    RFSoC, Laser, Caylar, mercuryITC = construct_object()
    rfsoc_status = "OFF"
    if RFSoC.try_connect():
        rfsoc_status = "ON"
        on_device.append(RFSoC)
        off_device.remove("RFSoC")
    laser_status = "OFF"
    if Laser.try_connect():
        laser_status = "ON"
        on_device.append(Laser)
        off_device.remove("Laser")
    mercury_status = "OFF"
    if mercuryITC.try_connect():
        mercury_status = "ON"
        on_device.append(mercuryITC)
        off_device.remove("Mercury")
    caylar_status = "OFF"
    if Caylar.try_connect():
        caylar_status = "ON"
        on_device.append(Caylar)
        off_device.remove("Caylar")
    GRFSoC = RFSoC
    GLaser = Laser
    GCaylar = Caylar
    GmercuryITC = mercuryITC

    common_off_devices = set(off_device).intersection(choosed_device)
    if common_off_devices:
        off_device_names = ", ".join(common_off_devices)
        message = f"Experiment cannot be started because {off_device_names} are offline."
        for i in on_device:
            i.disconnect()
        return JsonResponse({'message': message}, status=400)

    # All devices are online, continue with starting the experiment
    # Your logic for starting the experiment here
    try:
        os.makedirs(request.POST['file_name'], exist_ok = True)
        print("Directory '%s' created successfully" % request.POST['file_name'])
        # Create and write the information.txt file
        file_path = os.path.join(request.POST['file_name'], 'information.txt')
        with open(file_path, 'w') as file:
            file.write(f"Experiment Name: {request.POST['experiment_name']}\n")
            file.write(f"Description: {request.POST['description']}\n")
    except OSError as error:
        print("Directory '%s' can not be created" % request.POST['file_name'])
        message = ("Directory '%s' can not be created" % request.POST['file_name'])
        return JsonResponse({'message': message}, status=400)
    message = 'Experiment started successfully.'
    return JsonResponse({'message': message})
def stop_experiment(request):
    global GRFSoC
    global GLaser
    global GCaylar
    global GmercuryITC
    GRFSoC.disconnect()
    GLaser.disconnect()
    GCaylar.disconnect()
    GmercuryITC.disconnect()
    GRFSoC = None
    GLaser = None
    GCaylar = None
    GmercuryITC = None
    message = 'Experiment stopped successfully.'
    return JsonResponse({'message': message})
import json
import csv
from datetime import datetime
def append_to_csv(file_path, data,column_headers):
    file_exists = os.path.isfile(file_path)
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(column_headers)
        writer.writerow(data)
def get_live_data_and_run_rfsoc(request):
    global GRFSoC
    global GLaser
    global GCaylar
    global GmercuryITC
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    laser_scan_end = GLaser.report_scan_end()
    laser_scan_start = GLaser.report_scan_start()
    laser_scan_offset = GLaser.report_scan_offset()
    laser_scan_frequency = GLaser.report_scan_frequency()
    laser_wavelength = GLaser.report_ctl_wavelength_act()
    caylar_current = GCaylar.current()
    caylar_field = GCaylar.field()
    caylar_ADCDAC_temp = GCaylar.ADCDAC_temp()
    caylar_box_temp = GCaylar.box_temp()
    caylar_rack_temp = GCaylar.rack_temp()
    caylar_water_temp = GCaylar.water_temp()
    caylar_water_flow = GCaylar.water_flow()
    itc_heater_power = GmercuryITC.report_heater_power()
    itc_temperature = GmercuryITC.report_temperature()
    # Create a list with the data
    itc_data_row = [timestamp,itc_heater_power,itc_temperature]
    itc_column_headers = ['timestamp', 'Heater Power','temperature']
    caylar_column_headers = ['timestamp', 'current', 'field', 'ADCDAC temp', 'box temp', 'rack temp', 'water temp', 'water flow']
    caylar_data_row = [timestamp,caylar_current,caylar_field,caylar_ADCDAC_temp,caylar_box_temp,caylar_rack_temp,caylar_water_temp,caylar_water_flow]
    laser_column_headers = ['timestamp', 'scan start', 'scan end', 'scan offset', 'scan frequency', 'wavelength']
    laser_data_row = [timestamp, laser_scan_start, laser_scan_end, laser_scan_offset, laser_scan_frequency, laser_wavelength]
    # Append the data to the CSV file
    laser_csv_file_path = 'laser.csv'
    caylar_csv_file_path = 'caylar.csv'
    itc_csv_file_path = 'itc.csv'
    append_to_csv(laser_csv_file_path, laser_data_row,laser_column_headers)
    append_to_csv(caylar_csv_file_path, caylar_data_row,caylar_column_headers)
    append_to_csv(itc_csv_file_path, itc_data_row,itc_column_headers)
    data = {'laser_scan_end': laser_scan_end,
            'laser_scan_start': laser_scan_start,
            'laser_scan_offset': laser_scan_offset,
            'laser_scan_frequency': laser_scan_frequency,
            'laser_wavelength': laser_wavelength,
            'caylar_current': caylar_current,
            'caylar_field': caylar_field,
            'caylar_ADCDAC_temp': caylar_ADCDAC_temp,
            'caylar_box_temp': caylar_box_temp,
            'caylar_rack_temp': caylar_rack_temp,
            'caylar_water_temp': caylar_water_temp,
            'caylar_water_flow': caylar_water_flow,
            'itc_heater_power': itc_heater_power,
            'itc_temperature': itc_temperature}
    return JsonResponse(data)


@login_required(login_url="/login/")
def index(request):
    # if request.method == 'POST':
    #     form = ExperimentForm(request.POST)
    #     print(form)
    #     if form.is_valid():
    #         experiment_name = form.cleaned_data.get('experiment_name')
    #         description = form.cleaned_data['description']
    #         file_name = form.cleaned_data['file_name']

    #         # Perform further processing or save the data to the database
    #         # ...
    #     else:
    #         messages.warning(request, 'Cannot be updated!')
    #         return render(request, 'home/index.html', {'form': form, 'run':False})
    # else:
    form = ExperimentForm()

    return render(request, 'home/index.html', {'form': form, 'run':True})
def status(request):
    RFSoC, Laser, Caylar, mercuryITC = construct_object()

    if RFSoC.try_connect():
        rfsoc_status = "ON"
    else:
        rfsoc_status = "OFF"

    if Laser.try_connect():
        laser_status = "ON"
        Laser.disconnect()
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
