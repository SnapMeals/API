#!/bin/bash

curl -X POST -H "Content-Type: application/json" -d @meal1_suggestion.json http://localhost:8000/lowcal | jq | tee lowcal_meal1_suggestion.json