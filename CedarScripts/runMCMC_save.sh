#!/bin/bash
#SBATCH --account=def-acliu
#SBATCH --time=0-2:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32
#SBATCH --mail-user=<emma.klemets@mail.mcgill.ca>
#SBATCH --mail-type=ALL
#SBATCH --mem=30G

mpirun -np 32 python ~/projects/def-acliu/eklem1/MCMC_fitScript_new.py 128 20 300 0 4.0

z=0.9

file="slurm-${SLURM_JOB_ID}.out"
echo $file

line=$(grep -m 1 "Wrote" < $file)

RunName=${line%.b*}
RunName=${RunName##*/}

echo "files: ${RunName}"

outputP="testingP.txt"

python ~/projects/def-acliu/eklem1/MCMC_results_new.py ${RunName} $z > temp.txt

day=${RunName#smf_}
day=${day%%_*}

lowZ=${RunName#*_*_*_*_}
lowZ=${lowZ%%-*}

highZ=${RunName##*-}

echo "${SLURM_JOB_ID}, ${lowZ}, ${highZ}" >> $outputP

parmsAll=$(grep '#-#-' temp.txt -A 8)

parmsAll=${parmsAll##*#}
parmsAll=${parmsAll:1}

while IFS= read -r line
do
	echo "---"
	val=${line%, arr*}
	val=${val:1}

	errPos=${line##*([}
	errPos=${errPos%,*}

	errNe=${line##*,}
	errNe=${errNe%]*}

	echo "${val}, ${errPos}, ${errNe}" >> $outputP
done <<< "$parmsAll"


