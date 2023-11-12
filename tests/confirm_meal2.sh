#!/bin/bash

curl -X POST -H "Content-Type: application/json" -d @meal2_suggestion.json http://localhost:8000/confirm_meal | jq