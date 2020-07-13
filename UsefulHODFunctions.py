"""
July 9, 2020
"""

# import ares
import numpy as np
# import matplotlib.pyplot as pl
# import distpy

def getCsfrsData(path="../"):
    """
    Reads data file behroozi-2013-data-compilation/csfrs_new.dat to get data values for CSFR.
    
    Input: path (optional): path to behroozi data folder.
    
    Return: csfrs, [err1, err2]
        csfrs: [redshift, Log10(CSFR) (Msun/yr/Mpc^3)]
        [err1, err2]: [Err- (dex), Err+ (dex)]
    
    """
    
    text = path + "behroozi-2013-data-compilation/csfrs_new.dat"
    csfrs = np.transpose(np.loadtxt(text))

    logphi_ML = csfrs[1]
    err = csfrs[2]

    logphi_lo_tmp = logphi_ML - err   # log10 phi
    logphi_hi_tmp = logphi_ML + err   # log10 phi

    phi_lo = 10**logphi_lo_tmp
    phi_hi = 10**logphi_hi_tmp

    err1 = 10**logphi_ML - phi_lo
    err2 = phi_hi - 10**logphi_ML

    #example of how to plot
    #     pl.yscale('log')
    #     pl.errorbar(csfrs[0], 10**csfrs[1], yerr=[err1, err2], ls="", marker="o", label="Behroozi csfrs" )
    #     pl.ylabel('csfr $[M_{\odot}/yr/Mpc^3]$')
    #     pl.xlabel('Redshift')
    #     pl.title('Behroozi et al. 2013')
    #     pl.show()

    return csfrs, [err1, err2]
