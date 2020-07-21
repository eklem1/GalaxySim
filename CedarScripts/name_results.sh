#!/bin/bash

#file=slurm-46326974.out

file=$1

echo $file

line=$(grep -m 1 "Wrote" < $file)

RunName=${line%.b*}
RunName=${RunName##*/}

echo "files: ${RunName}"

python ~/projects/def-acliu/eklem1/MCMC_results_new.py ${RunName} $2
