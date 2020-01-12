#!/bin/bash
NOWTS="$(date '+%Y%m%d')"
wget -O $1 "https://tidesandcurrents.noaa.gov/api/datagetter?product=predictions&application=NOS.COOPS.TAC.WL&begin_date=$NOWTS&end_date=$NOWTS&datum=MLLW&station=8720587&time_zone=lst_ldt&units=english&interval=h&format=json"

