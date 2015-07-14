#!/bin/bash

mkdir tmp
cd tmp

# download the latest mirBase files
wget ftp://mirbase.org/pub/mirbase/CURRENT/miRNA.dat.gz
wget ftp://mirbase.org/pub/mirbase/CURRENT/database_files/wikipedia.txt.gz

gunzip miRNA.dat.gz
gunzip wikipedia.txt.gz

# formatting wikipedia
../mirwiki.py wikipedia.txt >strippedwiki.txt

# get abstracts
awk '/RX/{print $3}' miRNA.dat | sed 's/\.//' | sort -u >pmid

for i in `cat pmid`
do
   echo $i `../getabstract.sh $i`
done >abstracts.txt

../mirdatparse.py miRNA.dat abstracts.txt >mir_keywords.txt

# load the whole stuff to Redis
../mirassoc.py mir_keywords.txt >fisher.txt
#../keyputtodb.py mir_keywords.txt ../blacklist.txt
#../keyputtodb.py strippedwiki.txt ../blacklist.txt

cd ..
#rm -fr tmp
