#!/bin/bash

# get abstract file from ncbi by pmid

pmid=$1

wget -O - "http://www.ncbi.nlm.nih.gov/pubmed/?term=$pmid&report=abstract&format=text" | sed 's/<.\+>//g' | perl -pe 'chomp; $_ = lc . " ";'
