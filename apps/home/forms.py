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
class RFSoCForm(forms.Form):
    rfsoc_host = forms.CharField(label='IP Address', max_length=100)
    rfsoc_port = forms.IntegerField(label='Port',required=False)
