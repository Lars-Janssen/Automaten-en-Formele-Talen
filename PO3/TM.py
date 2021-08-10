# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  Framework for Automaten en Formele Talen           #
#  Written by Robin Visser, based on work by          #
#  Bas van den Heuvel and Daan de Graaf               #
#  This work is licensed under a Creative Commons     #
#  “Attribution-ShareAlike 4.0 International”         #
#   license.                                          #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #

import sys


class TM:
    """
    Turing machine (TM)
    """

    def __init__(self, Q, Sigma, Gamma, delta, s, t, r, verbose=False,
                 no_halt=1000):
        """
        Creates the TM object and performs input sanitization
        Q:       The finite set of states (list of strings)
        Sigma:   The input alphabet (list of strings)
        Gamma:   The tape alphabet (list of strings)
        delta:   The transition function, a list of tuples containing elements
                 of the form: ((Q, Gamma), (Q, Gamma, D)). Where 'D' must equal
                 either 'R' of 'L' signalling movement to the right or left
                 respectively.
        s:       The start state (string)
        t:       The accept state (string)
        r:       The reject state (string)
        verbose: Indicator of whether to print updates after a transition.
        no_halt: The amount of steps the TM is allowed to make before it is
                 assumed that it will not halt
        """

        # Verify that Gamma contains the left endmarker and blank symbol
        if '⊔' not in Gamma:
            sys.exit("TM-Error: Blank symbol \'⊔\' should be an element of" +
                     " Gamma, but it is not")
        if '⊢' not in Gamma:
            sys.exit("TM-Error: Left endmarker symbol \'⊢\' should be an" +
                     " element of Gamma, but it is not")

        # Verify proper use of states
        if len(Q) != len(set(Q)):
            sys.exit("StateError: Q contains duplicates")

        if s not in Q:
            sys.exit("StateError: Start state \'" + s + "\' not in Q")

        if t not in Q:
            sys.exit("StateError: Accept state \'" + t + "\' not in Q")

        if r not in Q:
            sys.exit("StateError: Reject state \'" + r + "\' not in Q")

        # Verify proper use of transitions
        for lhs, rhs in delta:

            # Left-hand side
            state, tape_symbol = lhs
            if state not in Q:
                sys.exit("TransitionError: State \'" + state +
                         "\' not in Q")
            if tape_symbol not in Gamma:
                sys.exit("TransitionError: Symbol \'" + tape_symbol +
                         "\' for transition \'" + str((lhs, rhs)) +
                         "\' not in Gamma")

            # Right-hand side
            state, tape_symbol, movement = rhs
            if state not in Q:
                sys.exit("TransitionError: State \'" + state +
                         "\' not in Q")
            if tape_symbol not in Gamma:
                sys.exit("TransitionError: Symbol \'" + tape_symbol +
                         "\' for transition \'" + str((lhs, rhs)) +
                         "\' not in Gamma")
            if movement not in ['R', 'L']:
                sys.exit("TransitionError: Movement \'" + movement +
                         "\' for relation \'" + str((lhs, rhs)) +
                         "\' does not equal either \'R\' or \'L\'")

        # Verify that the tape alphabet contains the input alphabet as a subset
        if not set(Sigma).issubset(Gamma):
            sys.exit("TM-Error: Gamma does not contain all elements of Sigma")

        # Create states
        self.states = {}
        for new_state_name in Q:
            # Check if the state-to-be has any transitions
            new_state_transitions = []
            for transition in delta:
                if transition[0][0] == new_state_name:
                    new_state_transitions.append(transition)
            new_state = State(new_state_name, new_state_transitions)
            self.states[new_state_name] = new_state

        # Retain and assign variables
        self.input_alphabet = Sigma
        self.tape_alphabet = Gamma
        self.verbose = verbose
        self.max_steps = no_halt
        self.start_state = self.states[s]
        self.accept_state = self.states[t]
        self.reject_state = self.states[r]

        # Setup the tape and the rest of the TM
        self.tape = Tape("")  # init with empty tape
        self.current_state = self.start_state
        self.step_counter = 0
        self.input_string = None

        if verbose:
            print("TM initialization complete, waiting for input...")

    def reset(self):
        """
        Reset the TM
        """
        self.tape = Tape(self.input_string)
        self.current_state = self.start_state
        self.step_counter = 0

    def set_input(self, input_string):
        """
        Reset the TM and write a new input on the tape
        """

        # Verify validity of the input string
        for element in input_string:
            if element not in self.input_alphabet:
                sys.exit("InputError: Input symbol \'" + element +
                         "\' not in input alphabet")

        self.input_string = input_string
        self.reset()

        if self.verbose:
            print("Input specified: " + self.input_string)
            print("New tape:")
            print(self.tape)

    def transition(self):
        """
        Try to take a single step in the TM.
        returns: True if the transition was successful, False otherwise.
        """

        # Check if the TM has an input string
        if not self.input_string:
            sys.exit("InputError: The TM has no input, specify using the" +
                     " set_input(input_string) function")

        # Check whether the TM has already entered the accept or reject state
        if self.current_state == self.accept_state:
            if self.verbose:
                print("Warning: the TM has already entered the accept state," +
                      " no transition was made")
            return False

        if self.current_state == self.reject_state:
            if self.verbose:
                print("Warning: the TM has already entered the reject state," +
                      " no transition was made")
            return False

        # Check whether we should assume that the TM is not going to halt
        if self.step_counter > self.max_steps:
            sys.exit("LogicError: The TM has taken more than " +
                     str(self.max_steps) + " steps without entering the" +
                     " accept or reject state, it is unlikely to halt!")

        # Read current element from the tape and try to transition.
        current_tape_element = self.tape.read()

        try:
            # Lookup new state, new tape element, and direction of movement
            new_state_name, new_tape_element, movement = \
                self.current_state.transition_table[current_tape_element]

        except KeyError:
            sys.exit("TM-Error: State \'" + self.current_state.name +
                     "\' has no transition for current tape symbol \'" +
                     current_tape_element + "\', the TM has stalled")

        # Write new tape element
        self.tape.write(new_tape_element)

        # Move position of the head
        self.tape.move(movement)

        # Keep track of previous state for printing transition info.
        previous_state = self.current_state

        # Change state in accordance with the transition
        self.current_state = self.states[new_state_name]

        if self.verbose:
            used_transition = ((previous_state.name, current_tape_element),
                               (new_state_name, new_tape_element, movement))
            print("Made transition using: " + str(used_transition))
            print("New tape:")
            print(self.tape)

        self.step_counter += 1

        return True

    def has_halted(self):
        """
        Check whether the TM has halted.
        """
        return self.current_state == self.accept_state or self.current_state \
                                  == self.reject_state

    def transition_all(self):
        """
        Take TM steps until the input is accepted or rejected.
        returns: True if the input is accepted, False if rejected.
        """

        while self.transition():
            pass

        if self.current_state == self.accept_state:
            return True

        if self.current_state == self.reject_state:
            return False

        sys.exit("TM-Error: Input was neither accepted or rejected")

    def get_tape_contents(self):
        """
        Retrieve a list representing the current finite part of the tape
        touched by the TM
        """
        return self.tape.tape_actual

    def get_execution_trace(self):
        """
        Retrieve a string representing the execution trace of the steps that
        the TM has taken so far
        """
        # Omit the final space
        return self.tape.execution_trace[:-1]


class State:
    """State in a Turing machine (TM)"""
    def __init__(self, name, transitions):
        """
        name:        State name
        transitions: a list of tuples containing elements of the form:
                     ((Q, Gamma), (Q, Gamma, D)). Where 'D' must equal either
                     'R' of 'L' signalling movement to the right or left
                     respectively.
        """
        self.name = name

        transition_table = {}
        for lhs, rhs in transitions:
            transition_table[lhs[-1]] = rhs

        self.transition_table = transition_table


class Tape:
    """
    Tape (and head) of a Turing machine (TM)
    The tape also keeps track of the produced execution trace.
    """
    def __init__(self, tm_input):

        # The (initial) relevant 'finite' part of the tape
        self.tape_actual = ['⊢']

        # Append the input to the tape
        self.tape_actual += tm_input

        # The current index of the TM head
        self.index = 0

        self.execution_trace = ""

    def __str__(self):
        # Assume a monospace terminal font.
        tape_result = ""
        head_result = ""

        for index in range(0, len(self.tape_actual)):
            if index > 0:
                tape_result += ' '
                head_result += ' '

            # Check if the head should be pointing to the current element
            if index == self.index:
                head_result += '^'
            else:
                head_result += ' ' * len(self.tape_actual[index])

            tape_result += self.tape_actual[index]

        tape_result += " ⊔ ⊔ ⊔ ..."

        return tape_result + "\n" + head_result

    def read(self):
        """ Read tape contents at the current position of the head """

        self.execution_trace += "- " + self.tape_actual[self.index]
        return self.tape_actual[self.index]

    def write(self, symbol):
        """ Write symbol to the current position of the head """

        # Verify left endmarker safety
        if self.index == 0 and symbol != '⊢':
            sys.exit("TapeError: The TM has overwritten the left endmarker" +
                     " at the leftmost piece of tape")

        self.execution_trace += " + " + symbol
        self.tape_actual[self.index] = symbol

    def move(self, direction):
        """ Move position of the head either to the left or to the right """
        if direction == 'R':
            # Check if we are at the end of the current 'finite' part.
            if self.index == (len(self.tape_actual) - 1):
                # Extend the finite part of the tape
                self.tape_actual.append('⊔')
            self.index += 1
            self.execution_trace += " > "
        elif direction == 'L':
            # Check if we are at the beginning of the tape
            if self.index == 0:
                sys.exit("TapeError: The TM has moved off the tape")
            self.index -= 1
            self.execution_trace += " < "
        else:
            sys.exit("TapeError: Movement \'" + direction +
                     "\' does not equal either \'R\' or \'L\'")
