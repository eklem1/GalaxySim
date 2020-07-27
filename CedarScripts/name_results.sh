#!/bin/bash

#file=slurm-46326974.out

file=$1

echo $file

line=$(grep -m 1 "Wrote" < $file)

RunName=${line%.b*}
RunName=${RunName##*/}

echo "files: ${RunName}"

python ~/projects/def-acliu/eklem1/params_results.py ${RunName}
