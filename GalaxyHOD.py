
#the start of my ares class
import ares #importing this for testing for now
from ares.populations.Halo import HaloPopulation
import numpy as np
from scipy.interpolate import interp1d


class GalaxyHOD(HaloPopulation):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

        HaloPopulation.__init__(self, **kwargs)
        
    def LuminosityFunction(self, z, mags):
        """
        Reconstructed luminosity function from a simple model of L = c*HaloMadd
        
        Parameters
        ----------
        z : int, float
            Redshift. Currently does not interpolate between values in halos.tab_z if necessary.
        mags : bool
            If True, x-values will be in absolute (AB) magnitudes
        
        Returns
        -------
        Number density.
        
        """

        #get halo mass function and array of halo masses
        hmf = self.halos.tab_dndm
        haloMass = self.halos.tab_M

        pars = {}
        pars['pq_func'] = 'linear' # double power-law with evolution in norm
        pars['pq_func_var'] = 'z'
        pars['pq_func_par0'] = 3e-4
        pars['pq_func_par1'] = 0
        pars['pq_func_par2'] = 0

        #LF loglinear models
        c = ares.phenom.ParameterizedQuantity(**pars) #really just a constant
        k = np.argmin(np.abs(z - self.halos.tab_z))
        
        LF = (np.log(10)*haloMass)/2.5 * hmf[k, :]
        MUV = -2.5*np.log10(c*haloMass)

        #check if requested magnitudes are in MUV, else interpolate LF function
        result =  all(elem in MUV for elem in mags)

        if result:
            #slice list to get the values requested
            findMags = np.array([elem in mags for elem in MUV])
            NumDensity = LF[findMags]
        else:
            print("Interpolating")
            f = interp1d(MUV, LF, kind='cubic')    

            NumDensity = f(mags)

        return NumDensity

    def _dlogm_dM(self, N, M_1, beta, gamma):
        
        dydx = -1* ((gamma-1)*(self.halos.tab_M/M_1)**(gamma+beta) - beta - 1) / (np.log(10)*self.halos.tab_M*((self.halos.tab_M/M_1)**(gamma+beta) + 1))

        return dydx

    
    def StellarMassFunction(self, z, bins):

        #get halo mass function and array of halo masses
        hmf = self.halos.tab_dndm
        haloMass = self.halos.tab_M

        #From Moster2010, table 7
        logM_0 = 11.88 #(0.01)
        mu = 0.019 #(0.002)
        N_0 = 0.0282 #(0.0003)
        nu = -0.72 #(0.06)
        gamma_0 = 0.556 #0.001
        gamma_1 = -0.26 #(0.05)
        beta_0 = 1.06 #(0.06)
        beta_1 = 0.17 #(0.12)

        parsB = {}
        parsB['pq_func'] = 'linear' # double power-law with evolution in norm
        parsB['pq_func_var'] = 'z'
        parsB['pq_func_par0'] = beta_0
        parsB['pq_func_par1'] = 0
        parsB['pq_func_par2'] = beta_1

        parsN = {}
        parsN['pq_func'] = 'pl' # double power-law with evolution in norm
        parsN['pq_func_var'] = 'z+1'
        parsN['pq_func_par0'] = N_0
        parsN['pq_func_par1'] = 1.0
        parsN['pq_func_par2'] = nu

        parsG = {}
        parsG['pq_func'] = 'pl' # double power-law with evolution in norm
        parsG['pq_func_var'] = 'z+1'
        parsG['pq_func_par0'] = gamma_0
        parsG['pq_func_par1'] = 1.0
        parsG['pq_func_par2'] = gamma_1

        parsM = {}
        parsM['pq_func'] = 'pl_10' # double power-law with evolution in norm
        parsM['pq_func_var'] = 'z+1'
        parsM['pq_func_par0'] = logM_0
        parsM['pq_func_par1'] = 1.0
        parsM['pq_func_par2'] = mu


        N = ares.phenom.ParameterizedQuantity(**parsN) #N_0 * (z + 1)**nu #PL
        M_1 = ares.phenom.ParameterizedQuantity(**parsM) #10**(logM_0*(z+1)**mu)
        beta = ares.phenom.ParameterizedQuantity(**parsB) #beta_1*z+beta_0 #linear
        gamma = ares.phenom.ParameterizedQuantity(**parsG) #gamma_0*(z + 1)**gamma_1 #PL


        k = np.argmin(np.abs(z - pop_halo.halos.tab_z))
        
        mM_ratio = np.log10( 2*N / ( (haloMass/M_1)**(-beta) + (haloMass/M_1)**(gamma) ) )#equ 2

        
        SMF = hmf[k, :] / _dlogm_dM(pop_halo, N, M_1, beta, gamma) #dn/dM / d(log10(m))/dM
        StellarMass = 10**(mM_ratio + np.log10(haloMass))


        #check if requested magnitudes are in MUV, else interpolate LF function
        result =  all(elem in StellarMass for elem in bins)

        if result:
            #slice list to get the values requested
            findMass = np.array([elem in bins for elem in StellarMass])
            phi = SMF[findMass]           
        else:
            print("Interpolating")
            f = interp1d(StellarMass, SMF, kind='cubic')    

            phi = f(bins)


        return phi    
        
    def SFRD(self, z):
        pass
        
    def SFR(self, z, Mh):    
        pass
        
            
    
if __name__ == '__main__':
    
    pop = GalaxyHOD()
    
    
    
    mags = np.arange(-25, -10)
    phi = pop.LuminosityFunction(6., mags)
    
    import matplotlib.pyplot as pl
    
    # pl.semilogy(mags, phi, marker="o")
    # pl.show()

    bins = np.logspace(8.5, 11.5)
    phi = pop.StellarMassFunction(1, bins)
    pl.loglog(bins, phi, marker="o")
    pl.show()
    
    # # Example of how to make a double power-law with PQ framework
    
    # pars = {}
    # pars['pq_func'] = 'dpl_evolN' # double power-law with evolution in norm
    # pars['pq_func_var'] = 'Mh'
    # pars['pq_func_var2'] = 'z'
    # pars['pq_func_par0'] = 5e-4
    # pars['pq_func_par1'] = 1e12
    # pars['pq_func_par2'] = 1.
    # pars['pq_func_par3'] = -0.6
    # pars['pq_func_par4'] = 1e10
    # pars['pq_func_par5'] = 0.88
    # pars['pq_func_par6'] = 0.0   # default to no evol
    
    # dpl = ares.phenom.ParameterizedQuantity(**pars)
    
    # fstar = dpl(z=6., Mh=1e10)
    
    
        