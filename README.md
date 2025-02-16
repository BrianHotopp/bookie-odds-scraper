# bookie-odds-scraper

![python version](https://img.shields.io/badge/python-3.6-blue.svg)

Containerized web scrapers for CSGO match odds data. 🎲


## Description

This project contains code to scrape odds data from bookie websites like ggbet, egb and others. In particular we scrape CSGO odds data like teams, tournaments and winner odds.

Since each website has different formatting, the data manipulation for each scraper must be hard coded to the website. 

The very basic procedure of each scraper is the following:

1. Fetch website html text using Selenium.
2. Locate and extract the relevant section containing tabular data.
3. Transcribe the html tabular data into python data structures.
4. Write the cleaned data to a database.

These scrapers are containerized using Docker and can be run on a schedule with AWS Fargate (or wherever you want really). The containers access database credentials and a Sentry URL for monitoring via environment variables configured on each deployment. The container images can be found on [Docker Hub](https://hub.docker.com/u/maxlamberti). A schematic of the production implementation can be found below.

## Database Schema


## Contributors
- [maxlamberti](https://github.com/maxlamberti)
- [kevinramlal](https://github.com/kevinramlal)
- [brian hotopp](https://github.com/BrianHotopp)
