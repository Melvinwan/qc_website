# forms.py
from django import forms
from django.forms.formsets import BaseFormSet

from django import forms

class ExperimentFormNew(forms.Form):
    experiment_name = forms.CharField(label='Experiment Name')
    description = forms.CharField(label='Experiment Description')
    laser_host = forms.CharField(label='IP Address', max_length=100)
    laser_port = forms.IntegerField(label='Port', required=False)
    laser_wavelength_act = forms.FloatField(label='Wavelength')
    laser_scan_end = forms.FloatField(label='Scan End')
    laser_scan_start = forms.FloatField(label='Scan Start')
    laser_scan_freq = forms.FloatField(label='Scan Frequency')
    laser_scan_offset = forms.FloatField(label='Scan Offset')
    caylar_host = forms.CharField(label='IP Address', max_length=100)
    caylar_port = forms.IntegerField(label='Port', required=False)
    caylar_current = forms.FloatField(label='Current', required=False)
    caylar_field = forms.FloatField(label='Field', required=False)
    mercury_host = forms.CharField(label='IP Address', max_length=100)
    mercury_port = forms.IntegerField(label='Port', required=False)
    mercury_heater_power = forms.FloatField(label='Heater Power', required=False)
    mercury_itc_temperature = forms.FloatField(label='ITC Temperature', required=False)
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


DEVICE_CHOICES = (
    ('laser', 'Laser'),
    ('eom', 'EOM'),
    ('aom', 'AOM'),
    ('frequency', 'Frequency'),
)

LASER_PARAMETER_CHOICES = (
    ('frequency', 'Frequency'),
    ('amplitude', 'Amplitude'),
)

FREQUENCY_CHOICES = (
    ('A', 'A'),
    ('B', 'B'),
)

class ParameterForm(forms.Form):
    device = forms.ChoiceField(choices=DEVICE_CHOICES, label='Device')
    laser_parameter = forms.ChoiceField(choices=LASER_PARAMETER_CHOICES, label='Laser Parameter', required=False)
    laser_frequency = forms.FloatField(label='Frequency', required=False)
    laser_amplitude = forms.FloatField(label='Amplitude', required=False)
    eom_frequency = forms.ChoiceField(choices=FREQUENCY_CHOICES, label='Frequency', required=False)
    eom_time_start = forms.FloatField(label='Time Start', required=False)
    eom_length = forms.FloatField(label='Length', required=False)
    aom_pins = forms.MultipleChoiceField(choices=[(str(i), str(i)) for i in range(4)], widget=forms.CheckboxSelectMultiple, label='Pins', required=False)
    aom_start_time = forms.FloatField(label='Start Time', required=False)
    aom_length = forms.FloatField(label='Length', required=False)
    frequency_name = forms.ChoiceField(choices=FREQUENCY_CHOICES, label='Name', required=False)
    frequency_frequency = forms.FloatField(label='Frequency', required=False)
    frequency_phase = forms.FloatField(label='Phase', required=False)
    frequency_amplitude = forms.FloatField(label='Amplitude', required=False)
    def __init__(self, *args, **kwargs):
        prefix = kwargs.pop('prefix', None)
        super(ParameterForm, self).__init__(*args, **kwargs)
        self.prefix = prefix
class ExperimentForm(forms.Form):
    experiment_name = forms.CharField(label='Experiment Name')
    description = forms.CharField(widget=forms.Textarea, label='Description', required=False)

class BaseExperimentForm(BaseFormSet):
    def has_duplicate_keys(self,dictionary):
        return len(dictionary) != len(set(dictionary.keys()))
    def clean(self):
        if any(self.errors):
            return
        # device = laser_parameter = laser_frequency = laser_amplitude = eom_frequency = eom_time_start = eom_length = aom_pins = aom_start_time = aom_length = frequency_name = frequency_frequency = frequency_phase = frequency_amplitude = []
        device = {'laser':{},
                  'eom':{'frequency':[],'start_time':[],'length':[]},
                  'aom':{'start_time':[],'pins':[],'length':[]},
                  'frequency_name':{'A':{},'B':{}}}
        for form in self.forms:
            if form.cleaned_data:
                device = form.cleaned_data['device']
                laser_parameter = form.cleaned_data['laser_parameter']
                laser_frequency = form.cleaned_data['laser_frequency']
                laser_amplitude = form.cleaned_data['laser_amplitude']
                eom_frequency = form.cleaned_data['eom_frequency']
                eom_time_start = form.cleaned_data['eom_time_start']
                eom_length = form.cleaned_data['eom_length']
                aom_pins = form.cleaned_data['aom_pins']
                aom_start_time = form.cleaned_data['aom_start_time']
                aom_length = form.cleaned_data['aom_length']
                frequency_name = form.cleaned_data['frequency_name']
                frequency_frequency = form.cleaned_data['frequency_frequency']
                frequency_phase = form.cleaned_data['frequency_phase']
                frequency_amplitude = form.cleaned_data['frequency_amplitude']

                if device:
                    if device == 'laser' or device == 'Laser':
                        if laser_parameter and laser_frequency:
                            device['laser'][laser_parameter] = laser_frequency
                            if self.has_duplicate_keys(device['laser']):
                                duplicates = True
                        else:
                            raise forms.ValidationError(
                                'All Laser frequency input should be chosen.',
                                code='incomplete_laser_frequency_form'
                            )
                        if laser_parameter and laser_amplitude:
                            device['laser'][laser_parameter] = laser_amplitude
                            if self.has_duplicate_keys(device['laser']):
                                duplicates = True
                        else:
                            raise forms.ValidationError(
                                'All Laser amplitude input should be chosen.',
                                code='incomplete_laser_amplitude_form'
                            )
                        if duplicates:
                            raise forms.ValidationError(
                                'Laser Input Should be unique',
                                code='duplicate_laser'
                            )
                    elif device == "eom" or device == "EOM":
                        if eom_frequency and eom_time_start and eom_length:
                            if eom_time_start in device['eom']['start_time']:
                                duplicates = True
                            device['eom']['start_time'].append(eom_time_start)
                            device['eom']['frequency'].append(eom_frequency)
                            device['eom']['length'].append(eom_length)
                        else:
                            raise forms.ValidationError(
                                'All eom input should be chosen.',
                                code='incomplete_eom_form'
                            )
                        if duplicates:
                            raise forms.ValidationError(
                                'Laser Input Should be unique',
                                code='duplicate_eom'
                            )
                    elif device == "aom" or device == "AOM":
                        if aom_pins and aom_start_time and aom_length:
                            if aom_start_time in device['aom']['start_time']:
                                duplicates = True
                            device['aom']['start_time'].append(aom_start_time)
                            device['aom']['pins'].append(aom_pins)
                            device['aom']['length'].append(aom_length)
                        else:
                            raise forms.ValidationError(
                                'All eom input should be chosen.',
                                code='incomplete_eom_form'
                            )
                        if duplicates:
                            raise forms.ValidationError(
                                'Laser Input Should be unique',
                                code='duplicate_aom'
                            )
                    elif device == "frequency" or device == "Frequency":
                        if frequency_name and frequency_frequency and frequency_amplitude and frequency_phase:
                            if frequency_name == "A" and len(device['frequency_name']["A"])==0:
                                duplicates = True
                            device['frequency_name']["A"] = {"frequency":frequency_frequency,"amplitude":frequency_amplitude,"phase":frequency_phase}
                            if frequency_name == "B" and len(device['frequency_name']["B"])==0:
                                duplicates = True
                            device['frequency_name']["B"] = {"frequency":frequency_frequency,"amplitude":frequency_amplitude,"phase":frequency_phase}
                        else:
                            raise forms.ValidationError(
                                'All Frequency input should be chosen.',
                                code='incomplete_freq_form'
                            )
                        if duplicates:
                            raise forms.ValidationError(
                                'Frequency Input Should be unique',
                                code='duplicate_freq'
                            )


class LaserForm(forms.Form):
    laser_host = forms.CharField(label='IP Address', max_length=100)
    laser_port = forms.IntegerField(label='Port', required=False)
    wavelength_act = forms.FloatField(label='Wavelength')
    scan_end = forms.FloatField(label='Scan End')
    scan_start = forms.FloatField(label='Scan Start')
    scan_freq = forms.FloatField(label='Scan Frequency')
    scan_offset = forms.FloatField(label='Scan Offset')

class LaserFormIP(forms.Form):
    laser_host = forms.CharField(label='IP Address', max_length=100)
    laser_port = forms.IntegerField(label='Port', required=False)

class LaserFormConfig(forms.Form):
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
    # eom_freqseq0 = forms.CharField(label='EOM Frequency Sequence Channel 0', required=False)
    # eom_freqseq1 = forms.CharField(label='EOM Frequency Sequence Channel 1', required=False)
    # eom_timeseq0 = forms.CharField(label='EOM Time Sequence 0', required=False)
    # eom_length0 = forms.FloatField(label='EOM Length 0', required=False)
    # eom_timeseq1 = forms.CharField(label='EOM Time Sequence 1', required=False)
    # eom_length1 = forms.FloatField(label='EOM Length 1', required=False)
    # eom_pulsefreq = forms.FloatField(label='EOM Pulse Frequency', required=False)
    eom_zone0 = forms.FloatField(label='EOM Zone 0', required=False)
    eom_mode0 = forms.CharField(label='EOM Mode 0', required=False)
    eom_zone1 = forms.FloatField(label='EOM Zone 1', required=False)
    eom_mode1 = forms.CharField(label='EOM Mode 1', required=False)
    freqA0_res_phase = forms.FloatField(label='Frequency A0 Res Phase', required=False)
    freqA0_pulse_gain = forms.FloatField(label='Frequency A0 Pulse Gain', required=False)
    freqA0_pulse_freq = forms.FloatField(label='Frequency A0 Pulse Frequency', required=False)
    freqB0_res_phase = forms.FloatField(label='Frequency B0 Res Phase', required=False)
    freqB0_pulse_gain = forms.FloatField(label='Frequency B0 Pulse Gain', required=False)
    freqB0_pulse_freq = forms.FloatField(label='Frequency B0 Pulse Frequency', required=False)
    freqA1_res_phase = forms.FloatField(label='Frequency A1 Res Phase', required=False)
    freqA1_pulse_gain = forms.FloatField(label='Frequency A1 Pulse Gain', required=False)
    freqA1_pulse_freq = forms.FloatField(label='Frequency A1 Pulse Frequency', required=False)
    freqB1_res_phase = forms.FloatField(label='Frequency B1 Res Phase', required=False)
    freqB1_pulse_gain = forms.FloatField(label='Frequency B1 Pulse Gain', required=False)
    freqB1_pulse_freq = forms.FloatField(label='Frequency B1 Pulse Frequency', required=False)
    aom_length_0 = forms.CharField(label='AOM Length', required=False)
    aom_length_1 = forms.CharField(label='AOM Length', required=False)
    aom_length_2 = forms.CharField(label='AOM Length', required=False)
    aom_length_3 = forms.CharField(label='AOM Length', required=False)
    aom_pins = forms.CharField(label='AOM Pins', required=False)
    aom_time_0 = forms.CharField(label='AOM Time', required=False)
    aom_time_1 = forms.CharField(label='AOM Time', required=False)
    aom_time_2 = forms.CharField(label='AOM Time', required=False)
    aom_time_3 = forms.CharField(label='AOM Time', required=False)

class RFSoCFrequencySequenceForm0(forms.Form):
    frequency0 = forms.CharField(label='EOM Frequency Sequence Channel 0', required=False)
    time0 = forms.FloatField(label='EOM Length 0', required=False)
    length0 = forms.FloatField(label='EOM Length 0', required=False)
class RFSoCFrequencySequenceForm1(forms.Form):
    frequency1 = forms.CharField(label='EOM Frequency Sequence Channel 1', required=False)
    time1 = forms.FloatField(label='EOM Length 1', required=False)
    length1 = forms.FloatField(label='EOM Length 1', required=False)