from __future__ import annotations

import random
import re
from typing import Literal, overload

DICTIONARY = "0123456789ABCDEFGHJKMNPQRSTUWXYZ"
DICTIONARY_SIZE = len(DICTIONARY)
CODE_LENGTH = 8
# first `Z` is reserved for future
TOTAL_COMBINATIONS = (DICTIONARY_SIZE - 1) * DICTIONARY_SIZE ** (CODE_LENGTH - 1)

CHECKSUM_LENGTH = 2

OPEN_XPD_UUID_REGEX = r"(?:-*[A-Za-z0-9]){8}(?:(?:-*[A-Za-z0-9]){2})?-*"
"""Regex string that matches open xPD UUIDs in any accepted input form.

Matches values with exactly 8 or 10 alphanumeric characters and any number
of dashes. This includes lowercase and ambiguous letters that can be
normalized via `sanitize`.

The pattern is intentionally not anchored so users can decide whether to use
`re.fullmatch`, `re.search`, or `re.finditer`.

When using `re.search` or `re.finditer` for text extraction, callers must apply
token-boundary post-filtering (characters adjacent to a match must not be
alphanumeric or `-`) to avoid partial matches from longer tokens.
"""

OPEN_XPD_UUID_PATTERN = re.compile(OPEN_XPD_UUID_REGEX)
"""Compiled regex pattern that matches open xPD UUIDs in any accepted input form."""

CANONICAL_OPEN_XPD_UUID_REGEX = r"[0-9A-HJKMNPQRSTUWXYZ]{8}(?:[0-9A-HJKMNPQRSTUWXYZ]{2})?"
"""Regex string that matches canonical open xPD UUIDs.

Matches uppercase UUIDs with exactly 8 or 10 characters from the canonical
dictionary (`DICTIONARY`) and no dashes.

The pattern is intentionally not anchored so users can decide whether to use
`re.fullmatch`, `re.search`, or `re.finditer`.

When using `re.search` or `re.finditer` for text extraction, callers must apply
token-boundary post-filtering (characters adjacent to a match must not be
alphanumeric or `-`) to avoid partial matches from longer tokens.
"""

CANONICAL_OPEN_XPD_UUID_PATTERN = re.compile(CANONICAL_OPEN_XPD_UUID_REGEX)
"""Compiled regex pattern that matches canonical open xPD UUIDs."""


class GuidValidationError(Exception):
    """An error happened while validating short readable GUID."""


def encode(number: int) -> str:
    """Turn `number` into short readable GUID using encoding table.

    :param number: numeric id
    :return: guid.
    """
    if number < DICTIONARY_SIZE:
        return DICTIONARY[number]
    return encode(number // DICTIONARY_SIZE) + encode(number % DICTIONARY_SIZE)


def decode(guid: str) -> int:
    """Turn `guid` into number based on encoding table. Collisions are possible.

    :param guid: short readable GUID. Must be validated.
    :return: number.
    """
    x = 0
    for char in guid:
        x = x * DICTIONARY_SIZE + DICTIONARY.index(char)
    return x


def generate(prefix: str | None = None) -> str:
    """Generate a short readable GUID.

    The GUID is an 8-character alphanumeric string derived from a random number.
    Optionally, a prefix can be provided to constrain the GUID to start with the sanitized prefix.

    Example:
        ``generate()`` returns ``'1U7XPGQ2'``.
        ``generate('CQD')`` returns ``'CQD12345'``.

    :param prefix: A string to constrain the GUID to start with the sanitized prefix.
                   The prefix can be in any form (e.g., with dashes, lowercase, or ambiguous characters).
                   Cannot start with ``'Z'``.
    :return: A short readable GUID in canonical form.

    :raises ValueError: If the ``prefix`` starts with ``'Z'``.
    :raises GuidValidationError: If the ``prefix`` is not a valid short readable GUID.

    .. note::
        If you wish to issue your own openEPD IDs, you can request any three-symbol prefix that is not already
        reserved. "EC3" is reserved for BuildingTransparency.org, "EST" is reserved for generic estimates,
        "CQD" and "WAP" are reserved for WAP Sustainability, "PCR" is reserved for designating product category
        rules, and "UL" is reserved for UL Sustainability. To request your own prefix, please email
        open-epd-forum@c-change-labs.com.
    """
    randint_from = 0
    randint_to = TOTAL_COMBINATIONS
    if prefix:
        prefix = sanitize(prefix)
        validate(prefix.rjust(CODE_LENGTH, "0"))
        if prefix.startswith("Z"):
            msg = "`prefix` must not start with 'Z'"
            raise ValueError(msg)
        randint_from = decode(prefix.ljust(CODE_LENGTH, "0"))
        randint_to = decode(prefix.ljust(CODE_LENGTH, DICTIONARY[-1]))

    number = random.randint(randint_from, randint_to)
    result = encode(number)

    return result.rjust(CODE_LENGTH, "0")


def checksum(guid: str) -> str:
    """Generate a checksum for the given valid GUID.

    The checksum is a sequence of two uppercase alphanumeric characters derived from the GUID.
    It ensures the integrity of the GUID and can be used for validation purposes.

    Example:
        ``checksum('1U7XPGQ2')`` returns ``'3X'``.

    :param guid: The GUID in any form (e.g., with dashes, lowercase, or ambiguous characters).

    :return: A two-character checksum in canonical form.

    :raises ValueError: If the ``guid`` is not provided.
    :raises GuidValidationError: If the ``guid`` is not a valid short readable GUID.
    """
    guid = sanitize(guid)
    validate(guid)
    result = 403
    for i in range(1, CODE_LENGTH // CHECKSUM_LENGTH + 1):
        stop = i * CHECKSUM_LENGTH
        start = stop - CHECKSUM_LENGTH

        result += decode(guid[start:stop])

    return encode(result % 1024).rjust(CHECKSUM_LENGTH, "0")


@overload
def remove_checksum(guid: str) -> str: ...


@overload
def remove_checksum(guid: None) -> None: ...


def remove_checksum(guid: str | None) -> str | None:
    """Remove checksum from a canonical open xPD UUID.

    Accepts canonical UUIDs with or without checksum (8 or 10 chars), case-insensitively.
    Preserves the original casing of the passed UUID.
    The function assumes the input UUID is already valid and does not perform validation.

    Example:
        ``remove_checksum("EC3949XK04")`` returns ``"EC3949XK"``.
        ``remove_checksum("ec3949xk04")`` returns ``"ec3949xk"``.
        ``remove_checksum("EC3949XK")`` returns ``"EC3949XK"``.
        ``remove_checksum(None)`` returns ``None``.

    :param guid: Canonical open xPD UUID with or without checksum, or ``None``.
    :return: 8-character canonical UUID without checksum, or ``None`` if input is ``None``.
    """
    if guid is None:
        return None
    return guid[:CODE_LENGTH]


@overload
def canonical_without_checksum(guid: str, *, none_on_error: Literal[False] = False) -> str: ...


@overload
def canonical_without_checksum(guid: None, *, none_on_error: Literal[False] = False) -> None: ...


@overload
def canonical_without_checksum(guid: str | None, *, none_on_error: Literal[True]) -> str | None: ...


def canonical_without_checksum(guid: str | None, *, none_on_error: bool = False) -> str | None:
    """Return canonical 8-character UUID without checksum from any accepted UUID form.

    This is a convenience helper that combines ``sanitize``, ``validate``, and
    ``remove_checksum`` in one call:
    1. sanitizes accepted UUID input (removes dashes, normalizes ambiguous chars),
    2. validates canonical UUID (including checksum if present),
    3. removes checksum and returns the base 8-character UUID.

    Example:
        ``canonical_without_checksum("as-b2-lm-oL")`` returns ``"ASB21M01"``.
        ``canonical_without_checksum("EC3949XK04")`` returns ``"EC3949XK"``.
        ``canonical_without_checksum("invalid", none_on_error=True)`` returns ``None``.
        ``canonical_without_checksum(None)`` returns ``None``.

    :param guid: Open xPD UUID in any accepted form, or ``None``.
    :param none_on_error: If ``True``, return ``None`` for invalid UUID input
                          instead of raising validation errors.
    :return: 8-character canonical UUID without checksum, or ``None`` if input is ``None``.
    :raises ValueError: If ``guid`` is empty after sanitization.
    :raises GuidValidationError: If ``guid`` has invalid length, characters, or checksum.
    """
    if guid is None:
        return None
    try:
        canonical_guid = sanitize(guid)
        validate(canonical_guid)
        return remove_checksum(canonical_guid)
    except (GuidValidationError, ValueError):
        if none_on_error:
            return None
        raise


def sanitize(guid: str) -> str:
    """Remove dashes and replaces ambiguous characters.

    :param guid: guid with either dashes or lowercase letters or ambiguous letters
    :return: sanitized guid
    """
    if not guid:
        return ""
    return guid.replace("-", "").upper().replace("I", "1").replace("L", "1").replace("O", "0")


def validate(guid: str) -> None:
    """Validate whether passed `guid` is short readable GUID  for product declaration.

    :param guid: guid to validate. Must be sanitized. See `def sanitize()`.

    :raise ValueError: if `guid` is not passed.
    :raise GuidValidationError: if passed `guid` is not valid short readable GUID.
    """
    if not guid:
        msg = "`guid` argument must be passed"
        raise ValueError(msg)

    code_length_with_checksum = CODE_LENGTH + CHECKSUM_LENGTH
    if len(guid) not in {CODE_LENGTH, code_length_with_checksum}:
        msg = f"`guid` length must be {CODE_LENGTH} characters long"
        raise GuidValidationError(msg)
    invalid_chars = set()
    for char in guid:
        if char not in DICTIONARY:
            invalid_chars.add(char)
    if invalid_chars:
        msg = f"`{''.join(invalid_chars)}` characters are not allowed to be used in `guid`"
        raise GuidValidationError(msg)

    if len(guid) == code_length_with_checksum and checksum(guid[:CODE_LENGTH]) != guid[CODE_LENGTH:]:
        msg = "Checksum doesn't match"
        raise GuidValidationError(msg)
