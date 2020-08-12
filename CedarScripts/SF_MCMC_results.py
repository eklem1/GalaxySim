
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
     #A
    'pq_func_par0[7]': '$a_0$', #const
    'pq_func_par1[7]': '$a_1$', #offset
    'pq_func_par2[7]': '$a_2$', #m

    #B
    'pq_func_par0[8]': '$b_0$', #const
    'pq_func_par1[8]': '$b_1$', #offset
    'pq_func_par2[8]': '$b_2$', #m

    #C
    'pq_func_par0[9]': '$c_0$', #const
    'pq_func_par2[9]': '$c_2$',

    #D
    'pq_func_par0[10]': '$d_1$', #const
    'pq_func_par2[10]': '$d_2$',

}

params = \
[
     #A
    'pq_func_par0[7]', #const
#    'pq_func_par1[7]', #offset
    'pq_func_par2[7]', #m

    #B
    'pq_func_par0[8]', #const
#    'pq_func_par1[8]', #offset
    'pq_func_par2[8]', #m

    #C
    'pq_func_par0[9]', #const
    'pq_func_par2[9]',

    #D
    'pq_func_par0[10]', #const
    'pq_func_par2[10]',

]

anl.custom_labels = labels

z = float(sys.argv[2])
# 0.35, 0.875, 1.125, 1.75, 2.25, 2.75

savename = sys.argv[1]+"_fig.png"

trig = anl.TrianglePlot(pars=params, color_by_like=True)
pl.savefig("trig_" + savename)

anl.WalkerTrajectoriesMultiPlot(best_fit='mode', fig=2)
pl.savefig("Walk_" + savename)


#making hist forset parameter
bests = [anl.get_1d_error(i, nu=0.68,  peak='mode') for i in params]
means = [anl.get_1d_error(i, nu=0.68,  peak='median') for i in params]

for i, e in enumerate(bests):
    print(bests[i])

i = 3

pars = ares.util.ParameterBundle("emma:model3")

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
pars_best = ares.util.ParameterBundle("emma:model3")

pars_best.update(fit_best_like)
pop_best = ares.populations.GalaxyPopulation(**pars_best)

#making SMF plot for a given z
fig, ax = pl.subplots(figsize=(8, 5))
Ms_short = np.linspace(7, 12, 80)

ls_best = pop_best.StellarMassFunction(z, Ms_short, sf_type='smf_sf')
ls_best_t = pop_best.StellarMassFunction(z, Ms_short, sf_type='smf_tot')
ls_best_q = pop_best.StellarMassFunction(z, Ms_short, sf_type='smf_q')

print(ls_best)

ax = anl.ReconstructedFunction('galaxy_smf_sf', ivar=[z, None], samples='all', color='lightskyblue', alpha=0.01, ax=ax)
ax = anl.ReconstructedFunction('galaxy_smf_q', ivar=[z, None], samples='all', color='peachpuff', alpha=0.01, ax=ax)

obslf = ares.analysis.GalaxyPopulation()
obslf.PlotSMF(z, sources="tomczak2014", color="y", ecolor='y', mec='y', label="tomczak2014 Tot", quantity="smf_tot", ax=ax, round_z=0.2, log10Mass=True)
obslf.PlotSMF(z, sources="tomczak2014",  label="tomczak2014 SF", color="b", ecolor='b',  mec='b', ax=ax, round_z=0.2, log10Mass=True)
obslf.PlotSMF(z, sources="tomczak2014", color="r", ecolor='r',  mec='r', label="tomczak2014 Q", quantity="smf_q", ax=ax, round_z=0.2, log10Mass=True)


pl.semilogy(Ms_short, ls_best, label='Best fit sf', color='navy', ls="--")
pl.semilogy(Ms_short, ls_best_t, label='total', color='goldenrod', ls="--")

pl.semilogy(Ms_short, ls_best_q, label='Best fit q', color='firebrick', ls="--")


pl.title("z = %.2f" %z)
pl.xlabel("log$_{10}$(m / M$_o$)")
pl.ylabel('$\phi(M_*)$ [dex$^{-1}$cMpc$^{-3}$]')

pl.legend()
# pl.ylim(1e-15, 1e2)
pl.savefig(savename)
# pl.show()

