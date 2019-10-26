# -*- coding: utf-8 -*-
"""
A program for Sophia to practice her multiplication tables.
"""

from itertools import product
from random import sample
import argparse
from typing import List
from sys import exit as sys_exit

import win32com.client as wincl
speak = wincl.Dispatch("SAPI.SpVoice")


def get_random_table(include_list: List[int] = [i for i in range(10)]):
    nums = [i for i in range(10)]
    prods = [val for val in product(nums, repeat=2)]
    random_prods = sample(prods, len(prods))
    return_list = []
    for prod in random_prods:
        for inc in include_list:
            if inc in prod:
                return_list.append(prod)
                break
    return return_list


def print_and_speak(phrase: str, end: str = '\n',
                    replace_speech: List[str] = ['', ''],
                    fore_color=None, back_color=None,
                    speak_phrase=False) -> None:
    '''Print the "phrase" with the end of line character "endl". Then speak
    the phrase Replace the characters replace_speech[0] with replace[1] before
    speaking the phrase'''
    print(phrase, flush=True, end=end)
    if speak_phrase:
        speak_phrase = phrase.replace(replace_speech[0], replace_speech[1])
        speak.Speak(speak_phrase)
    return speak_phrase


def speak_all_done_info(num_correct, num_attempts, wrong_answers):
    print_and_speak('\nALL DONE!')
    print_and_speak(f'\nYou got {num_correct:2} out of {num_attempts:d}.')
    print_and_speak(f'Your score is {num_correct/num_attempts*100:.1f}% ',
                    replace_speech=['%', ' percent'])
    print_and_speak('You got these wrong:')
    for wrong in set(wrong_answers):
        print(f'{wrong[0]:d} x {wrong[1]:d} = {wrong[0]*wrong[1]:d}')


def convert_str_to_int(answer: str):
    try:
        answer = int(answer)
    except ValueError:
        print_and_speak(f'{answer} is not a valid input. Please ' +
                        'enter an integer')
    return answer


def serve_cards(parser_args):
    table = get_random_table(include_list=parser_args.integers)
    if args.name != '':
        speak.Speak(f"Hello {args.name:s}. Let's get started!")
    num_correct = 0  # The number correct on the first try
    correct_answers = []
    wrong_answers = []
    for idx, val in enumerate(table):
        num_tries = 0
        try:
            while True:
                print_and_speak(f'{val[0]:d} x {val[1]:d} = ', end='',
                                replace_speech=[' x ', ' times '])
                answer = convert_str_to_int(input())
                num_attempts = idx + 1  # The number of cards attempted
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

    parser = argparse.ArgumentParser(description="Sophia's Multiplication " +
                                     "Flash Cards")
    parser.add_argument('integers', type=int, nargs='+')
    parser.add_argument('--name', type=str)
    args = parser.parse_args()
    serve_cards(args)
    sys_exit(0)
