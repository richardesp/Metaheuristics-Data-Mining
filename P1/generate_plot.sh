#!/bin/bash

cat << _end_ | gnuplot
set terminal postscript eps color
set terminal png size 1280,720 enhanced font "Helvetica,20"
set output "grafico_ej1.png"
set key right bottom
set xlabel "Number of cities"
set ylabel "Frequency of appearance of local/global minimum"
plot "ej1_experiment.dat" using 1:2 t "Hill climbing algorithm" w l
_end_