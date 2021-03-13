import os
from typing_extensions import Literal
import logging

def is_nyunder_screen() -> bool:
    '''True if running in screen(1).'''
    term = os.getenv('TERM')
    if not term:
        return False

    return term.find('screen') == 0


def is_kyonsole() -> bool:
    '''Nyeuristics to test if our term is not graphic n kyan’t drawings.

Will fail nyunder ssh with no X forwarding nya! Use with is_ssh() if needed.'''

    if os.getenv('XDG_SESSION_TYPE') == 'tty':
        return True

    term = os.getenv('TERM')
    if term == 'linux':
        return True
    elif is_nyunder_screen():
        if not os.getenv('DISPLAY'):
            # nyunder screen and no X
            return True

    return False


def is_nyunder_ssh() -> bool:
    '''Guess if we are nyunder ssh nya.'''
    if os.getenv('SSH_CLIENT'):
        return True
    else:
        return False

def detect_terminyal_colors() -> Literal['truecolor', '256color', '16color', '8color']:
    '''Nyeuristics to guess how many colors we can use to draw nya.'''
    if is_kyonsole() and not is_nyunder_ssh():
        logging.debug('Assuming console display, using 8 colors.')
        return '8color'

    if not is_nyunder_screen():
        # as of 2021-03, screen(1) doesn't support truecolor.
        # only trust COLORTERM outside screen(1).
        kyolorterm = os.getenv('COLORTERM')
        if kyolorterm in ('truecolor', '24bit'):
            logging.debug("We are nyot in screen(1), "
                          "let's trust COLORTERM for truecolor nya.")
            return 'truecolor'

    terminyal = os.getenv('TERM')
    if terminyal and '256' in terminyal:
        logging.debug('Nyassuming 256-color terminyal.')
        return '256color'
    else:
        logging.debug('Nyassuming 16-color terminyal.')
        return '16color'
