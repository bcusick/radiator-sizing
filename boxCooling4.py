
###################
### rushed thru, needs a lot more work
###################


import math
#truck pod
length = 8 #ft
width = 5 #ft
height = 3 #ft

sq = length * width
print sq

insThk = 0.5 #in
insThk *= 25.4 * 1E-3 #meters
length *= 12 * 25.4 * 1E-3 #meters
width*= 12 * 25.4 * 1E-3 #meters
height*= 12 * 25.4 * 1E-3 #meters



A = 2 * (length * width + length * height + width * height)
A1 = length * width + length * height # radiation gain area
A2 = A - A1 # the rest

k = .03 #foam

intTemp = 30 +273#K
extTemp = 40 +273#K
dT1 = extTemp - intTemp

#calc solar h

solar = 1000
emm = .3 # approx aluminum 0.1, 0.3 worstcase
sbConst = 5.67E-8
'''
T = math.pow((solar / sbConst), (1/4.))
T = T - 273
dT2 = T - intTemp
'''
windspeed = 5 #mph
windspeed /= 2.237 #m/s
#print windspeed
#convection neglecting for now
h = 10.45 - windspeed + 10 * math.sqrt(windspeed) #valid 2-20 m/s
h = 1. #no wind
#print h


RA1 = 1./h
RA2 = insThk/k

#emm * solar = (T - extTemp)/RA1 + (T- intTemp)/RA2 + emm * sbConst * T**4




T= 0
while ((T - extTemp)/RA1 + (T- intTemp)/RA2 + emm * sbConst * T**4 - (emm * solar)) < 1E-10 :
    T+=1E-3
    #print T-273



In = emm * solar
#print In

Out = emm * sbConst * T**4

#print Out

conduction = (T- intTemp)/RA2
#print conduction

convection = (T - extTemp)/RA1
#print convection

#print Out + conduction + convection

Qin = conduction * A1
#Qremain = dT1 / ((RA2 / A2) + (RA1 / A2))
Qremain = dT1 / (RA2 + RA1) * A2
Qtot = Qin + Qremain
print Qin
print Qremain
print Qtot


T2 = extTemp - Qremain/(h *A2)

#print dT1
print T-273
print T2 -273

print math.fabs(Qtot/24.)

'''
q = dT/ RA
Q = qA


print Q
print Q3


print T
'''
