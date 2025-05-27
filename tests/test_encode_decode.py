import pytest

from cqd.open_xpd_uuid import decode, encode


@pytest.mark.parametrize("number", [29, 1099511627775])
def test_encode_decode(number: int) -> None:
    """Test that encoding and then decoding a number returns the original number."""
    encoded = encode(number)
    assert number == decode(encoded)
