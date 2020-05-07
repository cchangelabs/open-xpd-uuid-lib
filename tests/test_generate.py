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
