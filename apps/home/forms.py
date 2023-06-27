# forms.py
from django import forms

class LaserForm(forms.Form):
    laser_host = forms.CharField(label='IP Address', max_length=100)
    laser_port = forms.IntegerField(label='Port', required=False)
    wavelength_act = forms.FloatField(label='Wavelength')
    scan_end = forms.FloatField(label='Scan End')
    scan_start = forms.FloatField(label='Scan Start')
    scan_freq = forms.FloatField(label='Scan Frequency')
    scan_offset = forms.FloatField(label='Scan Offset')


# forms.py
class CaylarForm(forms.Form):
    caylar_host = forms.CharField(label='IP Address', max_length=100)
    caylar_port = forms.IntegerField(label='Port', required=False)
    caylar_current = forms.FloatField(label='Current', required=False)
    caylar_field = forms.FloatField(label='Field', required=False)


class MercuryForm(forms.Form):
    mercury_host = forms.CharField(label='IP Address', max_length=100)
    mercury_port = forms.IntegerField(label='Port', required=False)
    mercury_heater_power = forms.FloatField(label='Heater Power', required=False)
    mercury_itc_temperature = forms.FloatField(label='ITC Temperature', required=False)
class RFSoCConfigForm(forms.Form):
    rfsoc_host = forms.CharField(label='IP Address', max_length=100)
    rfsoc_port = forms.IntegerField(label='Port', required=False)
    rfsoc_username = forms.CharField(label='Username', required=False)
    rfsoc_password = forms.CharField(label='Password', required=False)
    adc_trig_offset = forms.FloatField(label='ADC Trigger Offset', required=False)
    soft_avgs = forms.FloatField(label='Soft Averages', required=False)
    relax_delay = forms.FloatField(label='Relax Delay', required=False)
    readout_length = forms.FloatField(label='Readout Length', required=False)
    pulse_freq = forms.FloatField(label='Pulse Frequency', required=False)
    reps = forms.FloatField(label='Repetitions', required=False)
    eom_outch = forms.CharField(label='EOM Out Ch', required=False)
    eom_freqseq = forms.CharField(label='EOM Frequency Sequence', required=False)
    eom_timeseq = forms.CharField(label='EOM Time Sequence', required=False)
    eom_length = forms.FloatField(label='EOM Length', required=False)
    eom_pulsefreq = forms.FloatField(label='EOM Pulse Frequency', required=False)
    eom_zone = forms.FloatField(label='EOM Zone', required=False)
    eom_mode = forms.CharField(label='EOM Mode', required=False)
    freqA_res_phase = forms.FloatField(label='Frequency A Res Phase', required=False)
    freqA_pulse_gain = forms.FloatField(label='Frequency A Pulse Gain', required=False)
    freqA_pulse_freq = forms.FloatField(label='Frequency A Pulse Frequency', required=False)
    freqB_res_phase = forms.FloatField(label='Frequency B Res Phase', required=False)
    freqB_pulse_gain = forms.FloatField(label='Frequency B Pulse Gain', required=False)
    freqB_pulse_freq = forms.FloatField(label='Frequency B Pulse Frequency', required=False)
    aom_length_0 = forms.CharField(label='AOM Length', required=False)
    aom_length_1 = forms.CharField(label='AOM Length', required=False)
    aom_length_2 = forms.CharField(label='AOM Length', required=False)
    aom_length_3 = forms.CharField(label='AOM Length', required=False)
    aom_pins = forms.CharField(label='AOM Pins', required=False)
    aom_time_0 = forms.CharField(label='AOM Time', required=False)
    aom_time_1 = forms.CharField(label='AOM Time', required=False)
    aom_time_2 = forms.CharField(label='AOM Time', required=False)
    aom_time_3 = forms.CharField(label='AOM Time', required=False)

