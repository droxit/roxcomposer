#!/usr/bin/env bash
echo Starting tests...
python3 -m unittest tests/base_service.py &&
python3 -m unittest tests/math_service.py &&
python3 -m unittest tests/number_service.py &&
echo ...Finished tests