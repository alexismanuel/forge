#!/usr/bin/env sh

poetry run python -m pytest --cov=app --cov-report term-missing tests
