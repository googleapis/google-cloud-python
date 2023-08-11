import pytest

import bigframes.formatting_helpers as formatter


@pytest.mark.parametrize(
    "test_input, expected", [(None, "N/A"), ("string", "N/A"), (100000, "100.0 kB")]
)
def test_get_formatted_bytes(test_input, expected):
    assert formatter.get_formatted_bytes(test_input) == expected


@pytest.mark.parametrize(
    "test_input, expected", [(None, None), ("string", "string"), (100000, "a minute")]
)
def test_get_formatted_time(test_input, expected):
    assert formatter.get_formatted_time(test_input) == expected
