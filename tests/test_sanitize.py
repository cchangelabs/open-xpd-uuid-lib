import pytest

from cqd.open_xpd_uuid import sanitize


def test_sanitize_no_action() -> None:
    """Test that a GUID without dashes, lowercase, or ambiguous characters remains unchanged."""
    assert sanitize("1U7XPGQ2") == "1U7XPGQ2"


def test_sanitize_remove_dashes() -> None:
    """Test that dashes are removed from the GUID."""
    assert sanitize("1U-7X-PG-Q2") == "1U7XPGQ2"


def test_sanitize_capitalize() -> None:
    """Test that ambiguous characters are replaced with their correct counterparts."""
    assert sanitize("1u7xpgq2") == "1U7XPGQ2"


@pytest.mark.parametrize(
    ("ambiguous_chars", "expected_char"),
    [
        ("0oO", "0"),
        ("1LliI", "1"),
    ],
)
def test_sanitize_ambiguous_chars(ambiguous_chars: str, expected_char: str) -> None:
    """Test that ambiguous characters are replaced with their correct counterparts."""
    for ambiguous_char in ambiguous_chars:
        assert sanitize(f"{ambiguous_char}u7xpgq2") == f"{expected_char}U7XPGQ2"
