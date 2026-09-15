from __future__ import annotations

import pytest

from cqd.open_xpd_uuid import GuidValidationError, canonical_without_checksum


@pytest.mark.parametrize(
    ("guid", "expected"),
    [
        ("as-b2-lm-oL", "ASB21M01"),
        ("EC3949XK04", "EC3949XK"),
        ("ec3949xk04", "EC3949XK"),
        ("EC3949XK", "EC3949XK"),
        (None, None),
    ],
)
def test_canonical_without_checksum(guid: str | None, expected: str | None) -> None:
    """Test that any accepted UUID form is canonicalized and checksum is removed."""
    assert canonical_without_checksum(guid) == expected


@pytest.mark.parametrize(
    "guid",
    [
        "1234567",
        "ABCDE_FG",
        "EC3949XK00",
    ],
)
def test_canonical_without_checksum_invalid(guid: str) -> None:
    """Test that invalid UUIDs are rejected."""
    with pytest.raises(GuidValidationError):
        canonical_without_checksum(guid)


@pytest.mark.parametrize(
    ("guid", "expected"),
    [
        ("1234567", None),
        ("ABCDE_FG", None),
        ("EC3949XK00", None),
        ("as-b2-lm-oL", "ASB21M01"),
        ("----", None),
    ],
)
def test_canonical_without_checksum_none_on_error(guid: str, expected: str | None) -> None:
    """Test that validation errors can be suppressed and return None."""
    assert canonical_without_checksum(guid, none_on_error=True) == expected
