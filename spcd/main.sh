#!/bin/sh
echo 'run main.py to generate load.txt, traffic.txt'
python main.py
echo 'copy load.txt traffic.txt to directory Rscript'
cp load.txt Rscript
cp traffic.txt Rscript
#sleep 5
cd Rscript
echo 'start to run R script'
Rscript load.R
Rscript traffic.R
rm Rplots.pdf
dname=$(date +%Y%m%d-%H%M%S)
echo 'move result to directory '$dname
mkdir $dname
mv *.txt *.pdf $dname
