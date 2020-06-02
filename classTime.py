#just organzing things better in a python file


import numpy as np
# from ..util import labels
# from matplotlib import cm
import matplotlib.pyplot as pl
# from .Halo import HaloPopulation



"""
Gonna need to change how we acess:
pop_halo = ares.populations.HaloPopulation()
data = ares.analysis.GalaxyPopulation() #for lit values

- how to do plots
- what do they return
"""


"""
LF
"""

def LF_linearLog(z, pop_halo, const):
    
    c = const
    i = np.argmin(np.abs(z - pop_halo.halos.tab_z))
    
    LF = (np.log(10)*pop_halo.halos.tab_M)/2.5 * pop_halo.halos.tab_dndm[i, :]
    
    return LF


# z = [4, 6, 10]

# fig, axs = pl.subplots(1, len(z), figsize=(20, 5))

# obslf = ares.analysis.GalaxyPopulation() #for lit values

# for i, z in enumerate(z):
   
#     obslf.Plot(z=z, round_z=0.2, ax=axs[i]) 
# #     lf = pop.LuminosityFunction(z, MUV)
# #     axs[i].semilogy(MUV, lf)

#     for c in [1e-5, 1e-4, 3e-4, 1e-3, 1e-1]:
#         lf = LF_linearLog(z, pop_halo, c)

# #         MUV = np.linspace(-24, -10, num=len(lf))
#         MUV = -2.5*np.log10(c*pop_halo.halos.tab_M)

#         axs[i].semilogy(MUV, lf, label='c = %.e' %c)
        
#     axs[i].set_title("z = %i" %z)
#     axs[i].legend()
#     axs[i].set(xlabel='abs mag', ylabel='# of galaxies / $ mag~(cMpc)^3$')
#     axs[i].set_ylim(1e-15, 1e2)
# #     axs[i].set_xlim(-35, 0)

# pl.show()

"""
SMF
"""

#derivative of log10( m ) wrt M
def dlogm_dM(pop_halo, N, M_1, beta, gamma, mM_ratio):
    
    dydx = -1* ((gamma-1)*(pop_halo.halos.tab_M/M_1)**(gamma+beta) - beta - 1) / (np.log(10)*pop_halo.halos.tab_M*((pop_halo.halos.tab_M/M_1)**(gamma+beta) + 1))

    return dydx


#double power law
def SMF_Moster2010(z, pop_halo, fitParameters):

	logM_0, mu, N_0, nu, gamma_0, gamma_1, beta_0, beta_1 = fitParameters

	# Redshift-dependent parameterizations
	N = N_0 * (z + 1)**nu
    M_1 = 10**(logM_0*(z+1)**mu)
    beta = beta_1*z+beta_0
    gamma = gamma_0*(z + 1)**gamma_1

    
    k = np.argmin(np.abs(z - pop_halo.halos.tab_z))
    
    mM_ratio = np.log10( 2*N / ( (pop_halo.halos.tab_M/M_1)**(-beta) + (pop_halo.halos.tab_M/M_1)**(gamma) ) )#equ 2
    
    """
    tab_dndm (halo) -> dndlog(m) (SM)
    need: tab_dndm / d(log(ratio)/dM
    """
    
    SMF = pop_halo.halos.tab_dndm[k, :] / dlogm_dM(pop_halo, N, M_1, beta, gamma, mM_ratio) #dn/dM / d(log10(m))/dM

    #using equ 2 to get the new stellar masses
    Sm = 10**(mM_ratio + np.log10(pop_halo.halos.tab_M))

    return SMF, Sm, mM_ratio


def SMF(z):

	#check if new parameters are used else use default - probably want to change these

	#From Moster2010, table 7
	logM_0 = 11.88 #(0.01)
	mu = 0.019 #(0.002)
	N_0 = 0.0282 #(0.0003)
	nu = -0.72 #(0.06)
	gamma_0 = 0.556 #0.001
	gamma_1 = -0.26 #(0.05)
	beta_0 = 1.06 #(0.06)
	beta_1 = 0.17 #(0.12)

	fitParams = [logM_0, mu, N_0, nu, gamma_0, gamma_1, beta_0, beta_1]

    #plot lit values
#     data.PlotSMF(z=z, round_z=0.2, ax=axs[i])
    
    SMF, Sm, r = SMF_Moster2010(z, pop_halo, fitParams)

#     #get z index for halo mass array
#     zz = np.argmin(np.abs(z - pop_halo.halos.tab_z))
#     Sm_off = np.linspace(10**8.5, 10**12.5, num=len(pop_halo.halos.tab_dndm[zz, :]))

#     #plotting
#     axs[i].loglog(Sm, SMF, label='Fit')
    
#     #plotting just offset HMF for comparison
#     axs[i].loglog(Sm_off, pop_halo.halos.tab_dndm[zz, :]*0.05, ls = "--", label='hmf 0.05 offset')

#     axs[i].set_title("z = %.2f" %z)
#     axs[i].set(xlabel='m / M$_o$', ylabel='# of galaxies / $ (cMpc)^3$ / dex')
#     axs[i].set_ylim(1e-6, 1e0)
#     axs[i].set_xlim(1e8, )
# #     axs[i].axvline(10**(8.7), color="purple", label="Their lower limit-ish", ls=":")
#     axs[i].legend()

# 	pl.show()