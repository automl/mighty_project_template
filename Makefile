
# NOTE: Used on linux, limited support outside of Linux
#
# A simple makefile to help with small tasks related to development of Mighty
# These have been configured to only really run short tasks. Longer form tasks
# are usually completed in github actions.

.PHONY: help install-dev install check format pre-commit clean build clean-doc clean-build test doc publish

help:
	@echo "Makefile Mighty"
	@echo "* install-dev      to install all dev requirements and install pre-commit"
	@echo "* check            to check the source code for issues"
	@echo "* format           to format the code with ruff"
	@echo "* typing           to type check the code with mypy"
	@echo "* pre-commit       to run the pre-commit check"
	@echo "* clean            to clean the dist and doc build files"
	@echo "* build            to build a dist"
	@echo "* test             to run the tests"
	@echo "* docs             to serve and view the docs"
	@echo "* docs-build-only  to generate and view the html files"
	@echo "* docs-deploy      to push the latest doc version to gh-pages"
	@echo "* publish          to help publish the current branch to pypi"

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
	ruff format --check mighty_domain_randomization
	ruff check mighty_domain_randomization

format: 
	$(ISORT) isort mighty_domain_randomization
	$(RUFF) format --silent mighty_domain_randomization
	$(RUFF) check --fix --silent mighty_domain_randomization --exit-zero
	$(RUFF) check --fix mighty_domain_randomization --exit-zero
