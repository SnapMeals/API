#!/bin/bash

curl -X POST -H "Content-Type: application/json" -d @meal2.json http://localhost:8000/suggest_meal | jq | tee meal2_suggestion.json
