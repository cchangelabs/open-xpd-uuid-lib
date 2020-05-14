# Contribution Guide

## Development Environment
1. Install [python3.6](https://www.python.org/downloads/) for your operating system;
1. OPTIONAL: you can install more python versions e.g. 3.7 and 3.8 to use `tox`;
1. Install [pipenv](https://pypi.org/project/pipenv/);

1. Clone or download repository: `git clone git@github.com:cchangelabs/open-xpd-uuid-lib.git`;
1. Got to project folder: `cd open-xpd-uuid-lib`;
1. Install dependencies: `pipenv install --dev`;
1. `pipenv shell`.

## Run Tests
1. Got to project folder: `cd open-xpd-uuid-lib`;
1. `pipenv shell`;
1. `pytest` or `tox`.

alternatives:
* `pipenv run pytest`

## Packaging
1. `python3 setup.py sdist bdist_wheel`

## Publish package on PyPI
1. Install twine: `python3 -m pip install --user --upgrade twine`
1. `python3 -m twine upload dist/*`