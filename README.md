# GalaxySim

**GalSimReport.pdf**: Report with an overiew of my work over the summer: main functions of GalaxyHOD.py with a little theory, MCMC results and various smaller files.   

**GalaxyHOD.py**: The basis for a new ARES class with a LF and SMF model based off the work below, as well as main sequence SFR, SSFR and SFRD models.   
See https://github.com/eklem1/ares/tree/hod_add for updated file.   
Basic set up:
```
pars = ares.util.ParameterBundle("emma:model1")
pop = ares.populations.GalaxyPopulation(**pars)
```
### Creating Models   
**WorkingFromHalo.ipynb**: Looking at a simplified relation of the HMF to LF as well as to SMF.   
**HMFtoSMF_nonLinear.ipynb**: Starting from Moster2010 paper, a DPL relation of HMF to SMF.  
**SFRs.ipynb**: Starting from Speagle2014 paper, smain sequence SFR, SSFR and SFRD.    
**SMF_SFvsQ.ipynb**: Star-forming fraction to account for the difference of sf vs quiescent galaxies.   

### MCMC Fits   
**FirstFits.ipynb**: Starting to work with fitting in ARES for the LF.  
**SMF_fit.ipynb**: First work on MCMC fit of SMF, with old M_1 equation, and no SFRD blob.  
**SMF_fitScript.py**: Python script of SMF_fit.ipynb.  
**FitResults.ipynb**: Playing around with results of MCMCs.   
**CheckingFitGuesses.ipynb**: For checking walkers, initial guesses.   
   
**CompareParams.ipynb**: Comparing parameter values and resulting SMFs for various MCMC runs.    

**fractSMF_fit.py**: First try at fitting the SMF with the star-forming and quiescent fractions.   
**SF_FitResults.ipynb**: Looking at results of previous file fitting.

### Cedar   
#### CedarScripts   
Various bash scripts for running and analyzing MCMCs on Cedar, see pdf section 5.1 for details.   

 
### Miscellaneous
**DataCompile.ipynb**: Script to read and format data from "behroozi-2013-data-compilation" for more SMF and SSFR lit values.   
**UsefulHODFunctions.py**: To hold small functions I'm using in various files for analysis or getting lit values.   

Working with Ares (see docs at https://ares.readthedocs.io/en/latest/index.html).
