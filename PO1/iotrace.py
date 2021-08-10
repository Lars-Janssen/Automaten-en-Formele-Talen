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
This program uses a DFA to verify the proper use of syscalls
for a single file.
"""

from FA import FA


def create_fa():
    """
    Creates the finite automaton (FA) for trace verification
    """
    ### Finish the automaton here... ###
    Q = ['START', 'FD', 'ERROR']
    Sigma = ['open', 'read', 'write', 'close']
    delta = {'START': {'open': 'FD',
                       'read': 'ERROR',
                       'write': 'ERROR',
                       'close': 'ERROR'},
             'FD': {'open': 'ERROR',
                    'read': 'FD',
                    'write': 'FD',
                    'close': 'START'}}
    s = 'START'
    F = ['ERROR']

    M = FA(Q, Sigma, delta, s, F, verbose=False)

    return M


def verify_fileio(fa, trace):
    """
    Verify proper file handling using a finite automaton (FA)
    fa:    The finite automaton
    trace: List of strings ('syscalls')
    returns: True if the trace represents proper file handling (i.e. the trace
             is NOT accepted by the FA), False otherwise
    """

    """
    This reads the trace call by call and transitions the automaton each
    time. If the automaton is in a final position (ERROR), then it returns
    False because the use is not proper. If the automaton is not in a final
    position (namely not ERROR), then it return True because the use is proper.
    It also returns False if the trace if the input is incorrect.
    """
    fa.reset()
    for i in range(len(trace)):
        if(fa.transition(trace[i]) == False):
            return False
    if(fa.is_final() == False):
        return True
    else:
        return False


def main():
    """
    Create the FA and perform verification of a test trace
    """
    M = create_fa()
    ### Test your code here... ###
    trace = ["open", "read", "write", "write", "close", "open", "close"]
    print("Test trace: " + str(trace))
    print("Proper file handling: " + str(verify_fileio(M, trace)))


if __name__ == '__main__':
    main()
