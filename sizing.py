
import ht
import math
import fluids


## initial variables and all dims in meters
coreHeight = 18 * 25.4/1000 #all dims in meters
coreWidth = 23 * 25.4/1000
coreThickness = 1.25 * 25.4/1000


finHeight= 11.9/1000
finSpacing = 1.59/1000
finperRow = coreWidth/finSpacing
print finperRow

tubeWall = .001/1000
tubeHeight = 1.56/1000 #outer dimension

##fluid constants
##coolant to 50-50 glycol/water

k_Coolant = 0.415 # W/(m K), thermal conductivity
C_Coolant = 3681.9 # J/(kg K), Specific Heat
rho_Coolant = 1015.6 # kg/m3, Density
mu_Coolant = 0.000744 # Pa s, Dynamic Viscosity

k_Air = 0.02664 # W/(m K), thermal conductivity
C_Air = 1004.16 # J/(kg K), Specific Heat
rho_Air = 1.13731 # kg/m3, Density
mu_Air = 0.00001912 # Pa s, Dynamic Viscosity


## operating conditions

flowrateCoolant = 2 #GPM
flowrateCoolant = flowrateCoolant * 3.8/60/1000 # convert to m3/s
massflowCoolant = flowrateCoolant *rho_Coolant



flowrateAir = 2000 #CFM
flowrateAir = flowrateAir / 60 / 35.3 #convert to m3/s
print flowrateAir
#travelSpeed = 20.0 #mph
#travelSpeed = travelSpeed/3600
#travelSpeed = travelSpeed * 1609 # convert to m/s
#flowrateAir = travelSpeed * coreHeight * coreWidth
#print flowrateAir
massflowAir = flowrateAir *rho_Air

tempAir = 40 # Celsius
tempCoolant = 100 # Celsius


## calculate surface areas
numberTubes = round(coreHeight / finHeight - 1)
numberAirPass = coreWidth / finSpacing * (numberTubes + 1)
tubeInnerH = tubeHeight - 2 * tubeWall
tubeInnerW = coreThickness - 2 * tubeWall
areaCoolant = numberTubes * 2 * coreWidth * (tubeInnerW + tubeInnerH)
areaAir =  numberAirPass * 2 * coreThickness * (finSpacing + finHeight)
print areaAir
print areaCoolant

## fluids calcs
#Coolant
Dh_Coolant = 4 * (tubeInnerH * tubeInnerW) / (2*(tubeInnerH + tubeInnerW))
tubeVelocity = flowrateCoolant/numberTubes/(tubeInnerH*tubeInnerW)
reynoldsCoolant = fluids.core.Reynolds(D=Dh_Coolant, rho=rho_Coolant, V=tubeVelocity, mu=mu_Coolant)
prandltCoolant = fluids.core.Prandtl(Cp=C_Coolant , k=k_Coolant , mu=mu_Coolant, nu=None, rho=None, alpha=None)
nusseltCoolant = ht.conv_internal.turbulent_Dittus_Boelter(Re=reynoldsCoolant, Pr=prandltCoolant, heating=False)
h_Coolant = nusseltCoolant * k_Coolant / Dh_Coolant
print '------------------------'

#AIR
Dh_Air = 4 * (finHeight * finSpacing) / (2*(finHeight + finSpacing))
airVelocity = flowrateAir/numberAirPass/(finHeight*finSpacing)
reynoldsAir = fluids.core.Reynolds(D=Dh_Air, rho=rho_Air, V=airVelocity, mu=mu_Air)
prandltAir = fluids.core.Prandtl(Cp=C_Air , k=k_Air , mu=mu_Air, nu=None, rho=None, alpha=None)
nusseltAir = ht.conv_internal.turbulent_Dittus_Boelter(Re=reynoldsAir, Pr=prandltAir, heating=False)
nusseltAir = 3  # manual overide for laminare flow
h_Air = nusseltAir * k_Air / Dh_Air

#calculate UA
UA = 1/(h_Coolant*areaCoolant) + 1/(finperRow*h_Air*areaAir)
UA = 1/UA

print UA

print(ht.hx.effectiveness_NTU_method(mh=massflowCoolant, mc=massflowAir, Cph=C_Coolant, Cpc=C_Air, subtype='crossflow', Thi=tempCoolant, Tho=None, Tci=tempAir, Tco=None, UA=UA))


####testing