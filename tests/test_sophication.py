# type: ignore
"""Tests for sophication.py.

TODO: write unit test for convert_str_to_int
"""

# Python Standard Library Imports
from typing import Any, List, Tuple
from inspect import signature

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


def test_get_random_table() -> None:
    """Values from include_list should be in returned values."""
    max_val = 10
    include_list = [1, 2, 3]
    return_list = get_random_table(include_list, max_val)
    for inc in include_list:
        assert any([bool_val for bool_val in  # nosec
                    [inc in ret_tup for ret_tup in return_list]])


# #############################################################################
# Tests for get_random_product

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


# #############################################################################
# Tests for convert_str_to_int

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


# #############################################################################
# Tests for print_and_speak

# Inputs for test_print_and_speak_*
PRINT_AND_SPEAK_TEST_VALS = \
    [{'phrase': 'test phrase',
      'end': '\n',
      'replace_speech': ['', ''],
      'forecolor': None,
      'backcolor': None,
      'run_in_own_process': False,
      'speak': False,
      'return_val': 'test phrase',
      'stdout_val': 'test phrase\n'},
     {'phrase': 'test phrase',
      'end': '!',
      'replace_speech': ['phrase', 'test phrase'],
      'forecolor': None,
      'backcolor': back_c.GREEN,
      'run_in_own_process': False,
      'speak': False,
      'return_val': 'test test phrase',
      'stdout_val': back_c.GREEN + 'test phrase' + back_c.RESET + '!'},
     {'phrase': 'test phrase',
      'end': '\n',
      'replace_speech': ['', ''],
      'forecolor': fore_c.RED,
      'backcolor': back_c.LIGHTWHITE_EX,
      'run_in_own_process': False,
      'speak': False,
      'return_val': 'test phrase',
      'stdout_val': (back_c.LIGHTWHITE_EX + fore_c.RED + 'test phrase' +
                     fore_c.RESET + back_c.RESET + '\n')}
     ]
# PRINT_AND_SPEAK_TEST_VALS = \
#     [{'phrase': 'test phrase',
#       'end': '\n',
#       'replace_speech': ['', ''],
#       'forecolor': fore_c.RED,
#       'backcolor': back_c.LIGHTWHITE_EX,
#       'run_in_own_process': False,
#       'speak': False,
#       'return_val': 'test phrase',
#       'stdout_val': (back_c.LIGHTWHITE_EX + fore_c.RED + 'test phrase' +
#                      fore_c.RESET + back_c.RESET + '\n')}
#      ]

# Name of the parameters with default argument of the print_and_speak function.
P_AND_S_PARAMS_KEYS = \
    [val for val in list(signature(print_and_speak).parameters.keys())
     if val != 'phrase']


def get_test_print_and_speak_data(test_input):
    """Extract print_and_speak function inputs from test_input dictionary."""
    return (test_input['phrase'], test_input['return_val'],
            test_input['stdout_val'],
            {key: test_input[key] for key in P_AND_S_PARAMS_KEYS})


@pytest.mark.parametrize(
    "test_input", PRINT_AND_SPEAK_TEST_VALS
)
def test_print_and_speak_phrase_spoken(test_input):
    """Test return value for print_and_speak function."""
    phrase, return_val, _, input_dict = \
        get_test_print_and_speak_data(test_input)
    if pyttsx3 is not None:
        # Case when pyttsx3 can be imported
        assert return_val == print_and_speak(phrase, **input_dict)  # nosec
    else:
        # Case when pyttsx3 cannot be imported
        assert None is print_and_speak(phrase, **input_dict)  # nosec


@pytest.mark.parametrize(
    "test_input", PRINT_AND_SPEAK_TEST_VALS
)
def test_print_and_speak_phrase_printed(test_input, capsys):
    """Test phrase printed to stdout."""
    phrase, _, stdout_val, input_dict = \
        get_test_print_and_speak_data(test_input)
    # captured = capsys.readouterr()
    _ == print_and_speak(phrase, **input_dict)
    captured = capsys.readouterr()
    assert captured.out == stdout_val  # nosec
