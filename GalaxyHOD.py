
#the start of my ares class

from .Halo import HaloPopulation
import numpy as np


class GalaxyHOD(HaloPopulation):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

        HaloPopulation.__init__(self, **kwargs)
        
    def LuminosityFunction(self, z, mags):
        pass    
        
        hmf = self.halos.tab_dndm
        
        # Should depend on SFR
    
    def StellarMassFunction(self, z, bins):


        pass    
        
    def SFRD(self, z):
        pass
        
    def SFR(self, z, Mh):    
        pass
        
            
    
if __name__ == '__main__':
    
    pop = GalaxyHOD()
    
    
    
    mags = np.arange(-25, -10)
    phi = pop.LuminosityFunction(6., mags)
    
    import matplotlib.pyplot as pl
    
    pl.semilogy(mags, phi)
    
    # Example of how to make a double power-law with PQ framework
    
    pars = {}
    pars['pq_func'] = 'dpl_evolN' # double power-law with evolution in norm
    pars['pq_func_var'] = 'Mh'
    pars['pq_func_var2'] = 'z'
    pars['pq_func_par0'] = 5e-4
    pars['pq_func_par1'] = 1e12
    pars['pq_func_par2'] = 1.
    pars['pq_func_par3'] = -0.6
    pars['pq_func_par4'] = 1e10
    pars['pq_func_par5'] = 0.88
    pars['pq_func_par6'] = 0.0   # default to no evol
    
    dpl = ares.phenom.ParameterizedQuantity(**pars)
    
    fstar = dpl(z=6., Mh=1e10)
    
    
        