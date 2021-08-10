# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  Framework for Automaten en Formele Talen           #
#  Written by Robin Visser, based on work by          #
#  Bas van den Heuvel and Daan de Graaf               #
#  This work is licensed under a Creative Commons     #
#  “Attribution-ShareAlike 4.0 International”         #
#   license.                                          #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #

"""
Lars Janssen 12882712
This program uses a DFA to tokenize parts of a Turing machine execution trace.
It takes an exectution trace and returns a list of tuples, which consist
of a character in the trace and its corresponding state in the DFA after
transitioning from the start position. Symbols will be grouped.
"""

from FA import FA
import string
import sys


def create_fa():
    """
    Creates the finite automaton (FA) for trace tokenization
    Characters for left endmarker and BLANK: ⊢ , ⊔
    """
    ### Finish the automaton here... ###
    Q = ['START', 'SPACE', 'MLEFT', 'MRIGHT', 'READ', 'WRITE', 'BLANK', 'LEM',
         'SYMBOL']
    Sigma = [' ', '<', '>', "-", "+", '⊔', '⊢', 'character', 'digit']
    delta = {'START': {' ': 'SPACE',
                       '<': 'MLEFT',
                       '>': 'MRIGHT',
                       '-': 'READ',
                       '+': 'WRITE',
                       '⊔': 'BLANK',
                       '⊢': 'LEM',
                       'character': 'SYMBOL',
                       'digit': 'SYMBOL'},
             'SYMBOL': {'character': 'SYMBOL',
                        'digit': 'SYMBOL'}
             }
    s = 'START'
    F = ['SPACE', 'MLEFT', 'MRIGHT', 'READ', 'WRITE', 'BLANK', 'LEM', 'SYMBOL']

    M = FA(Q, Sigma, delta, s, F, verbose=False)

    return M


def char_type(char):
    """
    Returns the type of a character found in the trace
    """
    if char in string.digits:
        return 'digit'
    elif char in string.ascii_letters:
        return 'character'
    else:
        return char


def transition(fa, token):
    """
    This checks if the transition exist and uses sys.exit() otherwise.
    """
    if(fa.transition(token) == False):
        sys.exit()


def lexer(fa, trace):
    """
    The lexer iterates through the trace, tokenizing and assigning states to it
    fa: The finite automaton
    trace: A single string
    returns: A list of tuples containing first the token then the state.
    If something goes wrong the function should call sys.exit
    """
    
    """
    This reads the trace by character. If the read character is a digit or
    an ascii_letter it is added to the characters and
    transitions the DFA. If not, then it checks if characters is not empty,
    empties it, adds a tuple for the characters and resets the DFA.
    It then makes the transition with the token and adds a tuple for this
    token. In the end, it checks if characters is empty and adds a tuple if
    needed and the tupels are returned.
    """
    tuples = []
    characters = ''
    for i in range(len(trace)):
        token = trace[i]
        tokentype = char_type(trace[i])
        if(tokentype == trace[i]):
            if(characters != ''):
                tuples.append((characters, fa.current_state.name))
                characters = ''
                fa.reset()
            transition(fa, token)

            tuples.append((token, fa.current_state.name))
            fa.reset()
        elif(tokentype == 'digit'):
            transition(fa, 'digit')
            characters += token
        else:
            transition(fa, 'character')
            characters += token

    if(characters != ''):
        tuples.append((characters, fa.current_state.name))

    return tuples


def main(path):
    """
    Reads multiple traces from the file at 'path' and feeds them one by one to
    the lexer.
    """
    M = create_fa()

    fo = open(path)
    with fo as f:
        traces = [line.rstrip('\n') for line in f]
    fo.close()

    for trace in traces:
        M.reset()
        print("Trace: \"" + trace + "\"")
        print(lexer(M, trace))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('RuntimeError: Use `python3 tmtrace.py tmtraces.txt`')
    source = sys.argv[1]
    main(source)
