# type: ignore
"""Tests for sophication.py.

TODO: write unit test for convert_str_to_int
"""

# Python Standard Library Imports
from typing import Any, List, Tuple

# Third Party Library Imports
import pytest
from colorama import Fore as fore_c, Back as back_c
try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

# Local Application/Library Imports
from sophication.sophication import \
    filter_tuple_list, \
    get_random_products, \
    get_random_table, \
    convert_str_to_int, \
    print_and_speak


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


def test_val_in_get_random_products() -> None:
    """Only specified random products should be returned."""
    max_vals = range(10)
    for max_val in max_vals:
        random_products = get_random_products(max_val)
        for test_val in range(max_val):
            assert any([test_val in rand_prod  # nosec
                        for rand_prod in random_products])


def test_val_not_in_get_random_products() -> None:
    """Values at or above max_val should not be returned."""
    max_vals = range(10)
    for max_val in max_vals:
        random_products = get_random_products(max_val)
        for test_val in range(max_val, 10):
            assert not any([test_val in rand_prod  # nosec
                            for rand_prod in random_products])


def test_get_random_table() -> None:
    """Values from include_list should be in returned values."""
    max_val = 10
    include_list = [1, 2, 3]
    return_list = get_random_table(include_list, max_val)
    for inc in include_list:
        assert any([bool_val for bool_val in  # nosec
                    [inc in ret_tup for ret_tup in return_list]])


@pytest.mark.parametrize(
    "test_input, expected",
    [("'1'", 1), ("'2'", 2), ("'3'", 3), ("'123456'", 123456),
     ("'Bad Value'", None), ("1", 1)]
)
def test_convert_str_to_int(test_input, expected) -> None:
    """Return str as int if possible, else return None."""
    assert convert_str_to_int(eval(test_input)) == expected  # nosec


@pytest.mark.parametrize(
    "test_input, expected",
    [("A", None), ("B", None), ("C", None)]
)
def test_convert_str_to_int_stdout(test_input: str, expected: None,
                                   capsys) -> None:
    """Print correct value to stdout."""
    # test_input = "A"
    assert convert_str_to_int(test_input) == expected  # nosec
    out, _ = capsys.readouterr()
    assert out == ''.join((f"{test_input} is not a valid input. ",  # nosec
                           "Please enter an integer\n"))


PRINT_AND_SPEAK_TEST_VALS = \
    [{'phrase': 'test phrase',
      'end': '\n',
      'replace_speech': ['', ''],
      'forecolor': None,
      'backcolor': None,
      'run_in_own_process': False,
      'return_val': 'test phrase',
      'stdout_val': 'test phrase\n'},
     {'phrase': 'test phrase to speak',
      'end': '!',
      'replace_speech': ['', ''],
      'forecolor': None,
      'backcolor': None,
      'run_in_own_process': False,
      'return_val': 'test phrase',
      'stdout_val': 'test phrase!'},
     {'phrase': 'test phrase',
      'end': '\n',
      'replace_speech': ['', ''],
      'forecolor': fore_c.RED,
      'backcolor': None,
      'run_in_own_process': False,
      'return_val': 'test phrase',
      'stdout_val': 'test phrase\n'}
     ]


@pytest.mark.parametrize(
    "test_input", PRINT_AND_SPEAK_TEST_VALS
)
def test_print_and_speak_phrase_spoken(test_input):
    """Test return value for print_and_speak function."""
    phrase = test_input.pop('phrase')
    return_val = test_input.pop('return_val')
    _ = test_input.pop('stdout_val')
    if pyttsx3 is not None:
        # Case when pyttsx3 can be imported
        assert return_val == print_and_speak(phrase, **test_input)  # nosec
    else:
        # Case when pyttsx3 cannot be imported
        assert None is print_and_speak(phrase, **test_input)  # nosec


@pytest.mark.parametrize(
    "test_input", PRINT_AND_SPEAK_TEST_VALS
)
def test_print_and_speak_phrase_printed(test_input, capsys):
    """Test phrase printed to stdout."""
    phrase = test_input.pop('phrase')
    _ = test_input.pop('return_val')
    stdout_val = test_input.pop('stdout_val')
    _ = print_and_speak(phrase, **test_input)
    out, _ = capsys.readouterr()
    assert out == stdout_val  # nosec
