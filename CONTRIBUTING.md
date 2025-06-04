# Contribution Guide

Thank you for your interest in contributing to the project! 
This guide will help you set up your development environment, run tests, and contribute effectively.

---

## Table of Contents
1. [Getting Started](#getting-started)
2. [Development Environment Setup](#development-environment-setup)
3. [Running Tests](#running-tests)
4. [Using Tox](#using-tox)
5. [Preparing a Release](#preparing-a-release)
6. [Building and Publishing the Package](#building-and-publishing-the-package)
7. [Code of Conduct](#code-of-conduct)
8. [Submitting Changes](#submitting-changes)

---

## Getting Started

1. Fork the repository on GitHub.
2. Clone your forked repository:
    ```bash
    git clone git@github.com:<your-username>/open-xpd-uuid-lib.git
    ```
3. Create a new branch for your changes:
    ```bash
    git checkout -b feature/your-feature-name
    ```

---

## Development Environment Setup

1. **Recommended OS**: Use a Unix-based operating system (Linux or macOS).
2. **Install Prerequisites**:
   - [pyenv](https://github.com/pyenv/pyenv#installation) for managing Python versions.
   - [GNU Make](https://www.gnu.org/software/make/#download) (usually pre-installed on most systems).
   - [Poetry 2.x](https://python-poetry.org/docs/#installation) for dependency management.
3. **Install Python 3.9**:
    ```bash
    pyenv install 3.9
    ```
   If Python 3.9 is not available, update pyenv:
    ```bash
    pyenv update
    ```
4. **Set Up the Project**:
    ```bash
    cd open-xpd-uuid-lib
    make setup
    ```
   This will create a virtual environment and install all dependencies.

---

## Running Tests

To run the test suite, use one of the following methods:

1. Using `make`:
    ```bash
    make test
    ```
2. Using Poetry directly:
    ```bash
    poetry run pytest
    ```

---

## Using Tox

Tox is used to test the project across multiple Python versions.

1. **Install Tox**:
    ```bash
    pipx install tox
    ```
2. **Make Python Versions Available**:
    ```bash
    pyenv install 3.9 3.10 3.11 3.12 3.13
    pyenv local 3.9 3.10 3.11 3.12 3.13
    ```
3. **Run Tox**:
    ```bash
    make tox
    ```

---

## Preparing a Release

1. Prepare release commit and tag:
    ```bash
    make release
    ```
2. Push the changes and tags:
    ```bash
    git push origin --tags
    ```
3. Merge the `development` branch into `master`:
    ```bash
    git checkout master
    git merge development
    git push origin master
    ```

---

## Building and Publishing the Package

1. **Build the Package**:
    ```bash
    make build
    ```
   This will create a `dist` folder with the package.
2. **Publish to PyPI**:
    - For Test PyPI:
        ```bash
        make test-publish
        ```
    - For Production PyPI:
        ```bash
        make publish
        ```

---

## Submitting Changes

1. Ensure your changes pass all tests:
    ```bash
    make tox
    ```
2. Push your branch to your fork:
    ```bash
    git push origin feature/your-feature-name
    ```
3. Open a pull request on GitHub and describe your changes.

---

Thank you for contributing!