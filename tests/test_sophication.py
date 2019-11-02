"""Tests for sophication.py."""

# Python Standard Library Imports
# NONE

# Third Party Library Imports
from typing import Any, List, Tuple

# Local Application/Library Imports
from sophication import filter_tuple_list


def test_filter_tuple_list() -> None:
    """Only tuples containing the correct integers should pass the filter."""
    include_list: List[int] = [1, 5]
    tuple_list: List[Tuple[Any, ...]] = [(1, 2), (3, 4), (5, 6)]
    tuple_list = filter_tuple_list(include_list, tuple_list)
    valid: bool = True
    for this_tuple in tuple_list:
        if ((include_list[0] not in this_tuple) and
                (include_list[1] not in this_tuple)):
            valid = False
            break
    assert valid  # nosec


# TODO: write unit test for get_random_table
# TODO: write unit test for convert_str_to_int
