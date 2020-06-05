import pytest

from cqd.open_xpd_uuid import validate, GuidValidationError


def test_validate_positive():
    validate('XPDFHRTR')


@pytest.mark.parametrize('guid', ('1234567', '123456789'))
def test_validate_invalid_length(guid: str):
    with pytest.raises(GuidValidationError, match=r'`guid` length must be \d+ characters long'):
        validate(guid)


def test_validate_invalid_characters():
    with pytest.raises(GuidValidationError, match=r'`[-*Li]{4}` characters are not allowed to be used in `guid`'):
        validate('-X-X*XLi')


def test_validate_good_checksum():
    validate('00000000CK')


def test_validate_bad_checksum():
    with pytest.raises(GuidValidationError, match="Checksum doesn't match"):
        validate('00000000CA')
