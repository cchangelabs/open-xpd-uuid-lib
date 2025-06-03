import pytest

from cqd.open_xpd_uuid import checksum


@pytest.mark.parametrize(
    ("guid", "expected_checksum"),
    [
        ("00000000", "CK"),
        ("10000000", "DK"),
        ("ZZZZZZZZ", "CF"),
        ("12345678", "X7"),
        ("EC3949XK", "04"),
        ("ec3949-xk", "04"),
    ],
)
def test_checksum(guid: str, expected_checksum: str) -> None:
    """Test that the `checksum` function computes the correct checksum for a given GUID."""
    assert checksum(guid) == expected_checksum
