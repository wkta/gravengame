.SHELL := /bin/bash
MANAGE := python

.PHONY: all help deps static migrate restart update deploy

all: help

help:
	@echo " Usage: "
	@echo "  make start - start game"

freeze:
	pip freeze > requirements.txt

pipenv-install:
	@echo " Not implemented"


pip-install:
	pip install -r requirements.txt

start:
	$(MANAGE) launcher.py
