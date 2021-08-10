# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  Framework for Automaten en Formele Talen           #
#  Written by Robin Visser, based on work by          #
#  Bas van den Heuvel and Daan de Graaf               #
#  This work is licensed under a Creative Commons     #
#  “Attribution-ShareAlike 4.0 International”         #
#   license.                                          #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #

import sys


class FA:
    """
    Finite Automaton (FA)
    """

    def __init__(self, Q, Sigma, delta, s, F, verbose=False):
        """
        Creates the FA object and performs input sanitization
        Q:       The finite set of states (list or set of strings)
        Sigma:   The input alphabet (list of set of strings)
        delta:   The transition function (dictionary of dictionaries)
        s:       The start state (string)
        F:       The finite set of final states (list or set of strings)
        verbose: Indicator specifying whether a warning should be printed if
                 the FA attempts a non-existent transition
        """

        # Verify proper use of states
        if len(Q) != len(set(Q)):
            sys.exit("StateError: Q contains duplicates")

        if s not in Q:
            sys.exit("StateError: Starting state \'" + s + "\' not in Q")

        for state in F:
            if state not in Q:
                sys.exit("StateError: Final state \'" + state + "\' not in Q")

        # Verify proper use of transitions
        for state in delta:
            if state not in Q:
                sys.exit("TransitionError: State \'" + state + "\' not in Q")

            for symbol, next_state in delta[state].items():
                if symbol not in Sigma:
                    sys.exit("TransitionError: Symbol \'" + symbol +
                             "\' for state \'" + state + "\' not in Sigma")
                if next_state not in Q:
                    sys.exit("TransitionError: State \'" + next_state +
                             "\' for symbol \'" + symbol + "\' and state \'" +
                             state + "\' not in Q")

        # Create states
        self.states = {}
        self.final_states = []
        for state_name in Q:
            # Check if the state-to-be has a transition table
            if state_name in delta.keys():
                transition_table = delta[state_name]
            else:
                transition_table = {}

            new_state = State(state_name, transition_table)
            self.states[state_name] = new_state
            if state_name in F:
                self.final_states.append(new_state)

        # Retain and assign variables
        self.verbose = verbose
        self.input_alphabet = Sigma
        self.start_state = self.states[s]
        self.current_state = self.start_state

    def transition(self, symbol):
        """
        Try to follow the transition 'symbol' from the current state
        returns: True if succeeded, False otherwise
        """

        try:
            self.current_state = self.states[
                self.current_state.transition_table[symbol]]
            return True

        except KeyError:
            if self.verbose:
                print("Warning: State \'" + self.current_state.name +
                      "\' has no transition for symbol \'" + symbol +
                      "\', transition could not be performed")
            return False

    def is_final(self):
        """
        Check whether the current state is a final state
        """
        return self.current_state in self.final_states

    def reset(self):
        self.current_state = self.start_state


class State:
    """State in a Finite Automaton (FA)"""

    def __init__(self, name, transition_table):
        """
        name: State name
        transition_table: Dictionary of key-value pairs, where a key is the
                          transition symbol and a value the name of the state
                          the transition leads to
        """
        self.name = name
        self.transition_table = transition_table
