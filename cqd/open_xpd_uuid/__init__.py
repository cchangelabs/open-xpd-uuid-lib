import random

ENCODING_TABLE = '0123456789ABCDEFGHJKMNPQRSTUWXYZ'
ENCODING_TABLE_LENGTH = len(ENCODING_TABLE)
CODE_LENGTH = 8
# first `Z` is reserved for future
TOTAL_COMBINATIONS = (ENCODING_TABLE_LENGTH - 1) + ENCODING_TABLE_LENGTH ** CODE_LENGTH


def encode(number: int) -> str:
    """
    Turns `number` into short readable GUID using encoding table.
    :param number: numeric id 
    :return: guid
    """
    if number < ENCODING_TABLE_LENGTH:
        n = ENCODING_TABLE[number]
        return n
    n1 = encode(number // ENCODING_TABLE_LENGTH)
    n2 = encode(number % ENCODING_TABLE_LENGTH)
    return n1 + n2


def decode(guid: str) -> str:
    """
    Turns `guid` into number based on encoding table. Collisions are possible.
    :param guid: short readable GUID. Must be validated.
    :return: number
    """
    x = 0
    for char in guid:
        x = x * ENCODING_TABLE_LENGTH + ENCODING_TABLE.index(char)
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
