import pytest

from cqd.open_xpd_uuid import sanitize


def test_sanitize_no_action():
    assert sanitize('1U7XPGQ2') == '1U7XPGQ2'


def test_sanitize_remove_dashes():
    assert sanitize('1U-7X-PG-Q2') == '1U7XPGQ2'


def test_sanitize_capitalize():
    assert sanitize('1u7xpgq2') == '1U7XPGQ2'


@pytest.mark.parametrize(
    'ambiguous_chars, expected_char', (
            ('0oO', '0'),
            ('1LliI', '1'),
    ))
def test_sanitize_ambiguous_chars(ambiguous_chars: str, expected_char: str):
    for ambiguous_char in ambiguous_chars:
        assert sanitize(f'{ambiguous_char}u7xpgq2') == f'{expected_char}U7XPGQ2'
