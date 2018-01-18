
###################
### rushed thru, needs a lot more work
###################


import math

length = 12. #ft
width = 8. #ft
height = 7. #ft

insThk = 1. #in
insThk *= 25.4 * 1E-3 #meters
length *= 12 * 25.4 * 1E-3 #meters
width*= 12 * 25.4 * 1E-3 #meters
height*= 12 * 25.4 * 1E-3 #meters



A = 2 * (length * width + length * height + width * height)
A1 = length * width + length * height # radiation gain area
A2 = A - A1 # the rest

k = .03 #foam

intTemp = 20 #C
extTemp = 40 #C
dT1 = extTemp - intTemp



windspeed = 5 #mph
windspeed /= 2.237 #m/s

#convection neglecting for now
h = 10.45 - windspeed + 10 * math.sqrt(windspeed)
h=1.
#print h


R2 = 1/(h * A2) + insThk/(k * A2)

Q = dT1 / R2

print Q





T2 = extTemp - Q/(A2 * h)
print T2
print h
