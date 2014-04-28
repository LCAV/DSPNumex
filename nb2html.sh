#! /bin/bash

mkdir ./html &> /dev/null

for file in *.ipynb
do
  bname=`basename ${file} .ipynb`
  ipython nbconvert --to html --output html/${bname} ${file} &> /dev/null

  # If you need to protect data URI against URL auto-completion, uncomment the following line
  #python ./protect_dataURI.py html/${bname}.html html/${bname}.html
done
