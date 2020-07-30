
import sys
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

anl.custom_labels = labels

z = float(sys.argv[2])
# 0.35, 0.875, 1.125, 1.75, 2.25, 2.75

gpop = ares.analysis.GalaxyPopulation()

#ax = anl.ReconstructedFunction('galaxy_smf', ivar=[z, None], samples='all', color='b', alpha=0.01)

#gpop.PlotSMF(z, ax=ax, round_z=0.2, log10Mass=True)

#ax.legend()
savename = sys.argv[1]+"_fig.png"
#pl.savefig(savename)
#pl.show()

trig = anl.TrianglePlot(pars=params)
pl.savefig("trig_" + savename)

anl.WalkerTrajectoriesMultiPlot(best_fit='mode', fig=2)
pl.savefig("Walk_" + savename)



#making hist forset parameter
bests = [anl.get_1d_error(i, nu=0.68,  peak='mode') for i in params]
means = [anl.get_1d_error(i, nu=0.68,  peak='median') for i in params]

for i, e in enumerate(bests):
    print(bests[i])

i = 3

pars = ares.util.ParameterBundle("emma:model1")

ax = anl.PosteriorPDF(pars=params[i], fig=3)

#best fit with mode
pl.axvline(x=bests[i][0], ls="-", color="green", label="Best Fit")
ax.axvspan(bests[i][0]-bests[i][1][1], bests[i][0]+bests[i][1][0], alpha=0.2, color='green' ,label="68% error")

pl.axvline(x=means[i][0], ls="--", color="black", label="Mean Fit",  alpha=0.4)

pl.axvline(x=pars[params[i]], ls="--", color="orange", label="Moster2010",  alpha=1)

pl.ylabel(labels[params[i]])
pl.legend()
pl.savefig("like_" + savename)


fit_best_like = anl.max_likelihood_parameters()
pars_best = ares.util.ParameterBundle("emma:model1")

pars_best.update(fit_best_like)
pop_best = ares.populations.GalaxyPopulation(**pars_best)

#making DMF plot for a given z
fig, ax = pl.subplots(figsize=(8, 5))
Ms_short = np.linspace(7, 12, 80)

ls_best = pop_best.StellarMassFunction(z, Ms_short)
print(ls_best)
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

