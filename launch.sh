#!/usr/bin/env bash
# Update repository
git checkout RT_tests_45min_2018
git pull
# Launch test battery
python launch.py
