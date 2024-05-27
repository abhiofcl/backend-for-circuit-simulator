from flask import Flask, request, jsonify
import json
import io
import numpy as np
import matplotlib.pyplot as plt
from PySpice.Spice.Netlist import Circuit
from PySpice.Spice.Library import SpiceLibrary
from PySpice.Unit import *


app = Flask(__name__)
# if __name__ == "main":
#     app.run(host="127.0.0.1", port=8080, debug=True)

response = ''

# clipper circuit routes

@app.route("/api/clipper/<choice>", methods=['GET', 'POST'])
def clipper(choice):
    
    resistorValue = 1000
    sourceVoltage = 5
    
    global response
    if(request.method == 'POST'):
        # decoding the received data
        request_data = request.data
        request_data = json.loads(request_data.decode('utf-8'))
        resistorValue = int(request_data['resistorV']) 
        sourceVoltage = int(request_data['sourceVolt'])
        

        # defining the circuit netlist

        circuit = Circuit("Clipper Circuit")
        
        # model for diode 1n4148
        circuit.model('MyDiode', 'D', Is=4.352e-6,
                      Rs=0.6458, BV=110, IBV=0.0001, N=1.906)
        
        # starting of netlist creation

        circuit.SinusoidalVoltageSource(1, 'n1', circuit.gnd, amplitude=sourceVoltage, frequency=60)
        circuit.R(1, 'n2', circuit.gnd, resistorValue)
        if (choice == "1"):
            #negative clipper
            circuit.Diode(1, 'n1', 'n2', model='MyDiode')
        elif (choice == "2"):
            #positive clipper
            circuit.Diode(1, 'n2', 'n1', model='MyDiode')
        
        #netlist ended

        #starting simulation
        simulator = circuit.simulator(temperature=25, nominal_temperature=25)
        analysis = simulator.transient(step_time=1e-6, end_time=100e-3)

        #values for input and output graphs
        xaxis = np.array(analysis.time).tolist()
        yaxisop = np.array(analysis['n2']).tolist()
        yaxisip = np.array(analysis['n1']).tolist()
        
        #returning json with the values required for plotting the graph
        return jsonify({'time': xaxis, 'yo': yaxisop, 'yi': yaxisip})
    
@app.route("/api/bclipper/<choice>", methods=['GET', 'POST'])    
def biasedclipper(choice):
    resistorValue = 1000
    sourceVoltage = 5
    biasingVolt = 2

    if(request.method == 'POST'):
        # decoding the received data
        request_data = request.data
        request_data = json.loads(request_data.decode('utf-8'))
        resistorValue = int(request_data['resistorV']) 
        sourceVoltage = int(request_data['sourceVolt'])
        
        biasedVolt =   int(request_data['biasedVoltVal'])

        circuit = Circuit("Positive biased positive clipper")
        # model for diode 1n4148
        circuit.model('MyDiode', 'D', Is=4.352e-6,Rs=0.6458, BV=110, IBV=0.0001, N=1.906)

        circuit.SinusoidalVoltageSource(1, 'n1', circuit.gnd, amplitude=sourceVoltage, frequency=60)
        
        
        circuit.R(1, 'n2', 'n3', resistorValue)
        if( choice == "1"):
            #positive bias positive clipper
            circuit.Diode(1, 'n2', 'n1', model='MyDiode')
            circuit.V('V1', 'n3', circuit.gnd, biasedVolt)
        elif( choice == "2"):
            #negative bias positive clipper
            circuit.Diode(1, 'n2', 'n1', model='MyDiode')
            circuit.V('V1',circuit.gnd, 'n3' , biasedVolt)
        elif( choice == "3"):
            #positive bias negative clipper
            circuit.Diode(1, 'n1', 'n2', model='MyDiode')
            circuit.V('V1', 'n3', circuit.gnd, biasedVolt)
        elif( choice == "4"):
            #negative bias negative clipper
            circuit.Diode(1, 'n1', 'n2', model='MyDiode')
            circuit.V('V1',circuit.gnd, 'n3' , biasedVolt)
        simulator = circuit.simulator(temperature=25, nominal_temperature=25)
        analysis = simulator.transient(step_time=1e-6, end_time=100e-3)

        #values for input and output graphs
        xaxis = np.array(analysis.time).tolist()
        yaxisop = np.array(analysis['n2']).tolist()
        yaxisip = np.array(analysis['n1']).tolist()
        
        #returning json with the values required for plotting the graph
        return jsonify({'time': xaxis, 'yo': yaxisop, 'yi': yaxisip})
    else:
        
        circuit = Circuit("Positive biased positive clipper")
            # model for diode 1n4148
        circuit.model('MyDiode', 'D', Is=4.352e-6,Rs=0.6458, BV=110, IBV=0.0001, N=1.906)

        circuit.SinusoidalVoltageSource(1, 'n1', circuit.gnd, amplitude=sourceVoltage, frequency=60)
        
        circuit.Diode(1, 'n2', 'n1', model='MyDiode')
        circuit.R(1, 'n2', 'n3', resistorValue)
        if( choice == "1"):
            #positive bias
            circuit.V('V1', 'n3', circuit.gnd, 2)
        elif( choice =="2"):
            #negative bias
            circuit.V('V1',circuit.gnd, 'n3' , 2)

        simulator = circuit.simulator(temperature=25, nominal_temperature=25)
        analysis = simulator.transient(step_time=1e-6, end_time=100e-3)

        #values for input and output graphs
        xaxis = np.array(analysis.time).tolist()
        yaxisop = np.array(analysis['n2']).tolist()
        yaxisip = np.array(analysis['n1']).tolist()
        
        #returning json with the values required for plotting the graph
        return jsonify({'time': xaxis, 'yo': yaxisop, 'yi': yaxisip})
# clamper circuit routes

@app.route("/api/clamper/<choice>", methods=['GET','POST'])
def clamper(choice):
    # print(request.form)
    
    capacitorValue = 10
    sourceVoltage = 5
    freq=1@u_kHz
    request_data = request.data
    request_data = json.loads(request_data.decode('utf-8'))
    capacitorValue = int(request_data['capacitorV']) 
    sourceVoltage = int(request_data['sourceVolt'])
    
    circuit = Circuit("Clamper ")
        # model for diode 1n4148
    circuit.model('MyDiode', 'D', Is=4.352e-6,Rs=0.6458, BV=110, IBV=0.0001, N=1.906)

    circuit.SinusoidalVoltageSource(1, 'n1', circuit.gnd, amplitude=sourceVoltage, frequency=60)
    
    
    circuit.C(1, 'n1', 'n2', capacitorValue@u_uF)
    if(choice == "1"):
        #positive clamper
        circuit.Diode(1, circuit.gnd, 'n2', model='MyDiode')
    elif(choice=="2"):
        #negative clamper
        circuit.Diode(1, 'n2',circuit.gnd, model='MyDiode')

    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.transient(step_time=1e-6, end_time=100e-3)
    xaxis = np.array(analysis.time).tolist()
    yaxisop = np.array(analysis['n2']).tolist()
    # yaxisop = np.array(analysis['n2'])
    yaxisip = np.array(analysis['n1']).tolist()
    
    
    return jsonify({'time': xaxis, 'yo': yaxisop, 'yi': yaxisip})
    # return jsonify({'time': xaxis, 'yo': yaxisop})
    # data = [{'time': f, 'yo': g} for f, g in zip(xaxis, yaxisop)]
    # return jsonify(data)

#biased clampers
@app.route("/api/biasedclamper/<choice>", methods=['GET','POST'])
def bclamper(choice):
    capacitorValue = 10
    sourceVoltage = 5
    freq=1@u_kHz
    biasedVolt=2
    request_data = request.data
    request_data = json.loads(request_data.decode('utf-8'))
    resistorValue = float(request_data['resistorV'])
    sourceVoltage = float(request_data['sourceVolt'])
    capacitorValue = float(request_data['capacitorV'])
    biasedVolt=float(request_data['biasedVoltVal'])
    # sourceVoltage = 5
    freq=1@u_kHz
    
    
    circuit = Circuit("Positive biased positive clipper")
        # model for diode 1n4148
    circuit.model('MyDiode', 'D', Is=4.352e-6,Rs=0.6458, BV=110, IBV=0.0001, N=1.906)

    circuit.SinusoidalVoltageSource(1, 'n1', circuit.gnd, amplitude=sourceVoltage, frequency=60)
    
    
    circuit.C(1, 'n1', 'n2', capacitorValue@u_uF)
    if(choice == "1"):
        #positive clamper with positive bias
        circuit.Diode(1, 'n3', 'n2', model='MyDiode')
        circuit.V('V1', 'n3', circuit.gnd, biasedVolt)
    elif(choice == "2"):
        #positive clamper with negative bias
        circuit.Diode(1, 'n3', 'n2', model='MyDiode')
        circuit.V('V1',  circuit.gnd,'n3', biasedVolt)
    elif(choice=="3"):
        #negative clamper with positive bias
        circuit.Diode(1, 'n2','n3', model='MyDiode')
        circuit.V('V1', 'n3', circuit.gnd, biasedVolt)
    elif(choice=="3"):
        #negative clamper with negative bias
        circuit.Diode(1, 'n2','n3', model='MyDiode')
        circuit.V('V1',  circuit.gnd, 'n3',biasedVolt)

    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.transient(step_time=1e-6, end_time=100e-3)
    xaxis = np.array(analysis.time).tolist()
    yaxisop = np.array(analysis['n2']).tolist()
    # yaxisop = np.array(analysis['n2'])
    yaxisip = np.array(analysis['n1']).tolist()
    
    
    return jsonify({'time': xaxis, 'yo': yaxisop, 'yi': yaxisip})

#opamp circuits

libraries_path ='C:\\Users\\abhis\\Desktop\\MainProject\\app\\backend\\'
spice_library = SpiceLibrary(libraries_path)

@app.route("/api/opamp/<choice>", methods=['GET','POST'])
def opamp(choice):
    circuit = Circuit('Op-amp circuits - Non-inverting op-amp Amplifier')
    circuit.include("uA741.lib")

    # Define amplitude and frequency of input sinusoid
    amp=0.2@u_V
    freq=10@u_kHz
    request_data = request.data
    request_data = json.loads(request_data.decode('utf-8'))
    R1 = float(request_data['R1'])
    R2 = float(request_data['R2'])
    source = float(request_data['sourceVolt'])
    # Define transient simulation step time and stop time
    steptime=1@u_us
    finaltime = 3*(1/freq)

    
    circuit.V(2, '+Vcc', circuit.gnd,15@u_V)
    circuit.V(3, '-Vcc', circuit.gnd,-15@u_V)

    circuit.X(1, 'uA741', 'v+', 'v-', '+Vcc', '-Vcc', 'out')
    if(choice=="1"):
        # non inverting opamp
        circuit.SinusoidalVoltageSource(1, 'v+', circuit.gnd, amplitude=amp, frequency = freq)
        circuit.R(1, 'v-', 'out',  10@u_kΩ)
        circuit.R(2, 'v-', circuit.gnd,  1@u_kΩ)
        # circuit.R(3, 'v+', circuit.gnd,1@u_kΩ)
    elif(choice=="2"):
        #inverting opamp
        circuit.SinusoidalVoltageSource(1, 'x', circuit.gnd, amplitude=source, frequency = freq)
        circuit.R(1, 'v-', 'out',  R1)
        circuit.R(2, 'v-', 'x',  R2)
        circuit.R('3', 'v+', circuit.gnd,1@u_kΩ)
    


    ##*********************************************
    ## Simulation: Transient Analysis
    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.transient(step_time=steptime, end_time=finaltime)

    xaxis = np.array(analysis.time).tolist()
    yaxisop = np.array(analysis['out']).tolist()
    if(choice=="1"):
        #ninv
        yaxisip = np.array(analysis['v+']).tolist()
    elif(choice=="2"):
        #inv
        yaxisip = np.array(analysis['x']).tolist()
    return jsonify({'time': xaxis, 'yo': yaxisop, 'yi': yaxisip})

#low pass filter
@app.route("/api/opamp/lpf/<choice>", methods=['GET'])
def lpfop(choice):
    circuit = Circuit('Inverting Op-amp Low-Pass Filter')
    circuit.include("uA741.lib")

    circuit.SinusoidalVoltageSource(1, 'input', circuit.gnd, amplitude=1@u_V,frequency=1@u_kHz)

    # Low pass filter
    circuit.R('4', 'v-', 'out', 15@u_kΩ)
    circuit.R('1', 'v-', circuit.gnd, 10@u_kΩ)

    circuit.R('6', 'v+', 'x', 2.2@u_kΩ)
    circuit.R('5', 'x', 'input', 2.2@u_kΩ)

    circuit.C('1', 'v+', circuit.gnd, 100@u_nF)
    circuit.C('2', 'x', 'out', 100@u_nF)


    circuit.V(2, '+Vcc', circuit.gnd,15@u_V)
    circuit.V(3, '-Vcc', circuit.gnd,-15@u_V)

    circuit.X(1, 'uA741', 'v+', 'v-', '+Vcc', '-Vcc', 'out')
    deg = True
    start=1@u_Hz
    stop=1@u_MHz
    points=10
    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.ac(start_frequency=start, stop_frequency=stop, number_of_points=points,  variation='dec')
    

    F=analysis.frequency.tolist()
    G=(20*np.log10(np.abs(analysis.out)))
    data = [{'frequency': f, 'magnitude': g} for f, g in zip(F, G)]
    return jsonify(data)
    # xaxis = np.array(analysis.frequency).tolist()
    # yaxisop = np.array(20*np.log10(np.abs(analysis.out))).tolist()
    # yaxisip = np.array(analysis['input']).tolist()
    # return jsonify({'time': xaxis, 'yo': yaxisop})

# high pass filter
@app.route("/api/opamp/hpf/<choice>", methods=['GET'])
def hpfop(choice):
    circuit = Circuit('Inverting Op-amp Low-Pass Filter')
    circuit.include("uA741.lib")
    amp=1@u_V
    freq=1@u_kHz

    circuit.SinusoidalVoltageSource(1, 'input', circuit.gnd, amplitude=amp,frequency=freq)

# Low pass filter
    circuit.R('4', 'v-', 'out', 15@u_kΩ)
    circuit.R('1', 'v-', circuit.gnd, 10@u_kΩ)

    circuit.C('1', 'v+', 'x', 100@u_nF)
    circuit.C('2', 'x', 'input', 100@u_nF)

    circuit.R('2', 'v+', circuit.gnd, 2.2@u_kΩ)
    circuit.R('3', 'x', 'out', 2.2@u_kΩ)


    circuit.V(2, '+Vcc', circuit.gnd,15@u_V)
    circuit.V(3, '-Vcc', circuit.gnd,-15@u_V)

    circuit.X(1, 'uA741', 'v+', 'v-', '+Vcc', '-Vcc', 'out')
    deg = True
    start=1@u_Hz
    stop=1@u_MHz
    points=10
    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.ac(start_frequency=start, stop_frequency=stop, number_of_points=points,  variation='dec')
    

    F=analysis.frequency.tolist()
    G=20*np.log10(np.abs(analysis.out))
    data = [{'frequency': f, 'magnitude': g} for f, g in zip(F, G)]
    return jsonify(data)

# integrator using opamp

@app.route("/api/opamp/integrator/<choice>", methods=['GET'])
def integratorop(choice):
    circuit = Circuit('Integrator')
    circuit.include("uA741.lib")

    circuit.X(1, 'uA741', circuit.gnd, 'v-', '+Vcc', '-Vcc', 'out')
    # circuit.SinusoidalVoltageSource(1, 'input', circuit.gnd, amplitude=4@u_V,frequency=1@u_kHz)
    circuit.PulseVoltageSource(1,'input',circuit.gnd,initial_value=0,pulsed_value=2,delay_time=0,rise_time=0.0001@u_ms,fall_time=0.0001@u_ms,pulse_width=0.5@u_ms,period=1@u_ms)

    # Integrator
    circuit.R('1', 'v-', 'out', 150@u_kΩ)
    circuit.R('2', 'v-', 'input', 15@u_kΩ)
    circuit.C('1', 'v-', 'out', 10@u_nF)




    circuit.V(2, '+Vcc', circuit.gnd,15@u_V)
    circuit.V(3, '-Vcc', circuit.gnd,-15@u_V)



    # circuit.R(1, 'input', 'v-',  159.1549@u_Ω)
    # circuit.R('L', 'out', circuit.gnd,10@u_kΩ)


    ##*********************************************
    ## Circuit Simulation

    deg = True
    freq=1@u_kHz
    stop=0.1@u_MHz
    points=10
    steptime=1@u_us
    finaltime = 10*(1/freq)
    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.transient(step_time=steptime, end_time=finaltime)
    

    xaxis = np.array(analysis.time).tolist()
    yaxisop = np.array(analysis['out']).tolist()
    yaxisip = np.array(analysis['input']).tolist()
    

    return jsonify({'time': xaxis, 'yo': yaxisop, 'yi': yaxisip})

# diffenrentiator using opamp
@app.route("/api/opamp/differentiator/<choice>", methods=['GET'])
def differentiatorop(choice):
    circuit = Circuit('Differentiator')
    circuit.include("uA741.lib")

    circuit.X(1, 'uA741', circuit.gnd, 'v-', '+Vcc', '-Vcc', 'out')
    # circuit.SinusoidalVoltageSource(1, 'input', circuit.gnd, amplitude=4@u_V,frequency=1@u_kHz)
    circuit.PulseVoltageSource(1,'input',circuit.gnd,initial_value=0,pulsed_value=2,delay_time=0,rise_time=0.0001@u_ms,fall_time=0.0001@u_ms,pulse_width=0.5@u_ms,period=1@u_ms)
    # circuit.PulseVoltageSource(1,'input',circuit.gnd,initial_value=0,pulsed_value=2,delay_time=0,rise_time=0.5@u_ms,fall_time=0.5@u_ms,pulse_width=0.0001@u_ns,period=1@u_ms)

    # Integrator
    circuit.R('1', 'v-', 'out', 150@u_kΩ)
    circuit.R('2', 'x', 'input', 15@u_kΩ)
    circuit.C('1', 'v-', 'out', 10@u_nF)
    circuit.C('2', 'v-', 'x', 10@u_nF)
    # circuit.R('4', 'v-', 'out', 15@u_kΩ)

    # circuit.R('6', 'v+', 'x', 2.2@u_kΩ)
    # circuit.R('5', 'x', 'input', 2.2@u_kΩ)

    # circuit.C('1', 'v+', circuit.gnd, 100@u_nF)
    # circuit.C('2', 'x', 'out', 100@u_nF)


    circuit.V(2, '+Vcc', circuit.gnd,15@u_V)
    circuit.V(3, '-Vcc', circuit.gnd,-15@u_V)

    # circuit.R(1, 'input', 'v-',  159.1549@u_Ω)
    # circuit.R('L', 'out', circuit.gnd,10@u_kΩ)


    ##*********************************************
    ## Circuit Simulation

    deg = True
    freq=1@u_kHz
    stop=0.1@u_MHz
    points=10
    steptime=1@u_us
    finaltime = 10*(1/freq)
    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.transient(step_time=steptime, end_time=finaltime)
    

    xaxis = np.array(analysis.time).tolist()
    yaxisop = np.array(analysis['out']).tolist()
    yaxisip = np.array(analysis['input']).tolist()
    

    return jsonify({'time': xaxis, 'yo': yaxisop, 'yi': yaxisip})


#Schmitt trigger
@app.route("/api/opamp/schmitt/<choice>", methods=['GET'])
def schmitt(choice):
    circuit = Circuit('Op-amp circuits - Example 1 Schmitt trigger')
    circuit.include("uA741.lib")

    # Define amplitude and frequency of input sinusoid
    amp=7@u_V
    freq=1@u_kHz

    # Define transient simulation step time and stop time
    steptime=1@u_us
    finaltime = 5*(1/freq)

    circuit.SinusoidalVoltageSource(1, 'v-', circuit.gnd, amplitude=amp, frequency = freq)
    circuit.V(2, '+Vcc', circuit.gnd,15@u_V)
    circuit.V(3, '-Vcc', circuit.gnd,-15@u_V)

    circuit.X(1, 'uA741', 'input', 'v-', '+Vcc', '-Vcc', 'out')
    circuit.R(1,'input',circuit.gnd,1@u_kΩ)
    circuit.R(2,'input','out',2@u_kΩ)


    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.transient(step_time=steptime, end_time=finaltime)
    xaxis = np.array(analysis.time).tolist()
    yaxisop = np.array(analysis['out']).tolist()
    yaxisip = np.array(analysis['v-']).tolist()
    

    return jsonify({'time': xaxis, 'yo': yaxisop, 'yi': yaxisip})

@app.route("/api/opamp/triangle/<choice>", methods=['GET'])
def trianglegen(choice):
    circuit = Circuit('Op-amp circuits - Example 1 Non-inverting op-amp Amplifier')
    circuit.include("uA741.lib")
    amp=0.2@u_V
    freq=1@u_kHz

    # Define transient simulation step time and stop time
    steptime=1@u_us
    finaltime = 5*(1/freq)
    circuit.X(1, 'uA741', 'x', circuit.gnd, '+Vcc', '-Vcc', 'out1')
    circuit.X(2, 'uA741', circuit.gnd, 'v2-', '+Vcc', '-Vcc', 'out2')

    # circuit.SinusoidalVoltageSource(1, 'input', circuit.gnd, amplitude=amp, frequency = freq)
    circuit.V(2, '+Vcc', circuit.gnd,15@u_V)
    circuit.V(3, '-Vcc', circuit.gnd,-15@u_V)



    circuit.R(1, 'x','out1' ,  866@u_Ω)
    circuit.R(2, 'out1', 'v2-',  12@u_kΩ)
    circuit.R(3, 'x', 'out2',    180@u_Ω)
    circuit.C(1, 'v2-', 'out2',   100@u_nF)
# circuit.R('L', 'out', circuit.gnd,10@u_kΩ)


##*********************************************
## Simulation: Transient Analysis
    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.transient(step_time=steptime, end_time=finaltime)
    
    xaxis = np.array(analysis.time).tolist()
    yaxisop = np.array(analysis['out2']).tolist()
    # yaxisip = np.array(analysis['v-']).tolist()
    
    # return jsonify({'time': xaxis, 'yo': yaxisop, 'yi': yaxisip})
    return jsonify({'time': xaxis, 'yo': yaxisop})

#astable mv using opamp
@app.route("/api/opamp/astable/<choice>", methods=['GET'])
def astableop(choice):
    circuit = Circuit('Op-amp circuits - Example 2 Astable multivibrator')
    circuit.include("uA741.lib")

    # Define amplitude and frequency of input sinusoid
    amp=0.2@u_V
    freq=1@u_kHz

    # Define transient simulation step time and stop time
    steptime=20@u_us
    finaltime = 5*(1/freq)

    # source = circuit.SinusoidalVoltageSource(1, 'input', circuit.gnd, amplitude=amp, frequency = freq)
    # power supply voltages
    circuit.V(2, '+Vcc', circuit.gnd,15@u_V)
    circuit.V(3, '-Vcc', circuit.gnd,-15@u_V)

    circuit.X(1, 'uA741', 'input', 'v-', '+Vcc', '-Vcc', 'out')

    circuit.C(1,'v-',circuit.gnd,0.1@u_uF)
    circuit.R(1,'v-','out',4.7@u_kΩ)
    circuit.R(2,'input',circuit.gnd,10@u_kΩ)
    circuit.R(3,'input','out',10@u_kΩ)

    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.transient(step_time=steptime, end_time=0.01)
    xaxis = np.array(analysis.time).tolist()
    yaxisop = np.array(analysis['out']).tolist()
    yaxisip = np.array(analysis['v-']).tolist()
    
    return jsonify({'time': xaxis, 'yo': yaxisop, 'yi': yaxisip})

#monostable multivibrator using opamp
@app.route("/api/opamp/monostable/<choice>", methods=['GET'])
def monostableop(choice):
    circuit = Circuit('Op-amp circuits - Example 2 Astable multivibrator')
    circuit.include("uA741.lib")
    amp=0.2@u_V
    freq=1@u_kHz

    # Define transient simulation step time and stop time
    steptime=1@u_ms
    finaltime = 5*(1/freq)
    circuit.X(1, 'uA741', 'x', 'v-', '+Vcc', '-Vcc', 'out')
    # circuit.SinusoidalVoltageSource(1, 'input', circuit.gnd, amplitude=amp, frequency = freq)
    # circuit.PulseVoltageSource(1,'input',circuit.gnd,initial_value=0,pulsed_value=5,delay_time=0,rise_time=0.0001@u_ms,fall_time=0.0001@u_ms,pulse_width=0.5@u_ms,period=1@u_ms)
    circuit.PulseVoltageSource(1,'input',circuit.gnd,initial_value=0,pulsed_value=5,delay_time=0,rise_time=0.00001@u_ms,fall_time=0.00001@u_ms,pulse_width=1@u_ms,period=2@u_ms)
    circuit.model('MyDiode', 'D', Is=4.352e-6,Rs=0.6458, BV=110, IBV=0.0001, N=1.906)
    # power supply voltages
    circuit.V(2, '+Vcc', circuit.gnd,15@u_V)
    circuit.V(3, '-Vcc', circuit.gnd,-15@u_V)


    circuit.R(1,'v-','out',15@u_kΩ)
    circuit.C(1,'v-',circuit.gnd,.1@u_uF)
    circuit.Diode(1, 'v-', circuit.gnd, model='MyDiode')

    circuit.R(2,'x','out',10@u_kΩ)
    circuit.R(3,'x',circuit.gnd,10@u_kΩ)

    circuit.Diode(2, 'x', 'y', model='MyDiode')
    circuit.R(4,'y',circuit.gnd,1.2@u_kΩ)
    circuit.C(2, 'y', 'input', .1@u_uF)


    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.transient(step_time=steptime, end_time=0.01)

    xaxis = np.array(analysis.time).tolist()
    yaxisop = np.array(analysis['out']).tolist()
    yaxisip = np.array(analysis['input']).tolist()
    
    return jsonify({'time': xaxis, 'yo': yaxisop, 'yi': yaxisip})


# TESTING THE FREQUENCY RESPONSE GRAPH
@app.route("/api/freqres/<choice>", methods=['GET'])
def freqres(choice):
    circuit = Circuit('Inverting Op-amp Low-Pass Filter')
    circuit.include("uA741.lib")

    circuit.SinusoidalVoltageSource(1, 'input', circuit.gnd, amplitude=1@u_V)

    # Low pass filter
    circuit.R('f', 'v-', 'out', 1591.549@u_Ω)
    circuit.C('f', 'v-', 'out', 10@u_uF)

    circuit.V(2, '+Vcc', circuit.gnd,15@u_V)
    circuit.V(3, '-Vcc', circuit.gnd,-15@u_V)

    circuit.X(1, 'uA741', circuit.gnd, 'v-', '+Vcc', '-Vcc', 'out')

    circuit.R(1, 'input', 'v-',  159.1549@u_Ω)
    circuit.R('L', 'out', circuit.gnd,10@u_kΩ)


    ##*********************************************
    ## Simulation: Transient Analysis
    deg = True
    start=1@u_Hz
    stop=1@u_MHz
    points=10
    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.ac(start_frequency=start, stop_frequency=stop, number_of_points=points,  variation='dec')
    F=analysis.frequency.tolist()
    G=20*np.log10(np.abs(analysis.out))
    # P=np.angle(analysis.out, deg)

    # xaxis = np.array(analysis.time).tolist()
    # yaxisop = np.array(analysis['out']).tolist()
    # yaxisip = np.array(analysis['input']).tolist()
    data = [{'frequency': f, 'magnitude': g} for f, g in zip(F, G)]
    return jsonify(data)
    # return jsonify({'time': xaxis, 'yo': yaxisop, 'yi': yaxisip})

# Sinusoidal volatage source


