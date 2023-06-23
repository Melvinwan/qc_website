# forms.py
from django import forms

class LaserForm(forms.Form):
    laser_host = forms.CharField(label='IP Address', max_length=100)
    laser_port = forms.IntegerField(label='Port',required=False)
