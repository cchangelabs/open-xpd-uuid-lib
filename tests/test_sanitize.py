import pytest

from cqd.open_xpd_uuid import sanitize


@pytest.mark.parametrize(
    'guid, expected', (
            ('1U7XPGQ2', '1U7XPGQ2'),
            ('1u7xpgq2', '1U7XPGQ2'),
            ('lU7XPGQ2', '1U7XPGQ2'),
            ('1U-7X-PG-Q2', '1U7XPGQ2'),
    ))
def test_sanitize(guid: str, expected: str):
    assert sanitize(guid) == expected
