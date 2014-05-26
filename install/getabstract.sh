#!/bin/bash

# get abstract file from ncbi by pmid

pmid=$1
# FIXME Be careful. This script working only in build-db.sh!
wget -q -O - "http://www.ncbi.nlm.nih.gov/pubmed/?term=$pmid&report=xml&format=text" | ../pubxml.py
