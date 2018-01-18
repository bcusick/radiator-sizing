
###################
### rushed thru, needs a lot more work
###################


import math

from sympy.solvers import solve
from sympy import Symbol

x= Symbol('x')
y= Symbol('y')

def float_range(start, end, step):
    while start <= end:
        yield start
        start += step

length = 15 #ft
width = 8 #ft
height = 10 #ft
sq = length*width*1.66 # 2 levels, 2/3 of 2nd level
print sq

insThk = 3 #in
insThk *= 25.4 * 1E-3 #meters
length *= 12 * 25.4 * 1E-3 #meters
width*= 12 * 25.4 * 1E-3 #meters
height*= 12 * 25.4 * 1E-3 #meters



A = 2 * (length * width + length * height + width * height)
A1 = length * width + length * height # radiation gain area
A2 = A - A1 # the rest

k = .03 #foam

intTemp = 20 +273#K
extTemp = 40 +273#K
dT1 = extTemp - intTemp

#calc solar h

solar = 100
emm = .1 # approx aluminum 0.1, 0.3 worstcase
sbConst = 5.67E-8

windspeed = 5 #mph
windspeed /= 2.237 #m/s
#print windspeed
#convection neglecting for now
h = 10.45 - windspeed + 10 * math.sqrt(windspeed) #valid 2-20 m/s
#h = 1. #no wind
#print h
h2 = 1

RA1 = 1./h
RA2 = insThk/k
RA3 = 1./h2

#T1 = external wall temp (x), T2 = internal wall temp(y)
#emm * solar = (T1 - extTemp)/RA1 + (T1- T2)/RA2 + (emm * sbConst * T1**4) + (T2 - intTemp)/RA3 + (emm * sbConst * T2**4)
#f1 = (x - extTemp)/RA1 + (x- y)/RA2 + (emm * sbConst * x**4) + (y - intTemp)/RA3 + (emm * sbConst * y**4) - emm * solar

#T1 = external wall temp
f1 = (x - extTemp)/RA1 + (x- intTemp)/RA2 + (emm * sbConst * x**4) - (emm * solar)
#f1 = (x - extTemp)/RA1 + (x- (y))/RA2 + (emm * sbConst * x**4) + (y - intTemp)/RA3 - (emm * solar)
x>0
F=solve(f1)
print F

#while ((T - extTemp)/RA1 + (T- intTemp)/RA2 + emm * sbConst * T**4 - (emm * solar)) < 1E-10 :


'''


In = emm * solar
#print In

Out = emm * sbConst * T1**4

#print Out

conduction = (T1- intTemp)/RA2
#print conduction

convection = (T1 - extTemp)/RA1
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
print T1-273
print T2 -273

print math.fabs(Qtot/24.)
'''
'''
q = dT/ RA
Q = qA


print Q
print Q3


print T
'''
