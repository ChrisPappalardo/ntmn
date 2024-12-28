.PHONY: all clean clean-build clean-pyc clean-test docs coverage test test-all test-all-cov format lint pre-commit install-pre-commit deploy-pypi help

# Default target executed when no arguments are given to make.
all: help

# remove all build, test, coverage and Python artifacts
clean: clean-build clean-pyc clean-test

# remove build artifacts
clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name "*.egg-info" -exec rm -fr {} +
	find . -name "*.egg" -exec rm -f {} +

# remove Python file artifacts
clean-pyc:
	find . -name "*.pyc" -exec rm -f {} +
	find . -name "*.pyo" -exec rm -f {} +
	find . -name "*~" -exec rm -f {} +
	find . -name "__pycache__" -exec rm -fr {} +

# remove test, lint, typing, and coverage artifacts
clean-test:
	rm -f .coverage
	rm -fr .mypy_cache
	rm -fr .pytest_cache


###############
# DOCUMENTATION
###############

docs:
	mkdocs build


######################
# TESTING AND COVERAGE
######################

# Run unit tests and generate a coverage report.
coverage:
	pytest \
		--cov \
		--cov-config=.coveragerc \
		--cov-report xml \
		--cov-report term-missing:skip-covered

# Define a variable for the test file path.
TEST_FILE ?= tests/

test-all:
	python -m pytest $(TEST_FILE)

test-all-cov:
	python -m pytest $(TEST_FILE) \
		--cov \
		--cov xml \
		--cov-report term-missing:skip-covered

test: test-all-cov

########################
# LINTING AND FORMATTING
########################

# Define a variable for Python and notebook files.
PYTHON_FILES=.
lint format: PYTHON_FILES=.

lint:
	ruff check $(PYTHON_FILES)
	mypy $(PYTHON_FILES)

format:
	ruff check --fix $(PYTHON_FILES)
	mypy $(PYTHON_FILES)

pre-commit:
	pre-commit run --all-files


#######
# OTHER
#######

install-pre-commit:
	pre-commit install

deploy-pypi:
	twine upload dist/*


######
# HELP
######

help:
	@echo "===================="
	@echo "clean                        - run clean-build clean-pyc clean-test"
	@echo "-- DOCUMENTATION --"
	@echo "docs_build                   - build the documentation"
	@echo "-- LINTING --"
	@echo "format                       - run code formatters"
	@echo "lint                         - run linters"
	@echo "pre-commit                   - run pre-commit pipeline"
	@echo "-- TESTS --"
	@echo "coverage                     - run unit tests and generate coverage report"
	@echo "test                         - run unit tests"
	@echo "test TEST_FILE=<test_file>   - run all tests in file"
	@echo "install-pre-commit           - install pre-commit hooks"
	@echo "deploy-pypi                  - deploy to pypi"
