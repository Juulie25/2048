#!/bin/bash

max=30000
for (( i=1; i<=$max; i++ ))
do
  python3 2048_method3.py
  echo "Avancement : $i /$max"
done
