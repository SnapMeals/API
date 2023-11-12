#!/bin/bash

curl -X POST -H "Content-Type: application/json" -d @meal1.json http://localhost:8000/suggest_meal | jq | tee meal1_suggestion.json
