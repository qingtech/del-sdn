#!/bin/sh
#get the abs path of main.sh
this_dir=`pwd`

dirname $0|grep "^/" >/dev/null

if [ $? -eq 0 ];then

	this_dir=`dirname $0`

else

	dirname $0|grep "^\." >/dev/null

	retval=$?

	if [ $retval -eq 0 ];then

		this_dir=`dirname $0|sed "s#^.#$this_dir#"`

	else

		this_dir=`dirname $0|sed "s#^#$this_dir/#"`

	fi

fi

echo 'cd to '$this_dir
cd $this_dir

echo 'run main.py to generate load.txt, traffic.txt'
python main.py
echo 'copy load.txt traffic.txt to directory Rscript'
cp load.txt Rscript
cp traffic.txt Rscript
cp log.txt Rscript
#sleep 5
cd Rscript
echo 'start to run R script'
Rscript load.R
Rscript load2.R
Rscript traffic.R
rm Rplots.pdf
dname=$(date +%Y%m%d-%H%M%S)
echo 'log to logs.txt'
echo $dname >> result.log
cat log.txt >> result.log
echo 'move result to directory '$dname
mkdir $dname
mv *.txt *.pdf $dname
