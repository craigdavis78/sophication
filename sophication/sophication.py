"""A program for Sophia to practice her multiplication tables."""
# Python Standard Library Imports
import argparse
from itertools import product
from multiprocessing import Process
from sys import exit as sys_exit
from random import sample
from typing import List, Tuple, Union, Any, NewType

# Third Party Library Imports
from colorama import Fore, Back, init as colorama_init  # type: ignore
try:
    import pyttsx3  # type: ignore
except ImportError:
    pyttsx3 = None

# Local Application/Library Imports
# NONE

# Must initialize colorama
colorama_init(convert=True)

# Define some module constants
CLR_FORE_CORRECT = Fore.GREEN
CLR_BACK_CORRECT = Back.WHITE
CLR_FORE_WRONG = Fore.RED
CLR_BACK_WRONG = Back.YELLOW
CLR_FORE_RESET = Fore.RESET
CLR_BACK_RESET = Back.RESET

# Define some custom types
ForeColorType = NewType('ForeColorType', str)
BackColorType = NewType('BackColorType', str)


def get_random_products(max_val: int) -> \
        List[Tuple[Any, ...]]:
    """Create a list of randomly sampled Cartesian product tuples.

    Creates a list of randomly sampled cartesian products tuples up to the
    value of max_val.

    :param max_val: The maximum integer up to which cartesian products will be
    generated
    :type max_val: int

    Example
    Note that the results will not necessarily be in this order.

    >>> get_random_products(2)
    [(0, 0), (0, 1), (1, 0), (1, 1)]

    """
    prods = set(product(range(max_val), repeat=2))
    return sample(prods, len(prods))


def filter_tuple_list(include_list: List[int],
                      tuple_list: List[Tuple[Any, ...]]) -> \
        List[Tuple[Any, ...]]:
    """Filter tuples of integers by include_list.

    Filters tuple_list to include only the tuples that contain integers from
    include_list.

    :param include_list: List of integers to filter by
    :type include_list: List[int]
    :param tuple_list: List of tuples of integers to filter
    :type tuple_list: List[Tuple[Any, ...]]
    :return: A filtered list of tuples that only contain integers from
        include_list
    :rtype: List[Tuple[Any, ...]]
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

    :param include_list: The integers of multiplication to practice.
    :type include_list: List[int]
    :max_val: The maximum value to generate.
    :type max_val: int
    :return: A list of randomly sorted integers based on include_list and
        max_val
    :rtype: List[Tuple[Any, ...]]
    """
    # Get a list of randomly sampled tuples from 0 to max_val.
    random_products = get_random_products(max_val)
    # Filter random_products for those that contain integers from include_list.
    return_list = filter_tuple_list(include_list, random_products)
    return return_list


def speak_string(string_to_speak: str) -> None:
    """Speak a string (assuming win32com in installed).

    :param string_to_speak: The string to speak, if available on the system.
    :type string_to_speak: str
    :return: None
    :rtype: None
    """
    # Put this function in a try/except because it is called from a subprocess
    try:
        engine = pyttsx3.init()
        engine.say(string_to_speak)
        engine.runAndWait()
        engine.stop()
    except KeyboardInterrupt:
        pass


def print_and_speak(phrase: str,
                    replace_speech: Tuple[str, str] = ('', ''),
                    colors: Tuple[Union[None, ForeColorType],
                                  Union[None, BackColorType]] = (None, None),
                    run_in_own_process: bool = True,
                    speak: bool = True) \
                    -> Union[None, str]:
    """Print an optionally speak the phrase.

    Print the "phrase" with the end of line character "endl". Then speak
    the phrase Replace the characters replace_speech[0] with replace[1] before
    speaking the phrase.

    :param phrase: The phrase to print and speak
    :type phrase: str
    :param replace_speech: A tuple used to replace a characters in phrase.
    :type replace_speech: Tuple[str, str]
    :param colors: The colors to to use for foreground and background text
        colors.  Passed like this, (forground_color, background_color).
    :type colors: Tuple[Union[None, ForeColorType], Union[None, BackColorType]]
    :param run_in_own_process: Boolean to indicate whether to run the speaking
        in it's own process. This can alleviate some lag in, however, words
        can get garbled together if not careful.
    :type run_in_own_process:
    :param speak: Boolean that indicates whether or not to speak. This is set
        to false if a text-only mode is desired.
    :type speak: bool
    :return: The phrase that was spoken, if it was spoken at all. The returned
        value will have had replace_speech applied.
    :rtype: Union[None, str]
    """
    # Print the Phrase
    phrase_printed = phrase
    forecolor = colors[0]
    backcolor = colors[1]
    if forecolor is not None:
        phrase_printed = forecolor + phrase_printed + CLR_FORE_RESET
    if backcolor is not None:
        phrase_printed = backcolor + phrase_printed + CLR_BACK_RESET
    print(phrase_printed, flush=True, end='')

    # Speak the phrase
    phrase_spoken: Union[None, str] = None
    if pyttsx3 is not None:
        phrase_spoken = phrase.replace(replace_speech[0], replace_speech[1])
        # The bool speak is an override for testing
        if speak:
            if run_in_own_process:
                process = Process(target=speak_string, args=(phrase_spoken, ))
                process.start()
            else:
                speak_string(phrase_spoken)
    return phrase_spoken


def speak_all_done_info(num_correct: int,
                        num_attempts: int,
                        wrong_answers: Union[List[None],
                                             List[Tuple[int, int]],
                                             List[Tuple[Any, ...]]]) \
                        -> None:
    """Print and speak info when program completes.

    :param num_correct: The number the person got correct.
    :type num_correct: int
    :param num_attempts: The number of times the person answered a question.
    :type num_attempts: int
    :param wrong_answers: A list of wrong answers.
    :type wrong_answers: Union[List[None],
                               List[Tuple[int, int],
                               List[Tuple[Any, ...]]]]
    :return: None
    :rtype: None
    """
    print_and_speak('\nALL DONE!\n', run_in_own_process=False)
    print_and_speak(f'\nYou got {num_correct:2} out of {num_attempts:d}.\n',
                    run_in_own_process=False)
    print_and_speak(f'Your score is {num_correct/num_attempts*100:.1f}% \n',
                    replace_speech=('%', ' percent'),
                    run_in_own_process=False)
    if wrong_answers:
        print_and_speak('You got these wrong:\n', run_in_own_process=False)
        wrong: Tuple[int, int]
        for wrong in set(wrong_answers):  # type: ignore
            print(f'{wrong[0]:d} x {wrong[1]:d} ' +
                  f'= {wrong[0]*wrong[1]:d}', flush=True)


def convert_str_to_int(str_to_convert: str) -> Union[int, None]:
    """Convert a str to an int and print_and_speak on error.

    Convert a string to an integer.  Print and speak the error if 'answer'
    is not valid to be converted to an integer.

    :param str_to_convert: The string to attempt to convert to an integer.
    :type str_to_convert: None
    :return: The converted string if successful, None if not successful.
    :rtype: Union[int, None]
    """
    try:
        return int(str_to_convert)
    except ValueError:
        print_and_speak(f'{str_to_convert} is not a valid input. Please ' +
                        'enter an integer\n')
        return None


def serve_cards(integers_to_practice: List[int],
                player_name: str = '') -> None:
    """Generate and serve the multiplication tables.

    :param integers_to_practice: The integers of multiplication to practice.
    :type integers_to_practice: List[int]
    :parm player_name: The name of the player
    :type player_name: str
    :return: None
    :rtype: None
    """
    table = get_random_table(include_list=integers_to_practice)
    if player_name != '':
        print_and_speak(f"Hello {player_name:s}. Let's get started!\n",
                        run_in_own_process=False)
    num_correct = 0  # The number correct on the first try
    correct_answers = []
    wrong_answers: Union[None, List[Tuple[Any, ...]]]
    wrong_answers = []
    for idx, val in enumerate(table):
        num_tries = 0
        try:
            answer_is_incorrect = True
            while answer_is_incorrect:
                print_and_speak(f'{val[0]:d} x {val[1]:d} = ',
                                replace_speech=(' x ', ' times '))
                num_attempts = idx + 1  # The number of cards attempted
                answer = convert_str_to_int(input())  # nosec
                correct_answer = val[0]*val[1]
                if answer == correct_answer:
                    print_and_speak('CORRECT!\n', replace_speech=('!', ''),
                                    colors=(ForeColorType(CLR_FORE_CORRECT),
                                            BackColorType(CLR_BACK_CORRECT)),
                                    run_in_own_process=False)
                    if num_tries == 0:
                        num_correct += 1
                        correct_answers.append(val)
                    answer_is_incorrect = False
                else:
                    print_and_speak('Wrong!  :(\n',
                                    replace_speech=('!  :(', ''),
                                    colors=(ForeColorType(CLR_FORE_WRONG),
                                            BackColorType(CLR_BACK_WRONG)),
                                    run_in_own_process=False)
                    wrong_answers.append(val)
                    num_tries += 1
        except KeyboardInterrupt:
            break
    speak_all_done_info(num_correct, num_attempts, wrong_answers)


def parse_and_serve():
    """Parse command line arguments and serve cards.

    :return: None
    :rtype: None
    """
    # Argparse for command line interface
    parser = argparse.ArgumentParser(description="Sophia's Multiplication " +
                                     "Flash Cards")
    parser.add_argument('integers', type=int, nargs='+')
    parser.add_argument('--name', type=str)
    args = parser.parse_args()
    serve_cards(args.integers, player_name=args.name)


if __name__ == '__main__':
    # Parse arguments and serve_the_cards
    parse_and_serve()
    # Exit cleanly
    sys_exit(0)
