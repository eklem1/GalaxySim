
import sys, os
import ares
import numpy as np
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as pl
import distpy

title = '/home/eklem1/scratch/jobs/MCMC_files/'+ sys.argv[1]

print(title)
anl = ares.analysis.ModelSet(title)

labels = \
{
    'pq_func_par0[0]': 'beta_0',
    'pq_func_par2[0]': 'beta_1', 

    #norm
    'pq_func_par0[1]': 'N_0',
    'pq_func_par2[1]': 'nu', 

    #gamma
    'pq_func_par0[2]': 'gamma_0',
    'pq_func_par2[2]': 'gamma_1', 

    #peak mass
    'pq_func_par0[3]': 'logM_0',
    'pq_func_par2[3]': 'mu', 
}

anl.custom_labels = labels

z = float(sys.argv[2])

gpop = ares.analysis.GalaxyPopulation()

savename = sys.argv[1]+"_fig.png"
home = os.environ['HOME']
saveAs = home + "/scratch/jobs/results/" + savename

# trig = anl.TrianglePlot(pars=params)

# anl.WalkerTrajectoriesMultiPlot(best_fit='mode')

fit_best_like = anl.max_likelihood_parameters()
pars_best = ares.util.ParameterBundle("emma:model1")

pars_best.update(fit_best_like)
pop_best = ares.populations.GalaxyPopulation(**pars_best)


fig, ax = pl.subplots(figsize=(8, 5))
Ms_short = np.linspace(7, 12, 80)

ls_best = pop_best.StellarMassFunction(z, Ms_short)

ax = anl.ReconstructedFunction('galaxy_smf', ivar=[z, None], samples='all', color='lightskyblue', alpha=0.01, ax=ax)

obslf = ares.analysis.GalaxyPopulation()
obslf.PlotSMF(z=z, ax=ax, round_z=0.2, log10Mass=True)

pl.semilogy(Ms_short, ls_best, label='Best fit')

pl.title("z = %.2f" %z)
pl.xlabel("log$_{10}$(m / M$_o$)")
pl.legend()
pl.ylim(1e-15, 1e2)
pl.savefig(savename)
# pl.show()

print("#-#-###############################")
params = \
        ['pq_func_par0[0]',
         'pq_func_par2[0]', 

         #norm
         'pq_func_par0[1]',
         'pq_func_par2[1]', 

         #gamma
         'pq_func_par0[2]',
         'pq_func_par2[2]', 

         #peak mass
         'pq_func_par0[3]',
         'pq_func_par2[3]' 
        ]

covar = anl.CovarianceMatrix(params)

for i in range(len(covar[0])):
        print(anl.get_1d_error(params[i])) #(maximum likelihood value, positive error, negative error).

