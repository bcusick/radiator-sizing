import math
import ht
import fluids
import thermo
import intercoolerSizing as cooler

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import interpolate

def psi_to_Pa(P):
    P=P/14.5038*1E5
    return P

def ft_to_m(ft):
    m= ft*12.*25.4/1000.
    return m

#specific fuel consumption
specFuel =0.37 #lb/HP/hr
specFuel = specFuel/2.2 #kg/HP/hr
specFuel = specFuel/750. #kg/W/hr
specFuel = specFuel/3600. #kg/W/s

bore = 96 #mm
stroke = 103#mm
cylinders = 4

revs = 3600 #rpm

displacement = (math.pi * (bore/2.)**2) * stroke * cylinders
displacement = displacement / (1E3**3) #m3

flowVol = displacement/2. * revs/60.  #m3/s
volEff = 0.75
flowVol = flowVol * volEff

elevation = 0 # ft
elevation = ft_to_m(elevation)
ambient = 25 #C
ambient +=273 #K

#get air components and pressure at given elevation
atm = fluids.ATMOSPHERE_NRLMSISE00(Z=elevation) #z is meters
Patm = atm.P
N2 = atm.zs[0]
O2 = atm.zs[1]
Ar = atm.zs[2]

#create air mixture so I can get some properties I need
air = thermo.Mixture(['nitrogen', 'oxygen', 'argon'], Vfgs=[N2, O2, Ar], T=ambient, P=Patm)
k = air.isentropic_exponent
D1 = air.rho

# recalculate air density at given temp and pressure
def air_density_calc(T, P):
    air.calculate(T=T, P=P)
    density = air.rho
    return density

#compressor values
Pgage = 30. #psi gage
Pgage= psi_to_Pa(Pgage) #Pa gage
Pabs = Pgage + Patm

eta = .7 #compressor effieciency
#temp and density out of compressor
Tturbo = fluids.isentropic_T_rise_compression(P1=Patm, P2=Pabs, T1=ambient, k=k, eta=eta)
D2 = air_density_calc(T=Tturbo, P=Pabs)

#loop intercooler calcs since flowrate influences Tout from intercooler
Tcooler = Tturbo
Told = 0
while math.fabs(Told-Tcooler) >1E-6:
    Told = Tcooler
    #print Tcooler-273
    D3 = air_density_calc(T=Tcooler, P=Pabs) #need to include pressure drop here, should be manifold pressure
    massflowAir = flowVol * D3 #kg/s, mass flow into engine
    #flowVolCooler=massflowAir/D2
    Tcooler = cooler.get_Tout(Tturbo, massflowAir, D2) + 273.0
    print massflowAir
    #print Told-Tcooler

coolerEff = (Tturbo - Tcooler)/ (Tturbo - ambient)
#How much fuel can I add to available air
air_fuel=17.5
massflowFuel = massflowAir/air_fuel

massflowAirNoCooler = flowVol *D2
massflowFuelNoCooler = massflowAirNoCooler/air_fuel

#How much power do I get from fuel mass
power= massflowFuel/specFuel #watts
power= power/750 #HP

powerNoCooler = massflowFuelNoCooler/specFuel/750

CFM_engine = flowVol * (3.281**3) * 60 #convert from SI back to CFM
CFM_cooler = CFM_engine *D3/D2
CFM_filter = CFM_engine *D3/D1

Data = {'Power':power, 'CFM_engine':CFM_engine, 'CFM_cooler':CFM_cooler, 'CFM_filter':CFM_filter,
        'Turbo Tmep':Tturbo-273, 'Cooler Temp':Tcooler-273, 'Cooler Eff': coolerEff}
print Data
print 'Intercooler Adds {0} HP'.format(round(power-powerNoCooler))




'''
print x
print x.k
print x.Cp
print x.rho
print x.mu
'''
'''
graph = pd.Series(Cp, index=per)
graph.plot()
plt.show()

#print air

print air
#print air.Cp
print N.Cp
print O.Cp
print Ar.Cp
'''
