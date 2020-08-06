# -*- coding: utf-8 -*-
"""

"""

import ares
import numpy as np
import matplotlib.pyplot as pl
import distpy

# Independent variables
redshifts = np.sort(np.array([0.875, 1.125, 1.75, 2.25, 2.75]))

Ms = np.linspace(7, 12, 60)

# blob 1
blob_n1 = ['galaxy_smf_sf']
blob_i1 = [('z', redshifts), ('logbins', Ms)]
blob_f1 = ['StellarMassFunction']

blob_pars = \
{
 'blob_names': [blob_n1, ['galaxy_smf']],
 'blob_ivars': [blob_i1, blob_i1],
 'blob_funcs': [blob_f1, blob_f1],
 'blob_kwargs': [[{'sf_type': 'smf_sf'}], [None]]
}

#define the parameters that remain unchanged
base_pars = ares.util.ParameterBundle('emma:model1')
base_pars.update(blob_pars)#, pop_sf_type='sf')
base_pars.update({'debug':True})

blob_parsQ = \
{
 'blob_names': [['galaxy_smf_Q']],
 'blob_ivars': [blob_i1],
 'blob_funcs': [blob_f1],
 'blob_kwargs': [[{'sf_type': 'smf_q'}]]
}

base_parsQ = ares.util.ParameterBundle('emma:model1')
base_parsQ.update(blob_parsQ)
base_parsQ.update({'debug':True})

free_pars = \
[
     #A
    'pq_func_par0[7]',
    'pq_func_par1[7]',
    'pq_func_par2[7]', 

    #B
    'pq_func_par0[8]',
    'pq_func_par1[8]', 
    'pq_func_par2[8]',

    #C
    'pq_func_par0[9]',
    #D
    'pq_func_par0[10]', 

]

is_log = [False, False, False, False, False, False, False, False]

from distpy.distribution import UniformDistribution
from distpy.distribution import DistributionSet

ps = DistributionSet()
#total must be negative
ps.add_distribution(UniformDistribution(-4, 4), 'pq_func_par0[7]')
ps.add_distribution(UniformDistribution(0, 3.5),  'pq_func_par1[7]')
ps.add_distribution(UniformDistribution(-5.0, 1.0),   'pq_func_par2[7]')

#(-8, -12)
ps.add_distribution(UniformDistribution(-13.0, -7.0),  'pq_func_par0[8]')
ps.add_distribution(UniformDistribution(-1.0, 3.5),   'pq_func_par1[8]')
ps.add_distribution(UniformDistribution(-4.0, 3.5),  'pq_func_par2[8]')

ps.add_distribution(UniformDistribution(2.0, 8.0),   'pq_func_par0[9]')

ps.add_distribution(UniformDistribution(1.00, 6.0),  'pq_func_par0[10]')


guesses = \
{
     #A
	'pq_func_par0[7]': -1, #const
	'pq_func_par1[7]': 0.875, #offset
	'pq_func_par2[7]': -0.8, #m

    #B
	'pq_func_par0[8]': -10.84, #const
	'pq_func_par1[8]': 1.75, #offset
	'pq_func_par2[8]': 0.902857, #m

    #C
	'pq_func_par0[9]': 3.0, #const
    #D
	'pq_func_par0[10]': 2.0, #const
}

# Initialize a fitter object and give it the data to be fit
fitter_smf = ares.inference.FitGalaxyPopulation(**base_pars)

fitter_smf.include.append('smf_sf')

# The data can also be provided more explicitly
fitter_smf.data = 'tomczak2014'#,  'mortlock2011', 'moustakas2013', 'marchesini2009_10'

#Q
fitter_smfQ = ares.inference.FitGalaxyPopulation(**base_parsQ)

fitter_smfQ.include.append('smf_q')
# The data can also be provided more explicitly
fitter_smfQ.data = 'tomczak2014'

fitter = ares.inference.ModelFit(**base_parsQ)
fitter.add_fitter(fitter_smfQ)
fitter.add_fitter(fitter_smf)

# Establish the object to which we'll pass parameters
from ares.populations.GalaxyHOD import GalaxyHOD
fitter.simulator = GalaxyHOD

fitter.save_hmf = True  # cache HMF for a speed-up!
fitter.save_psm = True  # cache source SED model (e.g., BPASS, S99)

# Setting this flag to False will make ARES generate new files for each checkpoint.
fitter.checkpoint_append = False

fitter.parameters = free_pars
fitter.is_log = is_log
fitter.prior_set = ps

# In general, the more the merrier (~hundreds)
fitter.nwalkers = 50

fitter.jitter = [0.1] * len(fitter.parameters)

fitter.guesses = guesses

#home = os.environ['HOME']
#dt_string = datetime.now().strftime("%d_%m_%H-%M") + "_" + str(zLim_low) + "-" + str(zLim_high)
#title = home + "/scratch/jobs/MCMC_files/smf_" + dt_string

# Run the thing
#fitter.run(title, burn=BurnIn, steps=StepCount, save_freq=5, clobber=True)

fitter.run('MCMC_files/fract_test1SQ', burn=5, steps=80, save_freq=2, clobber=True)
