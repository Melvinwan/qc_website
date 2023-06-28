
from qick import *
from qick.parser import load_program
# Load bitstream with custom overlay
soc = QickSoc()

soccfg = soc
freqA = {"res_phase": 90.0 , # The phase of the signal
        "pulse_gain": 2000.0, # [DAC units]
        "pulse_freq": soccfg.adcfreq(999.9999984741211, gen_ch=0, ro_ch=0), # [MHz]
        }
freqB = {"res_phase": 90.0 , # The phase of the signal
        "pulse_gain": 2000.0, # [DAC units]
        "pulse_freq": soccfg.adcfreq(999.9999984741211, gen_ch=0, ro_ch=0), # [MHz]
        }
configEOM={"out_ch":[0, 1],
        "freqA": freqA,
        "freqB": freqB,
        "freq_seq": ['freqA', 'freqB', 'freqA', 'freqB'],
        "time_seq":[50, 190, 370, 700],
        "length":100.0, # [Clock ticks]
        "pulse_freq":soccfg.adcfreq(999.9999984741211, gen_ch=0, ro_ch=0), # [MHz]
        "zone": 1.0,
        "mode": "periodic",
}

#TTL
configAOM={
        "length":[[200, 200, 200, 200], [200, 200, 200, 200], [200, 200, 200, 200], [200, 200, 200, 200]], # [Clock ticks]
        "pins":[0, 1, 2, 3],
        "time":[[0, 400, 800, 1200], [0, 400, 800, 1200], [0, 400, 800, 1200], [0, 400, 800, 1200]],
}
config= {
"adc_trig_offset": 100.0, # [Clock ticks]
"soft_avgs":1.0,
"relax_delay":1.0, # --us
#Readout
"readout_length": 2000.0, # [Clock ticks]
"pulse_freq":soccfg.adcfreq(999.9999984741211, gen_ch=0, ro_ch=0),
"reps":1.0, # --Fixed
"EOM":configEOM,
"AOM":configAOM
}

from XMLGenerator import dict_to_xml_file,xml_config_to_dict
dict_to_xml_file(config, "xilinx.xml")
