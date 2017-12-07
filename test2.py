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

###N = thermo.Chemical('Nitrogen')
###O = thermo.Chemical('Oxygen')
###Ar = thermo.Chemical('Argon')
###g = thermo.Chemical('glycol')

#x= thermo.Mixture(['water', 'glycol'], Vfls=[.99, .01])
#x.calculate(T=temp1+273)

#specific fuel consumption
specFuel =0.37 #lb/HP/hr
specFuel = specFuel/2.2 #kg/HP/hr
specFuel = specFuel/750. #kg/W/hr
specFuel = specFuel/3600. #kg/W/s

bore = 96 #mm
stroke = 103#mm
cylinders = 4

revs = 2000 #rpm

displacement = (math.pi * (bore/2.)**2) * stroke * cylinders
displacement = displacement / (1E3**3) #m3

flowVol = displacement/2. * revs/60.  #m3/s
volEff = 0.85
flowVol = flowVol * volEff

elevation = 0 # ft
elevation = ft_to_m(elevation)
ambient = 25 #C
ambient +=273 #K

atm = fluids.ATMOSPHERE_1976(Z=elevation) #z is meters
Patm = atm.P

#compressor values
Pgage = 50. #psi gage
Pgage= psi_to_Pa(Pgage) #Pa gage
Pabs = Pgage + Patm

eta = .7 #compressor effieciency

air = thermo.Mixture(['nitrogen', 'oxygen', 'argon'], Vfgs=[.7806, .21, .0094], T=ambient, P=Patm)
k = air.isentropic_exponent
D1 = air.rho
#temp gain in compressor
T2 = fluids.isentropic_T_rise_compression(P1=Patm, P2=Pabs, T1=ambient, k=k, eta=eta)


#recalc air density after compression
def air_density_calc(T, P):
    air.calculate(T=T, P=P)
    density = air.rho
    return density


D2 = air_density_calc(T=T2, P=Pabs)

# intercooler
# this will run to my intercooler module... so i need temp and flow rate
#intEff = .6
#Tinter = T2-(T2 - ambient)*intEff
Tnew = T2
Told = T2+1


#loop intercooler calcs since flowrate influences Tout from intercooler
while math.fabs(Told-Tnew) >1E-6:
    Told = Tnew
    D3 = air_density_calc(T=Tnew, P=Pabs) #need to include pressure drop here, should be manifold pressure
    massflowAir = flowVol * D3 #kg/s
    flowVolCooler=massflowAir/D2
    Tnew = cooler.get_Tout(T2, flowVolCooler, D2) + 273
    #print massflowAir
    print Tnew-273
    print Told-Tnew

Tinter = Tnew




#massflowAir = flowVol * D3
air_fuel=17.5
massflowFuel = massflowAir/air_fuel






power= massflowFuel/specFuel #watts
power= power/750

D_ratio= D3/D1
#print D_ratio
CFM_engine = flowVol * (3.281**3) * 60
CFM_cooler = CFM_engine *D3/D2
CFM_filter = CFM_engine *D3/D1




print T2-273
print Tinter-273

print power

print CFM_engine
print CFM_cooler
print CFM_filter






#print air
#print test


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
