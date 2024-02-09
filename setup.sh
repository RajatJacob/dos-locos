#!/bin/sh

# We're using poetry to manage our dependencies and avoid conflicts with other projects
pip install poetry ipykernel
poetry install