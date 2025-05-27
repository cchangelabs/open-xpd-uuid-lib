import pytest

from cqd.open_xpd_uuid import GuidValidationError, validate


def test_validate_positive() -> None:
    """Test that a valid GUID passes validation."""
    validate("XPDFHRTR")


@pytest.mark.parametrize("guid", ["1234567", "123456789"])
def test_validate_invalid_length(guid: str) -> None:
    """Test that a valid GUID passes validation."""
    with pytest.raises(GuidValidationError, match=r"`guid` length must be \d+ characters long"):
        validate(guid)


def test_validate_invalid_characters() -> None:
    """Test that GUIDs with invalid characters raise a GuidValidationError."""
    with pytest.raises(
        GuidValidationError,
        match=r"`[-*Li]{4}` characters are not allowed to be used in `guid`",
    ):
        validate("-X-X*XLi")


def test_validate_good_checksum() -> None:
    """Test that a GUID with a valid checksum passes validation."""
    validate("00000000CK")


def test_validate_bad_checksum() -> None:
    """Test that a GUID with an invalid checksum raises a GuidValidationError."""
    with pytest.raises(GuidValidationError, match="Checksum doesn't match"):
        validate("00000000CA")
