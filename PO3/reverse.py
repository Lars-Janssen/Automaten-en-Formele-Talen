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
    This program can extract the input and output of a Turing machine by
    reading the execution trace. It can, using this information, reverse
    engineer a Turing machine which produces the same output and execution
    trace, provided the same input.
"""

from TM import TM
import sys


def extract_input(trace, trace_tokenized):
    """
    Determines (and returns) the input string that the TM used when doing the
    computation which produced the given trace.
    returns: the input (as a string without spaces)
    """

    # Characters for left endmarker and BLANK: ⊢ , ⊔

    """
    This function extracts the Turin machine's input from an execution trace.
    It does this by keeping track of the position, and when we go further
    right than we have been, it adds what it reads to the inputlist,
    which it converts to a string at the end.
    """

    inputlist = []
    position = 0
    reading = False
    for i in range(len(trace_tokenized)):
        if(reading):
            if(position >= len(inputlist)):
                inputlist.append(trace[2*i])
            reading = False
        if(trace_tokenized[i] == "READ"):
            reading = True
        if(trace_tokenized[i] == "MLEFT"):
            position -= 1
        if(trace_tokenized[i] == "MRIGHT"):
            position += 1

    inputstring = ""
    for i in range(1, len(inputlist)):
        inputstring += inputlist[i]

    return inputstring


def extract_output(trace, trace_tokenized):
    """
    Determines (and returns) the tape output produced by the TM when doing the
    computation which produced the given trace. The ouput is the longest string
    _after_ the left endmarker that does not end in a BLANK ('⊔').
    returns: the output (as a string without spaces)
    """

    # Characters for left endmarker and BLANK: ⊢ , ⊔

    """
    This function extracts the Turing machine's output from an execution trace.
    It does so by starting with the input, then looping through the
    execution trace while writing over the input. The outputlist starts with
    a 0 in the front to accommodate for the ⊢.
    """
    inputstring = extract_input(trace, trace_tokenized)
    outputlist = [0]
    for i in range(len(inputstring)):
        outputlist.append(inputstring[i])

    position = 0
    writing = False
    for i in range(len(trace_tokenized)):
        if(writing):
            outputlist[position] = trace[2*i]
            writing = False
        if(trace_tokenized[i] == "WRITE"):
            writing = True
        if(trace_tokenized[i] == "MLEFT"):
            position -= 1
        if(trace_tokenized[i] == "MRIGHT"):
            position += 1
    outputstring = ""
    for i in range(1, len(outputlist)):
        outputstring += outputlist[i]
    return outputstring


def reverse_tm(traces, traces_tokenized):
    """
    Recreates (reverse engineers) a TM which behaves identically to the TM that
    produced the supplied list of traces. Note: 'behaves identically' implies
    that the recreated TM must produce (given the same input) the exact same
    execution traces as the original.
    traces: A list of traces produced by the original
    traces_tokenized: Tokenized versions of the original traces
    returns: A TM object capable of reproducing the traces given the same input
    """

    # Characters for left endmarker and BLANK: ⊢ , ⊔

    """
    I could not figure this function out.
    """
    Q = [0, 't', 'r']
    Sigma = ['0', '1']
    Gamma = ['0', '1', '⊔', '⊢']
    delta = [((0, '⊔'), ('t', '⊔', 'R'))]
    s = 0
    t = 't'
    r = 'r'

    my_tm = TM(Q, Sigma, Gamma, delta, s, t, r, verbose=True)

    return my_tm


def main(source_original, source_tokenized):
    """
    Reads both a set of original traces and their tokenized counterparts.
    """
    # Read the original traces (as strings with spaces)
    fo = open(source_original)
    with fo as f:
        traces = [trace for trace in [line.rstrip('\n') for line in f]]
    fo.close()

    # Read the tokenized traces (as lists of tokens, excluding 'SPACE')
    fo = open(source_tokenized)
    with fo as f:
        traces_tokenized = [trace.split() for trace in [line.rstrip('\n')
                            for line in f]]
    fo.close()

    # extract_input(traces[0], traces_tokenized[0])

    for i in range(len(traces)):
        print(extract_input(traces[i], traces_tokenized[i]))

    # extract_output(traces[1], traces_tokenized[1])

    for i in range(len(traces)):
        print(extract_output(traces[i], traces_tokenized[i]))

    # reverse_tm(traces, traces_tokenized)

    reverse_tm(traces, traces_tokenized)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit("RuntimeError: Use \'python3 reverse.py" +
                 " original_traces.txt tokenized_traces.txt\'")
    source_original = sys.argv[1]
    source_tokenized = sys.argv[2]
    main(source_original, source_tokenized)
