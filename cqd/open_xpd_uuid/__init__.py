# TODO: under construction

def generate() -> str:
    """
    Generates short readable GUID.
    :return: guid
    """
    pass


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
    pass
