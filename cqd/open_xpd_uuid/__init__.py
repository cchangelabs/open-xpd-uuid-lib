import random

DICTIONARY = '0123456789ABCDEFGHJKMNPQRSTUWXYZ'
DICTIONARY_SIZE = len(DICTIONARY)
CODE_LENGTH = 8
# first `Z` is reserved for future
TOTAL_COMBINATIONS = (DICTIONARY_SIZE - 1) * DICTIONARY_SIZE ** (CODE_LENGTH - 1)


def encode(number: int) -> str:
    """
    Turns `number` into short readable GUID using encoding table.
    :param number: numeric id 
    :return: guid
    """
    if number < DICTIONARY_SIZE:
        return DICTIONARY[number]
    return encode(number // DICTIONARY_SIZE) + encode(number % DICTIONARY_SIZE)


def decode(guid: str) -> str:
    """
    Turns `guid` into number based on encoding table. Collisions are possible.
    :param guid: short readable GUID. Must be validated.
    :return: number
    """
    x = 0
    for char in guid:
        x = x * DICTIONARY_SIZE + DICTIONARY.index(char)
    return x


def generate() -> str:
    """
    Generates short readable GUID.

    It doesn't generate guids starting with 'Z_______'.

    :return: guid
    """
    number = random.randint(0, TOTAL_COMBINATIONS)
    result = encode(number)

    return result.rjust(CODE_LENGTH, '0')


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


def validate(guid: str) -> bool:
    """
    Validates whether passed `guid` is short readable GUID  for product declaration.
    :param guid: guid to validate. Must be sanitized. See `def sanitize()`.
    :return: True if passed `guid` is valid, False otherwise
    """
    # TODO: not implemented yet
    pass
