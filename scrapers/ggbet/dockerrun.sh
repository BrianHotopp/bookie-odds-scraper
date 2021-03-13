#!/bin/bash

docker run --rm --env-file environment.env --network="host" ggbet
