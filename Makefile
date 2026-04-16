.PHONY: setup test run-all clean lint typecheck format local-env junie junie-gemma generate-module

PYTHON = venv/bin/python3
PIP = venv/bin/pip

setup:
	python3 -m venv venv
	$(PIP) install --upgrade pip
	$(PIP) install -e ".[dev]"

test:
	$(PYTHON) -m pytest tests/

run-all:
	$(PYTHON) generate.py --source all

clean:
	rm -rf output/*
	rm -rf src/**/__pycache__
	rm -rf tests/__pycache__

lint:
	$(PYTHON) -m ruff check src tests

format:
	$(PYTHON) -m ruff format src tests

typecheck:
	$(PYTHON) -m mypy src tests

local-env:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo ".env file created from .env.example. Please edit it to set your local LLM API."; \
	else \
		echo ".env file already exists."; \
	fi

junie:
	@./scripts/junie_local.sh $(task)

junie-gemma:
	@./scripts/junie_local.sh --model gemma-local $(task)

generate-module:
	@./scripts/generate_module.sh $(name) "$(desc)"
