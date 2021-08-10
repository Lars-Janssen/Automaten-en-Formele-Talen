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
    This program will use pushdown automata (PDA's) to find out
    if tokenized Turing Machine traces are valid.
    It will print the valid traces afterwards.
"""

from PDA import PDA
import sys


"""
    This function defines a PDA to find out if a trace follows the correct
    steps to be a valid TM trace. If so, it returns True,
    else it returns False.
"""


def verify_steps(trace):
    """
    Creates and uses a PDA to verify proper Turing machine (TM) position in a
    single execution trace
    trace: A list of events (tokens)
    returns: True if the trace behaviour is valid, False otherwise
    """

    """
    This PDA has 4 states for the different operations in a step. Only the
    READ state will be a final state, because this means the TM trace is a
    multiple of 5 long.
    PS. Instead of using the stack to see if the PDA has to go to MOVE,
    you could also add an extra state, but I found this nicer.
    """
    Q = ['READ', 'TAPE', 'WRITE', 'MOVE']
    Sigma = ['MLEFT', 'MRIGHT', 'READ', 'WRITE', 'BLANK', 'LEM', 'SYMBOL']
    Gamma = ['⊥', 'ϵ', '1']
    delta = [(('READ', 'READ', '⊥'), ('TAPE', ['ϵ'])),
             (('READ', 'READ', 'ϵ'), ('TAPE', ['ϵ'])),
             (('TAPE', 'SYMBOL', 'ϵ'), ('WRITE', ['ϵ'])),
             (('TAPE', 'LEM', 'ϵ'), ('WRITE', ['ϵ'])),
             (('TAPE', 'BLANK', 'ϵ'), ('WRITE', ['ϵ'])),
             (('WRITE', 'WRITE', 'ϵ'), ('TAPE', ['1'])),
             (('TAPE', 'SYMBOL', '1'), ('MOVE', ['ϵ'])),
             (('TAPE', 'LEM', '1'), ('MOVE', ['ϵ'])),
             (('TAPE', 'BLANK', '1'), ('MOVE', ['ϵ'])),
             (('MOVE', 'MLEFT', 'ϵ'), ('READ', ['ϵ'])),
             (('MOVE', 'MRIGHT', 'ϵ'), ('READ', ['ϵ']))]
    s = 'READ'
    F = ['READ']
    pda_type = 'final_state'

    my_pda = PDA(Q, Sigma, Gamma, delta, s, F, pda_type, verbose=False)

    # Note: you can use my_pda.transition(symbol) to test a single transition
    """
    In the discussions a TA said you could also use the lack of a transition
    to see if a trace was false, so I did so.
    """
    for i in range(len(trace)):
        if(not my_pda.transition(trace[i])):
            return False

    return my_pda.is_final()


"""
    This function defines a PDA to find out if a trace stays on the trace.
    It will return True if so, and False otherwise.
"""


def verify_position(trace):
    """
    Creates and uses a PDA to verify proper Turing machine (TM) position in a
    single execution trace
    trace: A list of events (tokens)
    returns: True if the trace behaviour is valid, False otherwise
    """

    """
    I use 2 states to see if the head is still on the tape.
    In the stack I keep track of the position, so if the head moves right
    I add a 1 and if the head moves left it removes a 1. So if the stack is
    empty or only ⊥ it is on the left end marker.
    """
    Q = ['ONTAPE', 'OFFTAPE']
    Sigma = ['MLEFT', 'MRIGHT', 'READ', 'WRITE', 'BLANK', 'LEM', 'SYMBOL']
    Gamma = ['⊥', 'ϵ', '1']
    delta = [(('ONTAPE', 'MLEFT', '⊥'), ('OFFTAPE', ['ϵ'])),
             (('OFFTAPE', 'MLEFT', 'ϵ'), ('OFFTAPE', ['ϵ'])),
             (('ONTAPE', 'MLEFT', '1'), ('ONTAPE', ['ϵ'])),
             (('ONTAPE', 'MRIGHT', '⊥'), ('ONTAPE', ['1'])),
             (('ONTAPE', 'MRIGHT', '1'), ('ONTAPE', ['1', '1'])),
             (('OFFTAPE', 'MRIGHT', 'ϵ'), ('OFFTAPE', ['ϵ']))
             ]
    s = 'ONTAPE'
    F = ['ONTAPE']
    pda_type = 'final_state'

    my_pda = PDA(Q, Sigma, Gamma, delta, s, F, pda_type, verbose=False)

    return my_pda.transition_all(trace)


"""
    This PDA checks if the trace does not overwrite the left end marker.
    If it doesn't overwrite it, it returns True, else it returns False.
"""


def verify_lem(trace):
    """
    Creates and uses a PDA to verify Turing machine (TM) left endmarker safety
    for a single execution trace
    trace: A list of events (tokens)
    returns: True if the trace behaviour is valid, False otherwise
    """

    """
    This PDA also uses the stack to see if the head is on the left end marker.
    If so, it will check if it writes an LEM. If not, then the trace is unsafe.
    """
    Q = ['SAFE', 'CHECK', 'UNSAFE']
    Sigma = ['MLEFT', 'MRIGHT', 'READ', 'WRITE', 'BLANK', 'LEM', 'SYMBOL']
    Gamma = ['⊥', 'ϵ', '1']
    delta = [(('SAFE', 'WRITE', '⊥'), ('CHECK', ['ϵ'])),
             (('SAFE', 'WRITE', '1'), ('SAFE', ['1'])),
             (('SAFE', 'WRITE', 'ϵ'), ('CHECK', ['ϵ'])),
             (('CHECK', 'LEM', 'ϵ'), ('SAFE', ['ϵ'])),
             (('CHECK', 'SYMBOL', 'ϵ'), ('UNSAFE', ['ϵ'])),
             (('CHECK', 'BLANK', 'ϵ'), ('UNSAFE', ['ϵ'])),
             (('SAFE', 'MRIGHT', 'ϵ'), ('SAFE', ['1', '1'])),
             (('SAFE', 'MRIGHT', '1'), ('SAFE', ['1', '1'])),
             (('SAFE', 'MLEFT', '1'), ('SAFE', ['ϵ'])),
             ]
    s = 'SAFE'
    F = ['SAFE']
    pda_type = 'final_state'

    my_pda = PDA(Q, Sigma, Gamma, delta, s, F, pda_type, verbose=False)

    return my_pda.transition_all(trace)


def main(path):
    """
    Reads multiple tokenized traces from the file at 'path' and feeds them to
    the various verification functions.
    """
    # Read and parse traces
    fo = open(path)
    with fo as f:
        traces = [trace.split() for trace in [line.rstrip('\n') for line in f]]
    fo.close()

    """
    This checks for every trace if the steps are correct and adds it to
    the list if they are.
    """
    steps_correct = []
    for i in range(len(traces)):
        if(verify_steps(traces[i])):
            steps_correct.append(traces[i])

    """
    This checks for every remaining trace if it stays on the tape
    and adds it to the list if it does.
    """
    position_correct = []
    for i in range(len(steps_correct)):
        if(verify_position(steps_correct[i])):
            position_correct.append(steps_correct[i])

    """
    This checks for every remaining trace if the lem is not overwritten
    and adds it to the list if it doesn't overwrite it.
    """
    lem_correct = []
    for i in range(len(position_correct)):
        if(verify_lem(position_correct[i])):
            lem_correct.append(position_correct[i])

    """
    This prints the valid traces.
    """
    for i in range(len(lem_correct)):
        print(lem_correct[i])

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('RuntimeError: Use `python3 verification.py \
                 tokenized_traces.txt`')
    source = sys.argv[1]
    main(source)
