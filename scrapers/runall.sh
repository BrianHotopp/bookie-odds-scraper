#!/bin/sh
cd /home/scraper/bookie-odds-scraper/scrapers
docker run --rm --env-file environment.env --network="host" egb
docker run --rm --env-file environment.env --network="host" ggbet
docker run --rm --env-file environment.env --network="host" hltv
docker run --rm --env-file environment.env --network="host" hltv_results
docker run --rm --env-file environment.env --network="host" rivalry
