import math
import numpy as np
from engineering_notation import EngNumber
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
from matplotlib.pyplot import semilogx
from matplotlib import pyplot

import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()

from PySpice.Doc.ExampleTools import find_libraries
from PySpice.Probe.Plot import plot
from PySpice.Spice.Library import SpiceLibrary
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

##*********************************************
# Set the path where the op-amp uA741.lib file is located
# Place the *.lib file in the same folder as the script file
# C:\\Users\\abhis\\Desktop\\MainProject\\app\\backend\\
libraries_path ='C:\\Users\\abhis\\Desktop\\MainProject\\app\\backend\\'
spice_library = SpiceLibrary(libraries_path)

##*********************************************
## Circuit Netlist
circuit = Circuit('Op-amp circuits - Example 1 Non-inverting op-amp Amplifier')
circuit.include("uA741.lib")

# Define amplitude and frequency of input sinusoid
amp=0.2@u_V
freq=1@u_kHz

# Define transient simulation step time and stop time
steptime=1@u_us
finaltime = 5*(1/freq)

source = circuit.SinusoidalVoltageSource(1, 'x', circuit.gnd, amplitude=amp, frequency = freq)
circuit.V(2, '+Vcc', circuit.gnd,15@u_V)
circuit.V(3, '-Vcc', circuit.gnd,-15@u_V)

circuit.X(1, 'uA741', 'input', 'v-', '+Vcc', '-Vcc', 'out')

# circuit.R(1, 'v-', circuit.gnd,  1@u_kΩ)
# circuit.R(2, 'v-', 'x',          2@u_kΩ)
# circuit.R(3, 'x', 'out',         3@u_kΩ)
# circuit.R(4, 'x', circuit.gnd,   4@u_kΩ)
# circuit.R('L', 'out', circuit.gnd,10@u_kΩ)
circuit.R(1, 'v-', 'out',  10@u_kΩ)
circuit.R(2, 'v-', 'x',  1@u_kΩ)
circuit.R(3, 'input', circuit.gnd,1@u_kΩ)
# circuit.R('L', 'out', circuit.gnd,10@u_kΩ)

##*********************************************
## Simulation: Transient Analysis
simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.transient(step_time=steptime, end_time=finaltime)

##*********************************************
## Theory: See video Op-amp circuits - Example 1 Non-inverting op-amp Amplifier

# Gain = (1+ circuit.R2.resistance/circuit.R1.resistance +
#         circuit.R3.resistance/circuit.R1.resistance+
#         circuit.R3.resistance/circuit.R4.resistance+
#         (circuit.R2.resistance*circuit.R3.resistance)/
#         (circuit.R1.resistance*circuit.R4.resistance))
# print(Gain)

time=np.array(analysis.time)
# vout = Gain*(amp)*(np.sin(2*np.pi*freq*time))


##*********************************************
# PLOTTING COMMANDS

figure, axe = plt.subplots(figsize=(10, 6))

plt.title('Op-amp circuits - Example 2 Inverting op-amp Amplifier')
plt.xlabel('Time [s]')
plt.ylabel('Voltage [V]')
plt.grid()
plot(analysis['x'], axis=axe)
plot(analysis['out'], axis=axe)
# plt.plot(time, vout)
plt.legend(('sim:input', 'sim:output', 'theory'), loc=(.05,.1))
cursor = Cursor(axe, useblit=True, color='red', linewidth=1)
plt.tight_layout()
plt.show()