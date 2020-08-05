import random

DICTIONARY = '0123456789ABCDEFGHJKMNPQRSTUWXYZ'
DICTIONARY_SIZE = len(DICTIONARY)
CODE_LENGTH = 8
# first `Z` is reserved for future
TOTAL_COMBINATIONS = (DICTIONARY_SIZE - 1) * DICTIONARY_SIZE ** (CODE_LENGTH - 1)

CHECKSUM_LENGTH = 2


class GuidValidationError(Exception):
    """An error happened while validating short readable GUID"""
    pass


def encode(number: int) -> str:
    """
    Turns `number` into short readable GUID using encoding table.
    :param number: numeric id 
    :return: guid
    """
    if number < DICTIONARY_SIZE:
        return DICTIONARY[number]
    return encode(number // DICTIONARY_SIZE) + encode(number % DICTIONARY_SIZE)


def decode(guid: str) -> int:
    """
    Turns `guid` into number based on encoding table. Collisions are possible.
    :param guid: short readable GUID. Must be validated.
    :return: number
    """
    x = 0
    for char in guid:
        x = x * DICTIONARY_SIZE + DICTIONARY.index(char)
    return x


def generate(prefix: str = None) -> str:
    """
    Generates short readable GUID.

    It doesn't generate guids starting with 'Z_______'.

    :param prefix: prefix in canonical form.
                It forces this function to generate guids that start with the `prefix`. Cannot start with 'Z'.
    :return: guid
    """
    randint_from = 0
    randint_to = TOTAL_COMBINATIONS
    if prefix:
        if prefix.startswith('Z'):
            raise ValueError("`prefix` must not start with 'Z'")
        randint_from = decode(prefix.ljust(CODE_LENGTH, '0'))
        randint_to = decode(prefix.ljust(CODE_LENGTH, DICTIONARY[-1]))

    number = random.randint(randint_from, randint_to)
    result = encode(number)

    return result.rjust(CODE_LENGTH, '0')


def checksum(guid: str) -> str:
    """
    Generates checksum for passed "canonical" `guid`.
    Checksum is a sequence of two UPPER-case alphanumeric characters that are also allowed `guid` characters.
    For example: "JR", "CK", "00", "1F".

    `checksum('1U7XPGQ2') == '3X'`

    :param guid: guid in canonical form
    :return: two-letter checksum
    """
    result = 403
    for i in range(1, CODE_LENGTH // CHECKSUM_LENGTH + 1):
        stop = i * CHECKSUM_LENGTH
        start = stop - CHECKSUM_LENGTH

        result += decode(guid[start:stop])

    return encode(result % 1024)


def sanitize(guid: str) -> str:
    """
    Removes dashes and replaces ambiguous characters

    :param guid: guid with either dashes or lowercase letters or ambiguous letters
    :return: sanitized guid
    """
    if not guid:
        return ''
    guid = guid.replace('-', '').upper().replace('I', '1').replace('L', '1').replace('O', '0')
    return guid


def validate(guid: str):
    """
    Validates whether passed `guid` is short readable GUID  for product declaration.
    :param guid: guid to validate. Must be sanitized. See `def sanitize()`.

    :raise ValueError: if `guid` is not passed.
    :raise GuidValidationError: if passed `guid` is not valid short readable GUID.
    """
    if not guid:
        raise ValueError('`guid` argument must be passed')

    code_length_with_checksum = CODE_LENGTH + CHECKSUM_LENGTH
    if len(guid) not in {CODE_LENGTH, code_length_with_checksum}:
        raise GuidValidationError(f'`guid` length must be {CODE_LENGTH} characters long')
    invalid_chars = set()
    for char in guid:
        if char not in DICTIONARY:
            invalid_chars.add(char)
    if invalid_chars:
        raise GuidValidationError(f'`{"".join(invalid_chars)}` characters are not allowed to be used in `guid`')

    if len(guid) == code_length_with_checksum:
        if checksum(guid[:CODE_LENGTH]) != guid[CODE_LENGTH:]:
            raise GuidValidationError("Checksum doesn't match")
