#!/bin/bash

QUERY_FORMAT="$(date +%Y%m%d)";
PLOT_FORMAT="$(date +%m/%d/%Y)";
API_URL="https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=predictions&application=NOS.COOPS.TAC.WL&begin_date=${QUERY_FORMAT}&end_date=${QUERY_FORMAT}&datum=MLLW&station=8720587&time_zone=lst_ldt&units=english&interval=h&format=json";

curl --fail --connect-timeout 5 --max-time 30 --no-progress-meter --output /tmp/tideheights.json "${API_URL}" && \
jq -r '.predictions[] | (.t | split(" ")[1] | split(":")[0]) as $times | "\($times) \(.v)"' /tmp/tideheights.json | \
gnuplot -e "set title 'Tide Height Predictions ${PLOT_FORMAT}'; set xlabel 'Hour of Day'; set ylabel 'Height in Feet'; set term svg; set output '/tmp/tideheights.svg'; set xrange [0:23]; set grid back; plot '/dev/stdin' using 0:2:xticlabel(1) with linespoints notitle lt rgb '#0000ff';" && \
mv /tmp/tideheights.svg /srv/surfstation.surf/www/dynamic/tideheights.svg;
