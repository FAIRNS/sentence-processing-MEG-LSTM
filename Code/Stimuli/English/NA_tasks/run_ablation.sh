#!/bin/bash

cat $1 | /checkpoint/mbaroni/german-stuff/jl.py --max 200 | /private/home/mbaroni/stool/stool.py run --time 30 -

echo ALL DONE
