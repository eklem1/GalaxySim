#!/bin/bash

file=$1
echo $file

line=$(grep -m 1 "Wrote" < $file)

RunName=${line%.b*}
RunName=${RunName##*/}

echo "files: ${RunName}"

outputP="testing_1.txt"
temp="temp_1.txt"

python ~/projects/def-acliu/eklem1/params_results.py ${RunName} > $temp

day=${RunName#smf_}
day=${day%%_*}

lowZ=${RunName#*_*_*_*_}
lowZ=${lowZ%%-*}

highZ=${RunName##*-}

ID=${file##*m-}
ID=${ID%_*}

num=${file##*_}
num=${num%.*}

echo "${ID}.${num}, ${lowZ}, ${highZ}" >> $outputP

temp2="temp_2.txt"

grep '#-#-' $temp -A 10 > $temp2

grep -v "#" "$temp2" > $temp


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
done < "$temp"


