
# NOTE: Used on linux, limited support outside of Linux
#
# A simple makefile to help with small tasks related to development of Mighty
# These have been configured to only really run short tasks. Longer form tasks
# are usually completed in github actions.

.PHONY: help install check format

help:
	@echo "Makefile Mighty Project"
	@echo "* install      to install all dev requirements and install pre-commit"
	@echo "* check            to check the source code for issues"
	@echo "* format           to format the code with ruff"

PYTHON ?= python
CYTHON ?= cython
PYTEST ?= uv run pytest
CTAGS ?= ctags
PIP ?= uv --cache-dir .uv_cache pip
MAKE ?= make
PRECOMMIT ?= uv run pre-commit
RUFF ?= uv run ruff
MYPY ?= uv run mypy
ISORT ?= uv run isort

DIR := ${CURDIR}
DIST := ${CURDIR}/dist
DOCDIR := ${CURDIR}/docs
INDEX_HTML := file://${DOCDIR}/html/build/index.html

install:
	$(PIP) install hypersweeper==0.2.3
	$(PIP) install -e "."

# pydocstyle does not have easy ignore rules, instead, we include as they are covered
check: 
	ruff format --check mighty_project
	ruff check mighty_project

format: 
	$(ISORT) isort mighty_project
	$(RUFF) format --silent mighty_project
	$(RUFF) check --fix --silent mighty_project --exit-zero
	$(RUFF) check --fix mighty_project --exit-zero
