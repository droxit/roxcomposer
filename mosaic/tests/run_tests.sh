#!/usr/bin/env bash
echo Starting tests...
python3 -m unittest base_service.py &&
python3 -m unittest math_service.py &&
python3 -m unittest number_service.py &&
echo ...Finished tests