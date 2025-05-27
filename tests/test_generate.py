import random

import pytest

from cqd.open_xpd_uuid import generate


@pytest.mark.parametrize(
    ("numeric_id", "short_code"),
    [
        (1099511627775, "ZZZZZZZZ"),
        (29, "0000000X"),
    ],
)
def test_generate(monkeypatch: pytest.MonkeyPatch, numeric_id: int, short_code: str) -> None:
    """Test that `generate` produces the correct short code for given numeric IDs."""

    def mock_randint(a: int, b: int) -> int:
        return numeric_id

    monkeypatch.setattr(random, "randint", mock_randint)

    assert generate() == short_code


RANDINT_FROM = 437449129984
RANDINT_TO = 437482684415


@pytest.mark.parametrize(
    ("numeric_id", "short_code"),
    [
        (RANDINT_FROM, "CQD00000"),
        (437450247301, "CQD12345"),
        (RANDINT_TO, "CQDZZZZZ"),
    ],
)
def test_generate_with_prefix(monkeypatch: pytest.MonkeyPatch, numeric_id: int, short_code: str) -> None:
    """Test that `generate` produces the correct short code with a given prefix."""

    def mock_randint(a: int, b: int) -> int:
        assert a == RANDINT_FROM, "Incorrect lower bound for `randint` passed"
        assert b == RANDINT_TO, "Incorrect upper bound for `randint` passed"
        return numeric_id

    monkeypatch.setattr(random, "randint", mock_randint)

    assert generate("CQD") == short_code


def test_generate_with_z_prefix_is_not_allowed() -> None:
    """Test that `generate` raises a ValueError when the prefix starts with 'Z'."""
    with pytest.raises(ValueError) as excinfo:  # noqa: PT011
        generate("Z")

    assert "must not start with" in str(excinfo.value)
