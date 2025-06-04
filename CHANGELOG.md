# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 1.0.0 (2025-06-04)

### BREAKING CHANGE

- Removed support for Python 3.6, 3.7, and 3.8.

### Feat

- add support for non-canonical prefixes in `generate` function
- allow non-canonical `guid` formats in `checksum` function
- drop Python 3.6-3.8 support, add 3.9-3.13 compatibility

## 0.2.1 (2020-09-07)

### Fix

- Justify single-char checksums to two-char ones.

## 0.2.0 (2020-08-05)

### Feat

- Extend `generate` function with `prefix` argument.

## 0.1.0 (2020-06-09)

### Feat

- Implement `checksum` function.

## 0.0.1 (2020-05-14)

### Feat

- Initial version.