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
from .forms import LaserForm, RFSoCConfigForm, CaylarForm, MercuryForm, ExperimentForm, LaserFormConfig, LaserFormIP, ExperimentFormNew, RFSoCFrequencySequenceForm0,RFSoCFrequencySequenceForm1
from staticfiles.XMLGenerator import xml_config_to_dict, dict_to_xml_file

from django.contrib import messages
from datetime import datetime
import subprocess

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

    FormsetChannel0 = formset_factory(RFSoCFrequencySequenceForm0, extra=0)
    FormsetChannel1 = formset_factory(RFSoCFrequencySequenceForm1, extra=0)

    if request.method == 'POST':
        form = RFSoCConfigForm(request.POST)
        Formset0 = FormsetChannel0(request.POST)
        Formset1 = FormsetChannel1(request.POST)
        if all([form.is_valid(),Formset0.is_valid(),Formset1.is_valid()]):
            time0 = []
            length0 = []
            frequency0 = []
            print(Formset0)
            print("----------------------------1")
            for form0 in Formset0:

                if form0.cleaned_data.get('time0')!=None:
                    time0.append(form0.cleaned_data.get('time0'))
                if form0.cleaned_data.get('length0')!=None:
                    length0.append(form0.cleaned_data.get('length0'))
                if form0.cleaned_data.get('frequency0')!=None:
                    freq0 = str(form0.cleaned_data.get('frequency0'))
                    print(form0.cleaned_data.get('frequency0'))
                    frequency0.append("freq"+freq0+"0")
            print(frequency0)
            rfsoc_config["EOM"]["time_seq0"] = time0
            rfsoc_config["EOM"]["freq_seq0"] = length0
            rfsoc_config["EOM"]["lengthseq0"] = frequency0
            time1 = []
            length1 = []
            frequency1 = []
            for form1 in Formset1:

                if form1.cleaned_data.get('time1')!=None:
                    time1.append(form1.cleaned_data.get('time1'))
                if form1.cleaned_data.get('length1')!=None:
                    length1.append(form1.cleaned_data.get('length1'))
                if form1.cleaned_data.get('frequency1')!=None:
                    freq1 = str(form0.cleaned_data.get('frequency1'))
                    print(form1.cleaned_data.get('frequency1'))
                    frequency1.append("freq"+freq1+"1")
            rfsoc_config["EOM"]["time_seq1"] = time1
            rfsoc_config["EOM"]["freq_seq1"] = length1
            rfsoc_config["EOM"]["lengthseq1"] = frequency1
            print(frequency1)
            print("----------------------------2")
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
            out_ch = [int(ch) for ch in request.POST.getlist('eom_outch[]')]
            rfsoc_config["EOM"]["out_ch"] = out_ch
            rfsoc_config["EOM"]["length0"] = form.cleaned_data['eom_length0']
            rfsoc_config["EOM"]["length1"] = form.cleaned_data['eom_length1']
            rfsoc_config["EOM"]["zone0"] = form.cleaned_data['eom_zone0']
            rfsoc_config["EOM"]["mode0"] = form.cleaned_data['eom_mode0']
            rfsoc_config["EOM"]["zone1"] = form.cleaned_data['eom_zone1']
            rfsoc_config["EOM"]["mode1"] = form.cleaned_data['eom_mode1']

            # Update Frequency A0 configuration
            rfsoc_config["EOM"]["freqA0"]["res_phase"] = form.cleaned_data['freqA0_res_phase']
            rfsoc_config["EOM"]["freqA0"]["pulse_gain"] = form.cleaned_data['freqA0_pulse_gain']
            rfsoc_config["EOM"]["freqA0"]["pulse_freq"] = form.cleaned_data['freqA0_pulse_freq']

            # Update Frequency B0 configuration
            rfsoc_config["EOM"]["freqB0"]["res_phase"] = form.cleaned_data['freqB0_res_phase']
            rfsoc_config["EOM"]["freqB0"]["pulse_gain"] = form.cleaned_data['freqB0_pulse_gain']
            rfsoc_config["EOM"]["freqB0"]["pulse_freq"] = form.cleaned_data['freqB0_pulse_freq']
            # Update Frequency A1 configuration
            rfsoc_config["EOM"]["freqA1"]["res_phase"] = form.cleaned_data['freqA1_res_phase']
            rfsoc_config["EOM"]["freqA1"]["pulse_gain"] = form.cleaned_data['freqA1_pulse_gain']
            rfsoc_config["EOM"]["freqA1"]["pulse_freq"] = form.cleaned_data['freqA1_pulse_freq']

            # Update Frequency B1 configuration
            rfsoc_config["EOM"]["freqB1"]["res_phase"] = form.cleaned_data['freqB1_res_phase']
            rfsoc_config["EOM"]["freqB1"]["pulse_gain"] = form.cleaned_data['freqB1_pulse_gain']
            rfsoc_config["EOM"]["freqB1"]["pulse_freq"] = form.cleaned_data['freqB1_pulse_freq']
            pins = [int(pin) for pin in request.POST.getlist('selected_pins[]')]
            rfsoc_config["AOM"]["pins"] = pins
            # Update AOM configuration
            lengths = []
            for i in range(4):
                length_value = form.cleaned_data.get('aom_length_' + str(i))
                if length_value!='[]' and i in pins:
                    length_list = [int(length_str.strip()) for length_str in length_value.split(',') if length_str.strip()]
                    lengths.append(length_list)
                else:
                    lengths.append([])
            rfsoc_config["AOM"]["length"] = lengths

            times = []
            for j in range(4):
                time_value = form.cleaned_data.get('aom_time_' + str(i))
                if time_value!='[]'and j in pins:
                    time_list = [int(time_str.strip()) for time_str in time_value.split(',') if time_str.strip()]
                    times.append(time_list)
                else:
                    times.append([])
            rfsoc_config["AOM"]["time"] = times


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
        Formset0 = FormsetChannel0()
        Formset1 = FormsetChannel1()
        print(rfsoc_config["EOM"]["time_seq0"])
        print(rfsoc_config["EOM"]["freq_seq0"])
        print(rfsoc_config["EOM"]["lengthseq0"])
        initial_data0 = [{'time0': t, 'frequency0': f[-2], 'length0': l} for t, f, l in zip(rfsoc_config["EOM"]["time_seq0"], rfsoc_config["EOM"]["freq_seq0"], rfsoc_config["EOM"]["lengthseq0"])]
        initial_data1 = [{'time1': t, 'frequency1': f[-2], 'length1': l} for t, f, l in zip(rfsoc_config["EOM"]["time_seq1"], rfsoc_config["EOM"]["freq_seq1"], rfsoc_config["EOM"]["lengthseq1"])]
        if len(initial_data0)!=0:
            Formset0 = FormsetChannel0(initial=initial_data0)
        else:
            FormsetChannel0 = formset_factory(RFSoCFrequencySequenceForm0)
            Formset0 = FormsetChannel0()
        if len(initial_data1)!=0:
            Formset1 = FormsetChannel1(initial=initial_data1)
        else:
            FormsetChannel1 = formset_factory(RFSoCFrequencySequenceForm1)
            Formset1 = FormsetChannel1()

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
            'eom_length0': rfsoc_config["EOM"]["length0"],
            'eom_length1': rfsoc_config["EOM"]["length1"],
            'eom_zone0': rfsoc_config["EOM"]["zone0"],
            'eom_mode0': rfsoc_config["EOM"]["mode0"],
            'eom_zone1': rfsoc_config["EOM"]["zone1"],
            'eom_mode1': rfsoc_config["EOM"]["mode1"],
            'freqA0_res_phase': rfsoc_config["EOM"]["freqA0"]["res_phase"],
            'freqA0_pulse_gain': rfsoc_config["EOM"]["freqA0"]["pulse_gain"],
            'freqA0_pulse_freq': rfsoc_config["EOM"]["freqA0"]["pulse_freq"],
            'freqB0_res_phase': rfsoc_config["EOM"]["freqB0"]["res_phase"],
            'freqB0_pulse_gain': rfsoc_config["EOM"]["freqB0"]["pulse_gain"],
            'freqB0_pulse_freq': rfsoc_config["EOM"]["freqB0"]["pulse_freq"],
            'freqA1_res_phase': rfsoc_config["EOM"]["freqA1"]["res_phase"],
            'freqA1_pulse_gain': rfsoc_config["EOM"]["freqA1"]["pulse_gain"],
            'freqA1_pulse_freq': rfsoc_config["EOM"]["freqA1"]["pulse_freq"],
            'freqB1_res_phase': rfsoc_config["EOM"]["freqB1"]["res_phase"],
            'freqB1_pulse_gain': rfsoc_config["EOM"]["freqB1"]["pulse_gain"],
            'freqB1_pulse_freq': rfsoc_config["EOM"]["freqB1"]["pulse_freq"],
            'aom_pins': rfsoc_config["AOM"]["pins"],
            'aom_time_0': ', '.join(str(val) for val in rfsoc_config["AOM"]["time"][0]),
            'aom_time_1': ', '.join(str(val) for val in rfsoc_config["AOM"]["time"][1]),
            'aom_time_2': ', '.join(str(val) for val in rfsoc_config["AOM"]["time"][2]),
            'aom_time_3': ', '.join(str(val) for val in rfsoc_config["AOM"]["time"][3]),
            'aom_length_0': ', '.join(str(val) for val in rfsoc_config["AOM"]["length"][0]),
            'aom_length_1': ', '.join(str(val) for val in rfsoc_config["AOM"]["length"][1]),
            'aom_length_2': ', '.join(str(val) for val in rfsoc_config["AOM"]["length"][2]),
            'aom_length_3': ', '.join(str(val) for val in rfsoc_config["AOM"]["length"][3]),
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

@require_POST
def start_experiments(request):
    # Get the experiment count
    experiment_count = int(request.POST.get("experimentCount", 0))
    print(experiment_count)
    # Process the experiment data
    for i in range(experiment_count):
        print(i)
        parameter_select = request.POST.get(f"parameter_select_{i}", "")
        print(parameter_select)
        # Process other form fields based on the selected parameter
        if parameter_select == "laser":
            laser_select = request.POST.get(f"laser_select_{i}", "")
            laser_input = request.POST.get(f"laser_input_{i}", "")
            # Process laser_select and laser_input values accordingly
            print(laser_select)
            print(laser_input)
        elif parameter_select == "rfsoc":
            rfsoc_select = request.POST.get(f"rfsoc_select_{i}", "")
            # Process rfsoc_select value accordingly
        elif parameter_select == "setting_eom_frequency":
            eom_ab_select = request.POST.get(f"eom_ab_select_{i}", "")
            phase_input = request.POST.get(f"phase_input_{i}", "")
            gain_input = request.POST.get(f"gain_input_{i}", "")
            frequency_input = request.POST.get(f"frequency_input_{i}", "")
            # Process eom_ab_select, phase_input, gain_input, and frequency_input values accordingly

    # Return a response indicating success
    return HttpResponse("Experiments started successfully.")


@login_required(login_url="/login/")
def index(request):
    if request.method == 'POST':
        form = ExperimentForm(request.POST)
        print(form)
        if form.is_valid():
            experiment_name = form.cleaned_data['experiment_name']
            description = form.cleaned_data['description']
            file_name = form.cleaned_data['file_name']
            print(form)

            # Perform further processing or save the data to the database
            # ...

    else:
        form = ExperimentForm()

    return render(request, 'home/index.html', {'form': form})

def get_device_parameters(device_index, cleaned_data):
    device_type = cleaned_data.get(f'form-{device_index}-device')
    parameters = {}

    if device_type == 'laser':
        parameters['wavelength'] = cleaned_data.get(f'form-{device_index}-wavelength')
        parameters['frequency'] = cleaned_data.get(f'form-{device_index}-frequency')
    elif device_type == 'rf_soc':
        eom_aom = cleaned_data.get(f'form-{device_index}-eom_aom')
        parameters['eom_aom'] = eom_aom

        if eom_aom == 'eom':
            parameters['eom_frequency'] = cleaned_data.get(f'form-{device_index}-eom_frequency')
            parameters['eom_time_start'] = cleaned_data.get(f'form-{device_index}-eom_time_start')
            parameters['eom_length'] = cleaned_data.get(f'form-{device_index}-eom_length')
        elif eom_aom == 'aom':
            parameters['aom_pins'] = cleaned_data.get(f'form-{device_index}-aom_pins')
            parameters['aom_start_time'] = cleaned_data.get(f'form-{device_index}-aom_start_time')
            parameters['aom_length'] = cleaned_data.get(f'form-{device_index}-aom_length')
    elif device_type == 'frequency_setting':
        parameters['frequency_name'] = cleaned_data.get(f'form-{device_index}-frequency_name')
        parameters['frequency'] = cleaned_data.get(f'form-{device_index}-frequency')
        parameters['amplitude'] = cleaned_data.get(f'form-{device_index}-amplitude')
        parameters['phase'] = cleaned_data.get(f'form-{device_index}-phase')

    return parameters
# @login_required(login_url="/login/")
# def index(request):
#     ExperimentFormSet = formset_factory(ParameterForm, formset=BaseExperimentForm)

#     if request.method == 'POST':
#         experiment_formset = ExperimentFormSet(request.POST, prefix='experiment')
#         experiment_form = ExperimentForm(request.POST)
#         print(experiment_form.is_valid())
#         print(experiment_formset.is_valid())
#         print(experiment_formset)
#         if experiment_form.is_valid() and experiment_formset.is_valid():
#             # Collect data from the experiment form
#             experiment_name = experiment_form.cleaned_data['experiment_name']
#             description = experiment_form.cleaned_data['description']

#             # Create a list to store the form data from each form in the formset
#             form_data_list = []

#             # Iterate over each form in the formset and collect the data
#             for form in experiment_formset:
#                 device = form.cleaned_data['device']
#                 laser_parameter = form.cleaned_data['laser_parameter']
#                 laser_frequency = form.cleaned_data['laser_frequency']
#                 laser_amplitude = form.cleaned_data['laser_amplitude']
#                 eom_aom = form.cleaned_data['eom_aom']
#                 eom_frequency = form.cleaned_data['eom_frequency']
#                 eom_time_start = form.cleaned_data['eom_time_start']
#                 eom_length = form.cleaned_data['eom_length']
#                 aom_pins = form.cleaned_data['aom_pins']
#                 aom_start_time = form.cleaned_data['aom_start_time']
#                 aom_length = form.cleaned_data['aom_length']
#                 frequency_name = form.cleaned_data['frequency_name']
#                 frequency_frequency = form.cleaned_data['frequency_frequency']
#                 frequency_phase = form.cleaned_data['frequency_phase']
#                 frequency_amplitude = form.cleaned_data['frequency_amplitude']
#                 print(device)
#                 # Create a dictionary to store the form data
#                 form_data = {
#                     'device': device,
#                     'laser_parameter': laser_parameter,
#                     'laser_frequency': laser_frequency,
#                     'laser_amplitude': laser_amplitude,
#                     'eom_aom': eom_aom,
#                     'eom_frequency': eom_frequency,
#                     'eom_time_start': eom_time_start,
#                     'eom_length': eom_length,
#                     'aom_pins': aom_pins,
#                     'aom_start_time': aom_start_time,
#                     'aom_length': aom_length,
#                     'frequency_name': frequency_name,
#                     'frequency_frequency': frequency_frequency,
#                     'frequency_phase': frequency_phase,
#                     'frequency_amplitude': frequency_amplitude
#                 }

#                 form_data_list.append(form_data)

#     else:
#         experiment_formset = ExperimentFormSet()
#         experiment_form = ExperimentForm()

#     context = {
#         'experiment_formset': experiment_formset,
#         'experiment_form': experiment_form
#     }
#     return render(request, 'home/index.html', context)


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
