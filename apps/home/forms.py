# forms.py
from django import forms

class LaserForm(forms.Form):
    laser_host = forms.CharField(label='IP Address', max_length=100)
    laser_port = forms.IntegerField(label='Port', required=False)
    wavelength_act = forms.IntegerField(label='Wavelength')
    scan_end = forms.IntegerField(label='Scan End')
    scan_start = forms.IntegerField(label='Scan Start')
    scan_freq = forms.IntegerField(label='Scan Frequency')
    scan_offset = forms.IntegerField(label='Scan Offset')


# forms.py
class CaylarForm(forms.Form):
    caylar_host = forms.CharField(label='IP Address', max_length=100)
    caylar_port = forms.IntegerField(label='Port', required=False)
    caylar_current = forms.CharField(label='Current', max_length=100, required=False)
    caylar_field = forms.CharField(label='Field', max_length=100, required=False)


class MercuryForm(forms.Form):
    mercury_host = forms.CharField(label='IP Address', max_length=100)
    mercury_port = forms.IntegerField(label='Port', required=False)
    mercury_heater_power = forms.CharField(label='Heater Power', max_length=100, required=False)
    mercury_itc_temperature = forms.CharField(label='ITC Temperature', max_length=100, required=False)
class RFSoCConfigForm(forms.Form):
    rfsoc_host = forms.CharField(label='IP Address', max_length=100)
    rfsoc_port = forms.IntegerField(label='Port', required=False)
    rfsoc_username = forms.CharField(label='Username', required=False)
    rfsoc_password = forms.CharField(label='Password', required=False)
    adc_trig_offset = forms.IntegerField(label='ADC Trigger Offset', required=False)
    soft_avgs = forms.IntegerField(label='Soft Averages', required=False)
    relax_delay = forms.FloatField(label='Relax Delay', required=False)
    readout_length = forms.IntegerField(label='Readout Length', required=False)
    pulse_freq = forms.FloatField(label='Pulse Frequency', required=False)
    reps = forms.IntegerField(label='Repetitions', required=False)
    eom_outch = forms.CharField(label='EOM Out Ch', required=False)
    eom_freqseq = forms.CharField(label='EOM Frequency Sequence', required=False)
    eom_timeseq = forms.CharField(label='EOM Time Sequence', required=False)
    eom_length = forms.IntegerField(label='EOM Length', required=False)
    eom_pulsefreq = forms.FloatField(label='EOM Pulse Frequency', required=False)
    eom_zone = forms.IntegerField(label='EOM Zone', required=False)
    eom_mode = forms.CharField(label='EOM Mode', required=False)
    freqA_res_phase = forms.IntegerField(label='Frequency A Res Phase', required=False)
    freqA_pulse_gain = forms.IntegerField(label='Frequency A Pulse Gain', required=False)
    freqA_pulse_freq = forms.FloatField(label='Frequency A Pulse Frequency', required=False)
    freqB_res_phase = forms.IntegerField(label='Frequency B Res Phase', required=False)
    freqB_pulse_gain = forms.IntegerField(label='Frequency B Pulse Gain', required=False)
    freqB_pulse_freq = forms.FloatField(label='Frequency B Pulse Frequency', required=False)
    aom_length = forms.CharField(label='AOM Length', required=False)
    aom_pins = forms.CharField(label='AOM Pins', required=False)
    aom_time = forms.CharField(label='AOM Time', required=False)

