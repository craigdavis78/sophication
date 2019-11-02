# -*- coding: utf-8 -*-
"""A program for Sophia to practice her multiplication tables."""
# Python Standard Library Imports
import argparse
from itertools import product
from multiprocessing import Process
from sys import exit as sys_exit
from random import sample
from typing import List, Tuple, Union, Any

# Third Party Library Imports
try:
    import win32com.client as wincl  # type: ignore
    speak = wincl.Dispatch("SAPI.SpVoice")  # type: ignore
except ImportError:
    speak = None


def get_random_products(max_val: int) -> \
        List[Tuple[Any, ...]]:
    """Create a list of randomly sampled Cartesian product with repeat of 2.

    Creates a list of randomly sampled cartesian products up to the value of
    max_val.

    Example
    Note that the results will not necessarily be in this order.

    >>> get_random_products(2)
    [(0, 0), (0, 1), (1, 0), (1, 1)]

    """
    nums = [i for i in range(max_val)]
    prods = [val for val in product(nums, repeat=2)]
    return sample(prods, len(prods))


def filter_tuple_list(include_list: List[int],
                      tuple_list: List[Tuple[Any, ...]]) -> \
        List[Tuple[Any, ...]]:
    """Filter tuples of integers by include_list.

    Filters tuple_list to include only the tuples that contain integers from
    include_list.
    """
    return_list = []
    for prod in tuple_list:
        for inc in include_list:
            if inc in prod:
                return_list.append(prod)
                break
    return return_list


def get_random_table(include_list: List[int],
                     max_val: int = 10) -> List[Tuple[Any, ...]]:
    """Create a list of randomly sorted tuples for multiplication.

    INPUTS:
    include_list: The integers of multiplication to practice.
    max_val: The maximum value to generate.

    OUTPUTS:
    Returns a list of randomly sorted integers based on include_list and
    max_val
    """
    # Get a list of randomly sampled tuples from 0 to max_val.
    random_products = get_random_products(max_val)
    # Filter random_products for those that contain integers from include_list.
    return_list = filter_tuple_list(include_list, random_products)
    return return_list


def speak_string(string_to_speak: str) -> None:
    """Speak a string (assuming win32com in installed)."""
    # Put this function in a try/except because it is called from a subprocess
    try:
        if speak:
            speak.speak(string_to_speak)
    except KeyboardInterrupt:
        pass


def print_and_speak(phrase: str, end: str = '\n',
                    replace_speech: List[str] = ['', ''],
                    fore_color=None, back_color=None,
                    speak_phrase: bool = False) -> str:
    """Print an optionally speak the phrase.

    Print the "phrase" with the end of line character "endl". Then speak
    the phrase Replace the characters replace_speech[0] with replace[1] before
    speaking the phrase
    """
    print(phrase, flush=True, end=end)
    phrase_spoken = phrase
    if speak_phrase:
        phrase_spoken = phrase.replace(replace_speech[0], replace_speech[1])
        p = Process(target=speak_string, args=(phrase_spoken, ))
        p.start()
    return phrase_spoken


def speak_all_done_info(num_correct: int,
                        num_attempts: int,
                        wrong_answers: Union[List[None],
                                             List[Tuple[int, int]],
                                             List[Tuple[Any, ...]]]) -> \
                        None:
    """Print and speak info when program completes."""
    print_and_speak('\nALL DONE!')
    print_and_speak(f'\nYou got {num_correct:2} out of {num_attempts:d}.')
    print_and_speak(f'Your score is {num_correct/num_attempts*100:.1f}% ',
                    replace_speech=['%', ' percent'])
    if wrong_answers:
        print_and_speak('You got these wrong:')
        wrong: Tuple[int, int]
        for wrong in set(wrong_answers):  # type: ignore
            print(f'{wrong[0]:d} x {wrong[1]:d} ' +
                  f'= {wrong[0]*wrong[1]:d}')


def convert_str_to_int(answer: str) -> Union[int, None]:
    """Convert a str to an int and print_and_speak on error.

    Convert a string to an integer.  Print and speak the error if 'answer'
    is not valid to be converted to an integer
    """
    try:
        return int(answer)
    except ValueError:
        print_and_speak(f'{answer} is not a valid input. Please ' +
                        'enter an integer')
        return None


def serve_cards(integers_to_practice: List[int],
                player_name: str = '') -> None:
    """Generate and serve the multiplication tables."""
    table = get_random_table(include_list=integers_to_practice)
    if player_name != '':
        print_and_speak(f"Hello {player_name:s}. Let's get started!")
    num_correct = 0  # The number correct on the first try
    correct_answers = []
    wrong_answers: Union[None, List[Tuple[Any, ...]]]
    wrong_answers = []
    for idx, val in enumerate(table):
        num_tries = 0
        try:
            while True:
                print_and_speak(f'{val[0]:d} x {val[1]:d} = ', end='',
                                replace_speech=[' x ', ' times '])
                num_attempts = idx + 1  # The number of cards attempted
                answer = convert_str_to_int(input())  # nosec
                correct_answer = val[0]*val[1]
                if answer == correct_answer:
                    print_and_speak('CORRECT!', replace_speech=['!', ''])

                    if num_tries == 0:
                        num_correct += 1
                        correct_answers.append(val)
                    break
                else:
                    print_and_speak('Wrong!  :(',
                                    replace_speech=['!  :(', ''])
                    wrong_answers.append(val)
                    num_tries += 1
        except KeyboardInterrupt:
            break
    speak_all_done_info(num_correct, num_attempts, wrong_answers)


if __name__ == '__main__':
    # Argparse for command line interface
    parser = argparse.ArgumentParser(description="Sophia's Multiplication " +
                                     "Flash Cards")
    parser.add_argument('integers', type=int, nargs='+')
    parser.add_argument('--name', type=str)
    args = parser.parse_args()
    serve_cards(args.integers, player_name=args.name)
    # Exit cleanly
    sys_exit(0)
