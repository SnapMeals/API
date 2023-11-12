#!/bin/bash

curl -X POST -H "Content-Type: application/json" -d @meal2_suggestion.json http://localhost:8000/vegetarianize | jq | tee meal2_vegetarianized_suggestion.json