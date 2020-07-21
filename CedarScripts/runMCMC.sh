#!/bin/bash
#SBATCH --account=def-acliu
#SBATCH --time=0-1:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32
#SBATCH --mail-user=<emma.klemets@mail.mcgill.ca>
#SBATCH --mail-type=ALL
#SBATCH --mem=20G

mpirun -np 32 python ~/projects/def-acliu/eklem1/MCMC_fitScript_new.py 128 20 140 2.0  4.0
z=2.25

file="slurm-${SLURM_JOB_ID}.out"
echo $file

line=$(grep -m 1 "Wrote" < $file)

RunName=${line%.b*}
RunName=${RunName##*/}

echo "files: ${RunName}"

python ~/projects/def-acliu/eklem1/MCMC_results_new.py ${RunName} $z

