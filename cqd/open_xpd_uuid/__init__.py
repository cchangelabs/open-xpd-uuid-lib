from __future__ import annotations

import random

DICTIONARY = "0123456789ABCDEFGHJKMNPQRSTUWXYZ"
DICTIONARY_SIZE = len(DICTIONARY)
CODE_LENGTH = 8
# first `Z` is reserved for future
TOTAL_COMBINATIONS = (DICTIONARY_SIZE - 1) * DICTIONARY_SIZE ** (CODE_LENGTH - 1)

CHECKSUM_LENGTH = 2


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
