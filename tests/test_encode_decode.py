import pytest

from cqd.open_xpd_uuid import encode, decode


@pytest.mark.parametrize('number', (29, 1099511627775))
def test_encode_decode(number: int):
    encoded = encode(number)
    assert number == decode(encoded)
