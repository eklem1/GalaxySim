#!/bin/bash
#SBATCH --account=def-acliu
#SBATCH --time=0-1:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32
#SBATCH --mail-user=<emma.klemets@mail.mcgill.ca>
#SBATCH --mail-type=ALL
#SBATCH --mem=20G

mpirun -np 32 python ~/projects/def-acliu/eklem1/MCMC_fitScript_new.py 128 20 140 1.0 2.0 
