import math
import ht
import fluids

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

## initial variables and all dims in meters
#rad1 - crossflow - 2 pass
Height1 = (17.5/2.) * 25.4/1000 #all dims in meters
Width1 = 40 * 25.4/1000
Thickness1 = 2.0 * 25.4/1000
fanFlow1 = 1850   #CFM, volumetric, 1 Spal 12" low profile fan + 1 10" high perf. with thicker core
flowrateCoolant1 = 40 #GPM

#rad2 - DownFlow
Height2 = 21 * 25.4/1000 #all dims in meters
Width2 = 17.5 * 25.4/1000
Thickness2 = 2.0 * 25.4/1000
fanFlow2 = 1850   #CFM, volumetric, 1 Spal 12" low profile fan + 1 10" high perf. with thicker core
flowrateCoolant2 = 40 #GPM

#rad3 - crossflow - 1 pass
Height3 = 16 * 25.4/1000 #all dims in meters
Width3 = 21 * 25.4/1000
Thickness3 = 1.25 * 25.4/1000
fanFlow3 = 1600.   #CFM, volumetric, one 16" Spal low profile fan
flowrateCoolant3 = 40 #GPM

#CURRENT SETUP
#rad4 - crossflow - 1 pass, 20  GPM
Height4 = 16 * 25.4/1000 #all dims in meters
Width4 = 21 * 25.4/1000
Thickness4 = 1.25 * 25.4/1000
fanFlow4 = 1600.   #CFM, volumetric, one 16" Spal low profile fan
flowrateCoolant4 = 5 #GPM

#constants

tempAir = 30 # Celsius
tempCoolant = 105 # Celsius

finHeight= 10.0/1000
finSpacing = 1.7/1000  #ref 1.59

#print finperRow

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


def radCalc(coreHeight, coreWidth, coreThickness, fanFlow, flowrateCoolant):

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
        #flowrateAir *= 0.85

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
        if reynoldsAir<2600:
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
        Power = (NTU['Q']/1000 -16) *3/.75
        #Power = (NTU['Tho'])

        power.append(Power)
        rateAir.append(speed)

    output = pd.Series(power, index=rateAir)
    return output

rad1 = radCalc(Height1, Width1, Thickness1, fanFlow1, flowrateCoolant1)
rad2 = radCalc(Height2, Width2, Thickness2, fanFlow2, flowrateCoolant2)
rad3 = radCalc(Height3, Width3, Thickness3, fanFlow3, flowrateCoolant3)
rad4 = radCalc(Height4, Width4, Thickness4, fanFlow4, flowrateCoolant4)

dataSet = pd.DataFrame({'Cross - 2pass'         : rad1,
                        'Down'                  : rad2,
                        'Cross - 1pass'         : rad3,
                        'Cross - 1pass - 20GPM' : rad4})
dataSet.plot()
plt.show()

#print dataSet
####testing
