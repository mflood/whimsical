#!/usr/bin/env sh

source year_day.sh
printf -v padded_day "%02d" ${ADVENT_DAY}

vim data/${ADVENT_YEAR}/day/${ADVENT_DAY}/test-input.txt
