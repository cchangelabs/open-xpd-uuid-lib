import pytest

from cqd.open_xpd_uuid import checksum


@pytest.mark.parametrize(
    'guid, expected_checksum', (
            ('00000000', 'CK'),
            ('10000000', 'DK'),
            ('ZZZZZZZZ', 'CF'),
            ('12345678', 'X7'),
    ))
def test_checksum(guid: str, expected_checksum: str):
    assert checksum(guid) == expected_checksum
