import random

import pytest

from cqd.open_xpd_uuid import generate


@pytest.mark.parametrize(
    'numeric_id, short_code', (
            (1099511627775, 'ZZZZZZZZ'),
            (29, '0000000X'),
    ))
def test_generate(monkeypatch, numeric_id: int, short_code: str):
    def mock_randint(*args, **kwargs):
        return numeric_id

    monkeypatch.setattr(random, "randint", mock_randint)

    assert generate() == short_code


RANDINT_FROM = 437449129984
RANDINT_TO = 437482684415


@pytest.mark.parametrize(
    'numeric_id, short_code', (
            (RANDINT_FROM, 'CQD00000'),
            (437450247301, 'CQD12345'),
            (RANDINT_TO, 'CQDZZZZZ'),
    ))
def test_generate_with_prefix(monkeypatch, numeric_id: int, short_code: str):
    def mock_randint(a, b):
        assert a == RANDINT_FROM, 'Incorrect lower bound for `randint` passed'
        assert b == RANDINT_TO, 'Incorrect upper bound for `randint` passed'
        return numeric_id

    monkeypatch.setattr(random, "randint", mock_randint)

    assert generate('CQD') == short_code


def test_generate_with_z_prefix_is_not_allowed():
    with pytest.raises(ValueError) as excinfo:
        generate('Z')

    assert 'must not start with' in str(excinfo.value)
