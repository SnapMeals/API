#!/bin/bash

curl -X POST -H "Content-Type: application/json" -d @meal2_suggestion.json http://localhost:8000/lowcal | jq | tee meal2_lowcal_suggestion.json