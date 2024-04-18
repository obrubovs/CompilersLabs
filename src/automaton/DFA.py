from RegexParser import RegexParser
from automaton.NFA import NFA
from typing import Dict
from constants.constants import Consts
import queue

class DFA:
    startState: str
    acceptingStates: [str]
    stateDict: Dict[int, Dict[str, int]] #таблица переходов с однозначным значением конечного состочния

    def __init__(self, nfa: NFA):
        self.stateDict = {}
        self.acceptingStates = []

        self.create(nfa)

    def create(self, nfa: NFA): # aka алгоритм Томпсона

        state_arr = []

        alphabet = nfa.makeAlphabet()
        alphabet.discard(Consts.epsSymbol)

        queueStates = queue.Queue()
        queueStates.put(nfa.startState)

        startState = nfa.startState

        eps_set = self.eps_clusure(startState, nfa)
        state_arr.append(eps_set)

        while not queueStates.empty():

            curStates = queueStates.get()

            # eps_set = self.eps_clusure(startState, nfa)

            for sign in alphabet:
                newStateSet = self.move(curStates, sign, nfa)
                if newStateSet:
                    newEpsClosure = self.eps_clusure(newStateSet, nfa)
                    if newEpsClosure not in state_arr:
                        queueStates.put(newStateSet)
                        state_arr.append(newEpsClosure)

                        self.stateDict[curStates][sign] = [newStateSet]




    def eps_clusure(self, state, nfa):
        eps_clusure_set = {state}
        # eps_clusure_set.update(state)
        eps_clusure_set.update(nfa.stateDict.get(state, {}).get(Consts.epsSymbol, []))

        return eps_clusure_set

    def move(self, state, sign, nfa):
        newState = set()
        newState.update(nfa.stateDict.get(state, {}).get(sign, []))

        return newState

string = 'aab*|c'
Tree = RegexParser().build_tree(string)
nfa = Tree.root.createNFA()

dfa = DFA(nfa)

dfa.create(nfa)
