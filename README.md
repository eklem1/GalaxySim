# GalaxySim

**GalaxyHOD.py**: The basis for a new ARES class with a LF and SMF model based off the work below, as well as main sequence SFR, SSFR and SFRD models.   
See https://github.com/eklem1/ares/tree/hod_add for updated file.   
Basic set up:
```
pars = ares.util.ParameterBundle("emma:model1")
pop = ares.populations.GalaxyPopulation(**pars)
```

**WorkingFromHalo.ipynb**: Looking at a simplified relation of the HMF to LF as well as to SMF.   
**HMFtoSMF_nonLinear.ipynb**: Starting from Moster2010 paper, a DPL relation of HMF to SMF.  
**SFRs.ipynb**: Starting from Speagle2014 paper, smain sequence SFR, SSFR and SFRD.  

**FirstFits.ipynb**: Starting to work with fitting in ARES for the LF.  
**SMF_fit.ipynb**: Working on MCMC fit of SMF, currently not looking too great.  
**SMF_fitScript.py**: Python script of SMF_fit.ipynb.  
 
**DataCompile.ipynb**: Script to read and format data from "behroozi-2013-data-compilation" for more SMF and SSFR lit values.

Working with Ares (see docs at https://ares.readthedocs.io/en/latest/index.html).
