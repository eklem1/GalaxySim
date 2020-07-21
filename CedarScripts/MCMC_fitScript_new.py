"""
Emma Klemets
Affiliation: McGill University
Created on: June 24, 2020

Description: Running MCMC of the SMF to fit the 8 parameters using a GalaxyHOD model.s
Takes input as:
    python file.py NumberOfWalkers BurnIn Steps LowerZLimit HigherZLimit
"""

import ares
import numpy as np
#import matplotlib.pyplot as pl
#import distpy
import sys, os
from datetime import datetime

from distpy.distribution import UniformDistribution
from distpy.distribution import DistributionSet

if len(sys.argv) == 6:
    NumWalkers = int(sys.argv[1])
    BurnIn = int(sys.argv[2])
    StepCount = int(sys.argv[3])
    zLim_low = float(sys.argv[4])
    zLim_high = float(sys.argv[5])
else:
    NumWalkers = 96
    BurnIn = 20
    StepCount = 100
    zLim_low = 0
    zLim_high = 4
    
print("Using {0} walkers, {1} burn in, {2} steps, z limit {3}-{4}.".format(NumWalkers, BurnIn, StepCount, zLim_low, zLim_high) )

# Independent variables
redshiftTotal = np.sort(np.array([0.35, 0.875, 1.125, 1.75, 2.25, 2.75, 1.65, 2.5, 3.5, 0.10165, 0.25, 0.45, 0.575, 0.725, 0.9]))

mask = [zLim_low <= i <= zLim_high for i in redshiftTotal]
redshifts = redshiftTotal[mask]

#redshifts = np.sort(np.array([0.35, 0.875, 0.10165, 0.25, 0.45, 0.575, 0.725, 0.9]))

#redshifts = np.sort(np.array([0.10165, 0.25,    0.35 ,   0.45,    0.575,   0.725,   0.875,   0.9,     1.125, 1.65,    1.75,    2.25,    2.5]))# 2.75,    3.5,  ]))



Ms = np.linspace(7, 12, 60)

# blob 1: the smf
blob_n1 = ['galaxy_smf']
blob_i1 = [('z', redshifts), ('logbins', Ms)]
blob_f1 = ['StellarMassFunction']

# blob 2: the sfrd
blob_n2 = ['galaxy_sfrd']
blob_i2 = [('z', redshifts)]
blob_f2 = ['SFRD']

blob_pars = \
{
    'blob_names': [blob_n1, blob_n2],
    'blob_ivars': [blob_i1, blob_i2],
    'blob_funcs': [blob_f1, blob_f2],
    'blob_kwargs': [None] * 2,
} 


#define the parameters that remain unchanged
base_pars = ares.util.ParameterBundle('emma:model1')
base_pars.update(blob_pars)
base_pars.update({'debug':True})

#set free parameters to be fit
free_pars = \
[
    'pq_func_par0[0]',
    'pq_func_par2[0]', 

    #norm
    'pq_func_par0[1]',
    'pq_func_par2[1]', 

    #gamma
    'pq_func_par0[2]',
    'pq_func_par2[2]', 

    #peak mass
    'pq_func_par0[3]',
    'pq_func_par2[3]', 
]

is_log = [False, False, False, False, False, False, False, False]

#priors for each free parameter
ps = DistributionSet()
ps.add_distribution(UniformDistribution(-1, 4), 'pq_func_par0[0]')
ps.add_distribution(UniformDistribution(-1, 1),  'pq_func_par2[0]')

ps.add_distribution(UniformDistribution(0, 2),   'pq_func_par0[1]')
ps.add_distribution(UniformDistribution(-1, 1),  'pq_func_par2[1]')

ps.add_distribution(UniformDistribution(0, 1),   'pq_func_par0[2]')
ps.add_distribution(UniformDistribution(-3, 1),  'pq_func_par2[2]')

ps.add_distribution(UniformDistribution(10.0, 14.0),   'pq_func_par0[3]')
ps.add_distribution(UniformDistribution(-1, 2),  'pq_func_par2[3]')

#initial guesses
#From Moster2010, table 7
logM_0 = 11.88 #(0.01)
mu = 0.019 #(0.002)
N_0 = 0.0282 #(0.0003)
nu = -0.72 #(0.06)
gamma_0 = 0.556 #0.001
gamma_1 = -0.26 #(0.05)
beta_0 = 1.06 #(0.06)
beta_1 = 0.17 #(0.12)

#logM_0 = 11.0

guesses = \
{
    'pq_func_par0[0]': beta_0,
    'pq_func_par2[0]': beta_1, 

    #norm
    'pq_func_par0[1]': N_0,
    'pq_func_par2[1]': nu, 

    #gamma
    'pq_func_par0[2]': gamma_0,
    'pq_func_par2[2]': gamma_1, 

    #peak mass
    'pq_func_par0[3]': logM_0,
    'pq_func_par2[3]': mu, 
}

# Initialize a fitter object and give it the data to be fit
fitter_smf = ares.inference.FitGalaxyPopulation(**base_pars)

fitter_smf.include.append('smf')

# The data can also be provided more explicitly
fitter_smf.data = 'tomczak2014',  'mortlock2011', 'moustakas2013', 'marchesini2009_10'

fitter = ares.inference.ModelFit(**base_pars)
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
fitter.nwalkers = NumWalkers

fitter.jitter = [0.1] * len(fitter.parameters)

fitter.guesses = guesses

home = os. environ['HOME']
dt_string = datetime.now().strftime("%d_%m_%H-%M") + "_" + str(zLim_low) + "-" + str(zLim_high)
title = home + "/scratch/jobs/MCMC_files/smf_" + dt_string

# Run the thing
fitter.run(title, burn=BurnIn, steps=StepCount, save_freq=5, clobber=True)

#fitter.run('MCMC_files/testing', burn=BurnIn, steps=StepCount, save_freq=5, clobber=True)
