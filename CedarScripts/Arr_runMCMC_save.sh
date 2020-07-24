#!/bin/bash
#SBATCH --account=def-acliu
#SBATCH --time=0-4:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32
#SBATCH --mail-user=<emma.klemets@mail.mcgill.ca>
#SBATCH --mail-type=ALL
#SBATCH --mem=20G
#SBATCH --array=1-8%1

input=$(cat ./ArrScript/input_${SLURM_ARRAY_TASK_ID}.txt)
echo $input

mpirun -np 32 python ~/projects/def-acliu/eklem1/MCMC_fitScript_new.py $input

if [[ $SLURM_ARRAY_TASK_ID = 8 ]]
then
	for ID in {1..8}
	do	
#z=0.9

file="slurm-${SLURM_JOB_ID}_${ID}.out"
echo $file

line=$(grep -m 1 "Wrote" < ${file})

RunName=${line%.b*}
RunName=${RunName##*/}

echo "files: ${RunName}"

outputP="OutputArr.txt"

python ~/projects/def-acliu/eklem1/params_results.py ${RunName} > tempArr.txt

day=${RunName#smf_}
day=${day%%_*}

lowZ=${RunName#*_*_*_*_}
lowZ=${lowZ%%-*}

highZ=${RunName##*-}

echo "${SLURM_JOB_ID}.${ID}, ${lowZ}, ${highZ}" >> $outputP

parmsAll=$(grep '#-#-' tempArr.txt -A 8)

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

	done
fi
