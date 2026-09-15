from __future__ import annotations

import pytest

from cqd.open_xpd_uuid import remove_checksum


@pytest.mark.parametrize(
    ("guid", "expected"),
    [
        ("EC3949XK04", "EC3949XK"),
        ("ec3949xk04", "ec3949xk"),
        ("EC3949XK", "EC3949XK"),
        ("ec3949xk", "ec3949xk"),
        (None, None),
    ],
)
def test_remove_checksum(guid: str | None, expected: str | None) -> None:
    """Test that checksum is removed from canonical UUIDs and None is accepted."""
    assert remove_checksum(guid) == expected
