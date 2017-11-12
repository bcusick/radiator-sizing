import math
import ht
import fluids

x = 1.0
y = 1.0
z = 1.0

for x in range(1, 9):
    x+=1
    for y in range(1,9):
        y+=1
        for z in range(1,9):

            ## initial variables and all dims in meters, frozen boost int000333
            coreHeight = x * 25.4/1000 #all dims in meters
            coreWidth = y * 25.4/1000
            coreThickness = z * 25.4/1000

            wallThickness = 0.5/1000

            finHeightAir= 6.0/1000
            finSpacingAir = 25.4/12.5/1000  #ref frozen spec



            finHeightCoolant= 2.0/1000
            finSpacingCoolant = 25.4/8.5/1000  #ref frozen spec


            ## calculate surface areas
            numberofBars = math.floor((coreHeight - wallThickness)/(finHeightAir + wallThickness + finHeightCoolant + wallThickness))
            numberCoolantPass = (coreThickness/finSpacingCoolant + 1) * numberofBars
            #numberCoolantPass = numberofBars
            #print numberCoolantPass
            numberAirPass = (coreWidth/finSpacingAir + 1) * numberofBars
            #print numberAirPass

            areaCoolant = numberCoolantPass * 2 * coreWidth * (finSpacingCoolant + finHeightCoolant)
            #areaCoolant = numberCoolantPass * 2 * coreWidth * (coreThickness + finHeightCoolant)
            areaAir =  numberAirPass * 2 * coreThickness * (finSpacingAir + finHeightAir)


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

            flowrateCoolant = 10 #GPM, volumetric
            flowrateCoolant = flowrateCoolant * 3.8 #LPM

            flowrateCoolant = flowrateCoolant /60/1000 # convert to m3/s
            massflowCoolant = flowrateCoolant *rho_Coolant



            flowrateAir = 450 #CFM, volumetric
            flowrateAir = flowrateAir / 60 / 35.3 #convert to m3/s
            massflowAir = flowrateAir *rho_Air

            tempAir = 210 # Celsius
            tempCoolant = 80 # Celsius




            ## fluids calcs
            #Coolant
            Dh_Coolant = 4 * (finHeightCoolant * finSpacingCoolant) / (2*(finHeightCoolant + finSpacingCoolant))

            tubeVelocity = flowrateCoolant/numberCoolantPass/(finHeightCoolant*finSpacingCoolant)
            #reynoldsCoolant = fluids.core.Reynolds(D=Dh_Coolant, rho=rho_Coolant, V=tubeVelocity, mu=mu_Coolant)
            reynoldsCoolant = 5000 #force turbulent
            prandltCoolant = fluids.core.Prandtl(Cp=C_Coolant , k=k_Coolant , mu=mu_Coolant, nu=None, rho=None, alpha=None)
            if reynoldsCoolant<2600:
                nusseltCoolant = ht.conv_internal.laminar_Q_const()
            else:
                nusseltCoolant = ht.conv_internal.turbulent_Dittus_Boelter(Re=reynoldsCoolant, Pr=prandltCoolant, heating=True)
            h_Coolant = nusseltCoolant * k_Coolant / Dh_Coolant


            #AIR
            Dh_Air = 4 * (finHeightAir * finSpacingAir) / (2*(finHeightAir + finSpacingAir))
            airVelocity = flowrateAir/numberAirPass/(finHeightAir*finSpacingAir)
            reynoldsAir = fluids.core.Reynolds(D=Dh_Air, rho=rho_Air, V=airVelocity, mu=mu_Air)
            reynoldsAir = 5000 # force turbulent

            prandltAir = fluids.core.Prandtl(Cp=C_Air , k=k_Air , mu=mu_Air, nu=None, rho=None, alpha=None)
            if reynoldsAir<2600:
                nusseltAir = ht.conv_internal.laminar_Q_const()
            else:
                nusseltAir = ht.conv_internal.turbulent_Dittus_Boelter(Re=reynoldsAir, Pr=prandltAir, heating=False)

            #nusseltAir =ht.conv_external.Nu_cylinder_Zukauskas(Re=reynoldsAir, Pr=prandltAir, Prw=None)

            #nusseltAir = 10  # manual overide for laminare flow

            h_Air = nusseltAir * k_Air / Dh_Air

            #calculate UA
            UA = 1/(h_Coolant*areaCoolant) + 1/(h_Air*areaAir)
            UA = 1/UA



            #NTU = ht.hx.effectiveness_NTU_method(mh=massflowCoolant, mc=massflowAir, Cph=C_Coolant, Cpc=C_Air, subtype='crossflow', Thi=tempCoolant, Tho=None, Tci=tempAir, Tco=None, UA=UA)
            NTU = ht.hx.effectiveness_NTU_method(mh=massflowAir, mc=massflowCoolant, Cph=C_Air, Cpc=C_Coolant, subtype='crossflow', Thi=tempAir, Tho=None, Tci=tempCoolant, Tco=None, UA=UA)
            #print NTU
            #print NTU['Q']

            Tout = NTU['Tho']
            totalDim = x + y + z
            output = [Tout, x, y, z, totalDim]
            if output[4]<21:
                if output[0]<95:
                    print output
            #print "Support power: "
            #print Power


            ####testing
