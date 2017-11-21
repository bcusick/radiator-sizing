import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

 elif subtype == 'crossflow':
        def to_int(v, NTU, Cr):
            return (1. + NTU - v*v/(4.*Cr*NTU))*exp(-v*v/(4.*Cr*NTU))*v*iv(0, v)
        int_term = quad(to_int, 0, 2.*NTU*Cr**0.5, args=(NTU, Cr))[0]
        return 1./Cr - exp(-Cr*NTU)/(2.*(Cr*NTU)**2)*int_term
    elif subtype == 'crossflow approximate':
        return 1. - exp(1./Cr*NTU**0.22*(exp(-Cr*NTU**0.78) - 1.))
