#!/bin/bash
cd /home/scraper/bookie-odds-scraper/scrapers
docker build ./egb -t egb
docker build ./ggbet -t ggbet
docker build ./hltv -t hltv
docker build ./hltv_results -t hltv_results
docker build ./rivalry -t rivalry

