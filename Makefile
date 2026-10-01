SHELL := /bin/sh

.PHONY: help validate-template validate-mcp setup format lint test build security ci

help:
	@printf '%s\n' 'Template: validate-template' 'MCP: validate-mcp' 'Project (configure before use): setup format lint test build security ci' 'Bootstrap: python3 scripts/bootstrap.py --help'

validate-template:
	python3 scripts/validate_repo.py
	python3 scripts/validate_re_catalog.py
	python3 -m unittest discover -s tests -v

validate-mcp:
	python3 -m pip install -e 'services/mcp[dev]'
	ruff check services/mcp/src services/mcp/tests
	pytest -q services/mcp/tests

setup format lint test build security:
	@echo 'This is a template placeholder: implement this target for your actual project; do not treat it as a passing check.' >&2
	@exit 2

ci: validate-template validate-mcp lint test build security
