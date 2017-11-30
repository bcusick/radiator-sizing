import math
import ht
import fluids

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

## initial variables and all dims in meters
name1 = 'crossflow - 2 pass'
Height1 = (16./2.) * 25.4/1000 #all dims in meters
Width1 = (16 * 2.) * 25.4/1000
Thickness1 = 2.0 * 25.4/1000
fanFlow1 = 1600   #CFM, volumetric, 1 Spal 12" low profile fan + 1 10" high perf. with thicker core, 1850 CFM
flowrateCoolant1 = 40 #GPM
tempAir1 = 50 # Celsius


name2 = 'DownFlow - Griffen Toyota'
Height2 = 21 * 25.4/1000 #all dims in meters
Width2 = 16 * 25.4/1000
Thickness2 = 1.5 * 25.4/1000
fanFlow2 = 1850   #CFM, volumetric, 1 Spal 12" low profile fan + 1 10" high perf. with thicker core, 1850 CFM
flowrateCoolant2 = 40 #GPM
tempAir2 = 50 # Celsius

name3 = 'DownFlow - Griffen Toyota - custom'
Height3 = 21. * 25.4/1000 #all dims in meters
Width3 = 16. * 25.4/1000
Thickness3 = 2.38 * 25.4/1000
fanFlow3 = 1850   #CFM, volumetric, 1 Spal 12" low profile fan + 1 10" high perf. with thicker core, 1850 CFM
flowrateCoolant3 = 40 #GPM
tempAir3 = 50 # Celsius

#CURRENT SETUP
name4 = 'crossflow - 1 pass, 20  GPM'
Height4 = 16 * 25.4/1000 #all dims in meters
Width4 = 21 * 25.4/1000
Thickness4 = 1.25 * 25.4/1000
fanFlow4 = 1600.   #CFM, volumetric, one 16" Spal medium profile fan, 1600 CFM
flowrateCoolant4 = 20 #GPM
tempAir4 = 50 # Celsius

name5 = 'DownFlow - Griffen Toyota - custom - 30C'
Height5 = 21. * 25.4/1000 #all dims in meters
Width5 = 16. * 25.4/1000
Thickness5 = 1.5 * 25.4/1000
fanFlow5 = 1850   #CFM, volumetric, 1 Spal 12" low profile fan + 1 10" high perf. with thicker core, 1850 CFM
flowrateCoolant5 = 40 #GPM
tempAir5 = 30 # Celsius

#constants

tempCoolant = 95 # Celsius

finHeight= 10.0/1000
finSpacing = 1.7/1000  #ref 1.59

tubeWall = .5/1000
tubeHeight = 2.0/1000 #outer dimension

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


def radCalc(coreHeight, coreWidth, coreThickness, fanFlow, flowrateCoolant, tempAir):

    ## operating conditions
    fanFlow = fanFlow / 60. / 35.3 #convert to m3/s
    flowrateCoolant = flowrateCoolant * 3.8 #LPM
    flowrateCoolant = flowrateCoolant /60./1000. # convert to m3/s
    massflowCoolant = flowrateCoolant *rho_Coolant

    finperRow = coreWidth/finSpacing

    ## calculate surface areas
    numberTubes = math.floor(coreHeight / finHeight - 1)
    numberAirPass = coreWidth / finSpacing * (numberTubes + 1)
    tubeInnerH = tubeHeight - 2 * tubeWall
    tubeInnerW = coreThickness - 2 * tubeWall
    areaCoolant = numberTubes * 2 * coreWidth * (tubeInnerW + tubeInnerH)
    areaAir =  numberAirPass * 2 * coreThickness * (finSpacing + finHeight)

    ## fluids calcs
    #Coolant
    Dh_Coolant = 4 * (tubeInnerH * tubeInnerW) / (2*(tubeInnerH + tubeInnerW))
    tubeVelocity = flowrateCoolant/numberTubes/(tubeInnerH*tubeInnerW)
    reynoldsCoolant = fluids.core.Reynolds(D=Dh_Coolant, rho=rho_Coolant, V=tubeVelocity, mu=mu_Coolant)
    prandltCoolant = fluids.core.Prandtl(Cp=C_Coolant , k=k_Coolant , mu=mu_Coolant, nu=None, rho=None, alpha=None)
    nusseltCoolant = ht.conv_internal.turbulent_Dittus_Boelter(Re=reynoldsCoolant, Pr=prandltCoolant, heating=False)
    h_Coolant = nusseltCoolant * k_Coolant / Dh_Coolant

    #setup arrays for data.
    temp = []
    power = []
    rateAir =[]

    for speed in range(0, 61):
        travelSpeed = speed
        travelSpeed = travelSpeed/3600.
        travelSpeed = travelSpeed * 1609 # convert to m/s
        flowrateAir = travelSpeed * coreHeight * coreWidth
        flowrateAir *= 0.75  #safety factor accounts for radiator blockage

        if fanFlow > flowrateAir:
            flowrateAir = fanFlow

        massflowAir = flowrateAir *rho_Air

        ## fluids calcs
        #AIR
        Dh_Air = 4 * (finHeight * finSpacing) / (2*(finHeight + finSpacing))
        airVelocity = flowrateAir/numberAirPass/(finHeight*finSpacing)
        reynoldsAir = fluids.core.Reynolds(D=Dh_Air, rho=rho_Air, V=airVelocity, mu=mu_Air)
        reynoldsAir = 5000
        prandltAir = fluids.core.Prandtl(Cp=C_Air , k=k_Air , mu=mu_Air, nu=None, rho=None, alpha=None)
        if reynoldsAir<5000:
            nusseltAir = ht.conv_internal.laminar_Q_const()
        else:
            nusseltAir = ht.conv_internal.turbulent_Dittus_Boelter(Re=reynoldsAir, Pr=prandltAir, heating=True)
        #nusseltAir = 10  # manual overide for laminare flow

        h_Air = nusseltAir * k_Air / Dh_Air
        hRatio = h_Coolant/h_Air

        UA = 1/(h_Coolant*areaCoolant) + 1/(h_Air*areaAir)
        UA = 1/UA

        NTU = ht.hx.effectiveness_NTU_method(mh=massflowCoolant, mc=massflowAir, Cph=C_Coolant, Cpc=C_Air, subtype='crossflow', Thi=tempCoolant, Tho=None, Tci=tempAir, Tco=None, UA=UA)
        #NTU = ht.hx.effectiveness_NTU_method(mh=massflowAir, mc=massflowCoolant, Cph=C_Air, Cpc=C_Coolant, subtype='crossflow', Thi=tempAir, Tho=None, Tci=tempCoolant, Tco=None, UA=UA)
        Power = (NTU['Q']/1000) /0.3/.75
        #Power = (NTU['Tho'])

        power.append(Power) #fill data arrays
        rateAir.append(speed)

    output = pd.Series(power, index=rateAir)
    return output

rad1 = radCalc(Height1, Width1, Thickness1, fanFlow1, flowrateCoolant1, tempAir1)
rad2 = radCalc(Height2, Width2, Thickness2, fanFlow2, flowrateCoolant2, tempAir2)
rad3 = radCalc(Height3, Width3, Thickness3, fanFlow3, flowrateCoolant3, tempAir3)
rad4 = radCalc(Height4, Width4, Thickness4, fanFlow4, flowrateCoolant4, tempAir4)
rad5 = radCalc(Height5, Width5, Thickness5, fanFlow5, flowrateCoolant5, tempAir5)

dataSet = pd.DataFrame({'{0} - {1}C'.format(name1, tempAir1)            : rad1,
                        '{0} - {1}C'.format(name2, tempAir2)            : rad2,
                        '{0} - {1}C'.format(name3, tempAir3)            : rad3,
                        '{0} - {1}C'.format(name4, tempAir4)            : rad4,
                        '{0} - {1}C'.format(name5, tempAir5)            : rad5})
print dataSet

dataSet.plot()
plt.xlabel('MPH')
plt.ylabel('HP supported')
plt.title('Radiator Comparison')
ymin, ymax = plt.ylim()
plt.text(0.01, ymin + 1, 'Th={0}, Tc={1}'.format(tempCoolant, tempAir1), size=8)
plt.grid(1)
plt.show()

#print dataSet
####testing
