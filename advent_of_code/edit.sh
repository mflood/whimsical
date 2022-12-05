#!/usr/bin/env sh

source year_day.sh
printf -v padded_day "%02d" ${ADVENT_DAY}

vim flood_advent/problem_${ADVENT_YEAR}_${padded_day}.py "${@:1}"
echo "flood_advent/problem_${ADVENT_YEAR}_${padded_day}.py"
