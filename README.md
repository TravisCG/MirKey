MirKey
======

MicroRNA keyword database for text mining.

1. Installing MirKey:

- Set up a Readis database
- Install rredis R package (optional)
- Install python-redis
- Clone this repository
- run build-db.sh in build directory

2. Use MirKey

- Create a list of microRNA ids
- Run getmirkeyword.py with the mir IDs
- Start R
- source("sig.keys.R")
- load the table created by getmirkeyword.py
- run sig.keys
