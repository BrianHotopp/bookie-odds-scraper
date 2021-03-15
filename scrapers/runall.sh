#!/bin/sh
cd /home/hotopb/bookie-odds-scraper/scrapers
/snap/bin/docker run --rm --env-file environment.env --network="host" egb
/snap/bin/docker run --rm --env-file environment.env --network="host" ggbet
/snap/bin/docker run --rm --env-file environment.env --network="host" hltv
/snap/bin/docker run --rm --env-file environment.env --network="host" hltv_results
/snap/bin/docker run --rm --env-file environment.env --network="host" rivalry
