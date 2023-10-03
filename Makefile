.PHONY: all test clean
SHELL := /usr/bin/env bash

lint:
	@echo "Running linting commands"; \
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics; \
  flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics;

test:
	@echo "Running unit tests"; \
	python -m unittest discover;
