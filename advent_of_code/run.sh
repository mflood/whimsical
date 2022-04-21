#!/usr/bin/env sh

source venv/bin/activate
source year_day.sh
printf -v padded_day "%02d" ${ADVENT_DAY}

python flood_advent/problem_${ADVENT_YEAR}_${padded_day}.py "${@:1}"
echo "done running flood_advent/problem_${ADVENT_YEAR}_${padded_day}.py"