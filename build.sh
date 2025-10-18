#!/bin/bash
# Build script for production deployment

# Backup original files
cp main.py main_development.py
cp requirements.txt requirements_development.txt

# Use production versions
cp main_production.py main.py
cp requirements_production.txt requirements.txt

# Install dependencies
pip install -r requirements.txt