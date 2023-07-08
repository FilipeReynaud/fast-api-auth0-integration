################################################################
# Makefile to setup the local development environment
################################################################

#-----------------------------------------------------------------------------------------------
# Shell variables
#-----------------------------------------------------------------------------------------------

SHELL := /bin/bash

# Console text colors :)
BOLD=$(shell tput bold)
RED=$(shell tput setaf 1)
GREEN=$(shell tput setaf 2)
YELLOW=$(shell tput setaf 3)
RESET=$(shell tput sgr0)

# Virtual environment
VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip3
DOCKER-COMPOSE = docker-compose

# Default run command
COMMAND = "--help"
ifdef command
	COMMAND=$(command)
endif

#-----------------------------------------------------------------
# Tasks
#-----------------------------------------------------------------

help:
	@echo "$(BOLD)$(GREEN)FastAPI Auth0 Integration"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: virtualenv
virtualenv:  ## Creates a virtual environment
	@virtualenv $(VENV)

.PHONY: local-init
install-deps:  ## Installs project dependencies
	@poetry install

.PHONY: local-run
local-run:  ## Run local API
	uvicorn src.app:app --reload

.PHONY: run
run:  ## Run API with docker
	docker-compose up --build -d

.PHONY: down
down:  ## Kill docker containers
	docker-compose down

.PHONY: test
test:  ## Run tests
	pytest

# Default command to help
.DEFAULT_GOAL := help
