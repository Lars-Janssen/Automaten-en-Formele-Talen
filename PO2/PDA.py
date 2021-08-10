# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  Framework for Automaten en Formele Talen           #
#  Written by Robin Visser, based on work by          #
#  Bas van den Heuvel and Daan de Graaf               #
#  This work is licensed under a Creative Commons     #
#  “Attribution-ShareAlike 4.0 International”         #
#   license.                                          #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #

import sys


class PDA:
    """
    Pushdown Automaton (PDA)
    """

    def __init__(self, Q, Sigma, Gamma, delta, s, F, pda_type="final_state",
                 verbose=False):
        """
        Creates the PDA object and performs input sanitization
        Q:       The finite set of states (list or set of strings)
        Sigma:   The input alphabet (list of set of strings)
        Gamma:   The stack alphabet (list of set of strings)
        delta:   The transition relation, a list of relation tuples containing
                 elements of the form: ((Q, Sigma, Gamma), (Q, [Gamma*])).
                 Where both 'Gamma' in the left-hand side and '[Gamma*]' in the
                 right-hand side may be (individually) replaced with 'ϵ'
        s:       The start state (string)
        F:       The finite set of final states (list or set of strings)
        pda_type:Specification of the type of PDA: "final_state" or
                 "empty_stack"
        verbose: Indicator of whether to print the new configuration after a
                 transition
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
        for lhs, rhs in delta:
            # Left-hand side
            state, input_symbol, top_stack = lhs
            if state not in Q:
                sys.exit("TransitionError: State \'" + state +
                         "\' not in Q")
            if input_symbol not in Sigma:
                sys.exit("TransitionError: Symbol \'" + input_symbol +
                         "\' for relation \'" + str((lhs, rhs)) +
                         "\' not in Sigma")
            if top_stack not in Gamma and top_stack != "ϵ":
                sys.exit("TransitionError: Stack-symbol \'" +
                         top_stack + "\' for relation \'" +
                         str((lhs, rhs)) + "\' not in Gamma")
            # Right-hand side
            state, top_stack_list = rhs
            if state not in Q:
                sys.exit("TransitionError: State \'" + state +
                         "\' not in Q")
            if top_stack_list != "ϵ":
                for stack_symbol in top_stack_list:
                    if stack_symbol not in Gamma:
                        sys.exit("TransitionError: Stack-symbol \'" +
                                 stack_symbol +
                                 "\' for relation \'" +
                                 str((lhs, rhs)) + "\' not in Gamma")

        # Create states
        self.states = {}
        self.final_states = []
        for state_name in Q:
            # Check if the state-to-be has any transitions/relations
            state_transitions = []
            for relation in delta:
                if relation[0][0] == state_name:
                    state_transitions.append(relation)

            new_state = State(state_name, state_transitions)
            self.states[state_name] = new_state
            if state_name in F:
                self.final_states.append(new_state)

        # Retain and assign variables
        self.pda_type = pda_type
        self.verbose = verbose
        self.input_alphabet = Sigma
        self.stack_alphabet = Gamma
        self.start_state = self.states[s]
        self.current_state = self.start_state

        # Setup stack
        self.stack = ['⊥']

    def transition(self, symbol):
        """
        Try to follow the input 'symbol' from the current state
        returns: True if succeeded, false otherwise
        """

        if self.stack:
            top_stack_symbol = self.stack.pop()
        else:
            top_stack_symbol = "ϵ"

        try:
            # Lookup new state and stack top
            new_state_name, new_top_stack = \
                self.current_state.transition_table[(symbol, top_stack_symbol)]

        except KeyError:
            if self.verbose:
                print("Warning: State \'" + self.current_state.name +
                      "\' has no transition for input-symbol \'" + symbol +
                      "\', and top stack-symbol: \'" +
                      top_stack_symbol + "\', no changes were made.")

            # Reappend the removed stack symbol
            if top_stack_symbol != "ϵ":
                self.stack.append(top_stack_symbol)

            return False

        # Keep track of previous state for printing transition info
        previous_state = self.current_state

        self.current_state = self.states[new_state_name]

        # Add new stack symbols to existing stack. Unfortunately Kozen notation
        # has the top of the stack on the left, while Python has it on the
        # right --> reverse append the symbols.
        if new_top_stack != "ϵ":
            for element in reversed(new_top_stack):
                self.stack.append(element)

        if self.verbose:
            used_relation = ((previous_state.name, symbol, top_stack_symbol),
                             (self.current_state.name, new_top_stack))
            print("Made transition using relation: " + str(used_relation))
            stack_visual = ' '.join(reversed(self.stack))
            print("State: \'" + self.current_state.name +
                  "\'| Stack: top -> " + stack_visual)

        return True

    def is_final(self):
        """
        Check whether the current state is a final state
        """
        return self.current_state in self.final_states

    def is_empty(self):
        """
        Check whether the PDA stack is empty
        """
        return not bool(self.stack)

    def transition_all(self, list_of_symbols):
        """
        Run PDA against the complete input 'list_of_symbols'
        returns: True if the input is accepted, False otherwise
        """

        for symbol in list_of_symbols:
            self.transition(symbol)

        if self.is_final() and self.pda_type == "final_state":
            return True

        if self.is_empty() and self.pda_type == "empty_stack":
            return True

        return False

    def reset(self):
        self.current_state = self.start_state
        self.stack = ['⊥']


class State:
    """State in a Pushdown Automaton (PDA)"""
    def __init__(self, name, relations):
        """
        name:       State name
        relations:  A list of relation tuples containing elements of the form:
                    ((Q, Sigma, Gamma), (Q, [Gamma*])). Where both 'Gamma' in
                    the left-hand side and '[Gamma*]' in the right-hand side
                    may be (individually) replaced with 'ϵ'
        """
        self.name = name

        transition_table = {}
        for lhs, rhs in relations:
            transition_table[lhs[1:]] = rhs
        self.transition_table = transition_table
