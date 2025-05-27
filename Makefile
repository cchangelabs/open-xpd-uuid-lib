VIRTUAL_ENV_PATH=venv
SKIP_VENV="${NO_VENV}"
SHELL := /bin/bash
PYTHON := python3.9

POETRY ?= poetry
POETRY_GROUPS := dev

MYPY_PATH := "./cqd"

# Helper function to activate virtual environment if not skipped
define activate_venv
  if [ -z $(SKIP_VENV) ]; then source $(VIRTUAL_ENV_PATH)/bin/activate; fi;
endef

# Default target to run if no target is specified
.DEFAULT_GOAL := pre_commit

verify-prerequisites:
	@(development/ensure-dependencies.sh)

# Create a virtual environment
.PHONY: venv
venv:
	@set -e; \
	$(PYTHON) -m venv $(VIRTUAL_ENV_PATH); \
	source $(VIRTUAL_ENV_PATH)/bin/activate;

# Install dependencies listed in pyproject.toml for local development
.PHONY: deps
deps:
	@set -e; \
	$(call activate_venv) \
	echo "Installing dependencies..."; \
	$(POETRY) install --all-extras --no-root --with "$(POETRY_GROUPS)"; \
	echo "DONE: all dependencies are installed";

# Lock dependencies without updating them
.PHONY: deps-lock
deps-lock:
	@( \
		$(call activate_venv) \
		echo "Locking dependencies..."; \
		$(POETRY) lock; \
		echo "DONE: all dependencies are locked"; \
	)

# Synchronize installed dependencies to match the lock file
.PHONY: deps-sync
deps-sync:
	@( \
		$(call activate_venv) \
		set -e; \
		echo "Syncing dependencies..."; \
		$(POETRY) sync --all-extras --no-root --with "$(POETRY_GROUPS)"; \
		echo "DONE: all dependencies are synchronized"; \
	)

# Update a specific dependency
.PHONY: deps-update-dep
deps-update-dep:
	@set -e; \
	$(call activate_venv) \
	echo "Updating dependency $(DEPENDENCY)..."; \
	$(POETRY) update $(DEPENDENCY) --with "$(POETRY_GROUPS)"; \
	echo "DONE: dependency $(DEPENDENCY) is updated";

# Update all dependencies
.PHONY: deps-update-all
deps-update-all:
	@set -e; \
	$(call activate_venv) \
	echo "Updating dependencies..."; \
	$(POETRY) update --with "$(POETRY_GROUPS)"; \
	echo "DONE: all dependencies are updated";

# Show dependencies tree
.PHONY: deps-tree
deps-tree:
	@( \
		$(call activate_venv) \
		echo "Showing dependencies tree..."; \
		$(POETRY) show --tree --with "$(POETRY_GROUPS)"; \
	)

# Prepare the development environment.
# This target should be run only once after cloning the repository.
.PHONY: setup
setup: verify-prerequisites venv deps
	 @set -e; \
	 $(call activate_venv) \
	 pre-commit install; \
	 echo "Pre-commit hooks installed"; \
	 echo "DONE: setup";

# Run pre-commit hooks
.PHONY: pre_commit_hook lint
pre_commit_hook:
	 @set -e; \
	 $(call activate_venv) \
	 echo "Running pre-commit hooks..."; \
	 pre-commit run --all-files --hook-stage commit; \
	 echo "DONE: pre-commit hooks";

# Run commands required before committing code
pre_commit: pre_commit_hook lint


# Format code using ruff
.PHONY: ruff-format
ruff-format:
	@set -e; \
	$(call activate_venv) \
	echo "Running Ruff code formatter..."; \
	ruff format; \
	echo "DONE: Ruff"

# Check code formatting using ruff
ruff-format-check:
	 @( \
		$(call activate_venv) \
		echo "Running Ruff format check..."; \
		ruff format --check $(FORMAT_PATH); \
		echo "DONE: Ruff"; \
	 )

# Sort imports using ruff
.PHONY: ruff-import-sort
ruff-import-sort:
	@set -e; \
	$(call activate_venv) \
	echo "Running Ruff import sort..."; \
	ruff check --select I --fix --exit-zero; \
	echo "DONE: Ruff"

# Lint code using Ruff
# Use the `RUFF_OUTPUT_FORMAT` environment variable to override the default output format.
# Examples:
# - `RUFF_OUTPUT_FORMAT=junit make ruff-lint` for TeamCity integration.
# - `RUFF_OUTPUT_FORMAT=json-lines make ruff-lint` for IDEs like PyCharm, which highlights filenames as clickable links.
.PHONY: ruff-lint
ruff-lint:
	 @set -e; \
	 $(call activate_venv) \
	 echo "Running Ruff lint..."; \
	 ruff check || exit 1; \
	 echo "DONE: Ruff";

# Lint code using MyPy
.PHONY: mypy
mypy:
	 @set -e; \
	 $(call activate_venv) \
	 echo "Running MyPy..."; \
	 mypy $(MYPY_PATH); \
	 echo "DONE: MyPy";


# Format code and sort imports
.PHONY: format
format: ruff-import-sort ruff-format

# Check code formatting and import sorting
.PHONY: check-format
check-format: ruff-format-check

# Lint code
.PHONY: lint
lint: ruff-lint mypy check-format

# Run the test suite.
# This target activates the virtual environment (if not skipped)
# and uses pytest to execute all tests in verbose mode.
.PHONY: test
test:
	@( \
		echo "Running tests"; \
		set -e; \
		 $(call activate_venv) \
		pytest -v; \
		echo "DONE: Tests"; \
	)

# Run the tox test environments.
# This target uses tox to execute tests across multiple environments.
.PHONY: tox
tox:
	@( \
		echo "Running tox"; \
		set -e; \
		tox; \
		echo "DONE: Running tox"; \
	)



# Build distributable packages for the project.
# This target removes old build artifacts, activates the virtual environment (if not skipped),
# and uses Poetry to create new packages in the `dist` directory.
.PHONY: build
build:
	 @set -e; \
	 echo "Building packages..."; \
	 $(call activate_venv) \
	 rm -rf dist/*; \
	 $(POETRY) build; \
	 echo "DONE: Building packages";

# Publish the package to the Test PyPI repository.
# This target builds the package, activates the virtual environment (if not skipped),
# and uses Poetry to publish the package to the Test PyPI repository.
.PHONY: test-publish
test-publish: build
	@( \
		set -e; \
		echo "Publishing packages to the TEST PYPI"; \
	 	$(call activate_venv) \
		$(POETRY) publish -r test-pypi; \
		echo "DONE: Publishing packages (TEST PYPI)"; \
	)

# Publish the package to the official PyPI repository.
# This target builds the package, activates the virtual environment (if not skipped),
# and uses Poetry to publish the package to PyPI.
.PHONY: publish
publish: build
	@( \
		echo "Publishing packages"; \
		set -e; \
	 	$(call activate_venv) \
		$(POETRY) publish; \
		echo "DONE: Publishing packages"; \
	)
