import re

import pytest

from cqd.open_xpd_uuid import (
    CANONICAL_OPEN_XPD_UUID_PATTERN,
    CANONICAL_OPEN_XPD_UUID_REGEX,
    OPEN_XPD_UUID_PATTERN,
    OPEN_XPD_UUID_REGEX,
)


@pytest.mark.parametrize(
    "guid",
    [
        "123ABCED",
        "123ABCEDAR",
        "ASB21M01",
        "avbDK93S",
        "-AB-11-cc-Ll---",
    ],
)
def test_open_xpd_uuid_regex_matches_valid_guids(guid: str) -> None:
    """Test that open xPD UUID regex constants match valid non-canonical and canonical GUIDs."""
    assert re.fullmatch(OPEN_XPD_UUID_REGEX, guid)
    assert OPEN_XPD_UUID_PATTERN.fullmatch(guid)


@pytest.mark.parametrize(
    "guid",
    [
        "",
        "1234567",
        "123456789",
        "12345678901",
        "1234_5678",
        "1234 5678",
        "1234/5678",
    ],
)
def test_open_xpd_uuid_regex_rejects_invalid_guids(guid: str) -> None:
    """Test that open xPD UUID regex constants reject invalid GUIDs."""
    assert not re.fullmatch(OPEN_XPD_UUID_REGEX, guid)
    assert not OPEN_XPD_UUID_PATTERN.fullmatch(guid)


@pytest.mark.parametrize(
    "guid",
    [
        "12345678",
        "ABCDEFG1",
        "123ABCEDAR",
        "ASB21M01",
    ],
)
def test_canonical_open_xpd_uuid_regex_matches_valid_guids(guid: str) -> None:
    """Test that canonical open xPD UUID regex constants match valid canonical GUIDs."""
    assert re.fullmatch(CANONICAL_OPEN_XPD_UUID_REGEX, guid)
    assert CANONICAL_OPEN_XPD_UUID_PATTERN.fullmatch(guid)


@pytest.mark.parametrize(
    "guid",
    [
        "",
        "avbDK93S",
        "AB-11CCLL",
        "ABCDEFGHJ",
        "123456789",
        "ABCDVFG1",
    ],
)
def test_canonical_open_xpd_uuid_regex_rejects_invalid_guids(guid: str) -> None:
    """Test that canonical open xPD UUID regex constants reject invalid GUIDs."""
    assert not re.fullmatch(CANONICAL_OPEN_XPD_UUID_REGEX, guid)
    assert not CANONICAL_OPEN_XPD_UUID_PATTERN.fullmatch(guid)


def test_open_xpd_uuid_pattern_extracts_guids_from_text() -> None:
    """Test that open xPD UUID pattern can be used for extraction from plain text."""
    text = "IDs: 123ABCED, -AB-11-cc-Ll--- and invalid 1234_5678"
    matches = [match.group(0) for match in OPEN_XPD_UUID_PATTERN.finditer(text)]

    assert matches == ["123ABCED", "-AB-11-cc-Ll---"]


def test_open_xpd_uuid_pattern_extraction_requires_boundary_post_filtering() -> None:
    """Test boundary post-filtering requirement for text extraction with regex constants."""
    text = "invalid 12345678901 and valid 1234567890"
    token_chars = set("-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")

    def has_token_boundaries(match: re.Match[str]) -> bool:
        start, end = match.span()
        previous_char = text[start - 1] if start > 0 else ""
        next_char = text[end] if end < len(text) else ""
        return previous_char not in token_chars and next_char not in token_chars

    raw_matches = [match.group(0) for match in OPEN_XPD_UUID_PATTERN.finditer(text)]
    filtered_matches = [match.group(0) for match in OPEN_XPD_UUID_PATTERN.finditer(text) if has_token_boundaries(match)]

    assert raw_matches == ["1234567890", "1234567890"]
    assert filtered_matches == ["1234567890"]
