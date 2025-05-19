# Contribution Guide

## Development Environment
1. Install [pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation).
    This is needed to manage multiple python versions;
2. Install `python3.9` via `pyenv`:
    ```bash
    pyenv install 3.9
    ```
   If `3.9` in pyenv is not available, then `pyenv update` and try again;
1. Install [pipenv](https://pypi.org/project/pipenv/);
1. Clone or download repository: `git clone git@github.com:cchangelabs/open-xpd-uuid-lib.git`;
1. Make sure you are in `development` branch;
1. Go to project folder: `cd open-xpd-uuid-lib`;
1. Install dependencies: `pipenv install --dev`;
1. `pipenv shell`.

## Run Tests
1. Go to project folder: `cd open-xpd-uuid-lib`;
1. `pipenv shell`;
1. `pytest`.

alternatives:
* `pipenv run pytest`

### Tox
1. Install [`tox`](https://tox.wiki/en/4.26.0/installation.html):
    ```bash
    pipx install tox
    ```
2. Make python versions available for `tox`:
    ```bash
    pyenv install 3.9 3.10 3.11 3.12 3.13
    pyenv local 3.9 3.10 3.11 3.12 3.13
    ```
3. Run `tox`:
    ```bash
    tox
    ```

## Prepare release
1. Change version in `CHANGELOG.md`
1. Change version in `setup.py`
1. Commit modified files with the following message: `bump version: <major.minor.revision>`. 
For example `bump version: 0.1.0`.
1. Tag the commit `git tag 0.1.0`
1. Push changes and tags `git push origin --tags`
1. Merge `development` branch into `master`

## Packaging
1. `python3 setup.py sdist bdist_wheel`

## Publish package on PyPI
1. Install twine: `python3 -m pip install --user --upgrade twine`
1. `python3 -m twine upload dist/*`