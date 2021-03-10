#!/bin/bash

docker run --env-file environment.env --network="host" hltv-results
