import math
import ht
import fluids
import thermo

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
elevation = 8000 # ft
elevation = ft_to_m(elevation)
ambient = 25

atm = fluids.ATMOSPHERE_1976(Z=elevation) #z is meters
Patm = atm.P

#compressor values
Pgage = 30. #psi gage
Pgage= psi_to_Pa(Pgage) #Pa gage
Pabs = Pgage + Patm

eta = .7 #compressor effieciency

air = thermo.Mixture(['nitrogen', 'oxygen', 'argon'], Vfgs=[.7806, .21, .0094], T=ambient+273, P=Patm)
k = air.isentropic_exponent
print air
print air.rho
#temp gain in compressor
T2 = fluids.isentropic_T_rise_compression(P1=Patm, P2=Pabs, T1=273+ambient, k=k, eta=eta)
print T2-273

#recalc air density after compression
air.calculate(T=T2, P=Pabs)
print air
density = air.rho
print density

# intercooler
# this will run to my intercooler module... so i need temp and flow rate
intEff = .6
Tinter = (T2-273)-(((T2-273) - ambient)*intEff)
print Tinter
#now recalc density
air.calculate(T=Tinter+273, P=Pabs) #need to include pressure drop here, should be manifold pressure

print air
density = air.rho
print density








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
