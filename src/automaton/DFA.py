from RegexParser import RegexParser
from automaton.NFA import NFA
from typing import Dict
from constants.constants import Consts
import queue

class DFA:
    startState: int
    acceptingStates: set
    stateDict: Dict[int, Dict[str, int]] #таблица переходов с однозначным значением конечного состочния

    def __init__(self, nfa: NFA):
        self.stateDict = {}
        self.acceptingStates = set()

        self.create(nfa)

    def create(self, nfa: NFA): # aka алгоритм Томпсона

        state_arr = []

        alphabet = nfa.makeAlphabet()
        alphabet.discard(Consts.epsSymbol)

        queueStates = queue.Queue()

        startState = {nfa.startState}

        startEpsStates = self.eps_clusure_set(startState, nfa)

        state_arr.append(startEpsStates)

        queueStates.put(startEpsStates)
        self.startState = state_arr.index(startEpsStates)


        while not queueStates.empty():


            curStates = queueStates.get()

            for state in curStates:
                if state in nfa.acceptingStates:
                    self.acceptingStates.add(state_arr.index(curStates))
                    break
            # eps_set = self.eps_clusure(startState, nfa)

            for sign in alphabet:
                newStateSet = self.move(curStates, sign, nfa)

                newEpsClosure = self.eps_clusure_set(newStateSet, nfa)

                if not len(newEpsClosure):
                    continue
                if newEpsClosure not in state_arr:
                    queueStates.put(newEpsClosure)
                    state_arr.append(newEpsClosure)

                iStart = state_arr.index(curStates)
                iFinish = state_arr.index(newEpsClosure)
                self.stateDict.setdefault(iStart, {})[sign] = iFinish
                # self.stateDict[curStates][sign] = {newStateSet}

    def eps_clusure_set(self, stateSet, nfa):
        eps_clusure_set = set()

        for state in stateSet:
            eps_clusure_set.update(self.eps_clusure_state(state, nfa))

        return eps_clusure_set

    def eps_clusure_state(self, state, nfa):
        epsClosure = {state}
        toStateEpsList = nfa.stateDict.get(state, {}).get(Consts.epsSymbol, [])
        for state in toStateEpsList:
            epsClosure.update(self.eps_clusure_state(state, nfa))

        return epsClosure


    def move(self, stateSet, sign, nfa):
        newState = set()
        for state in stateSet:
            newState.update(nfa.stateDict.get(state, {}).get(sign, []))

        return newState


string = 'aab*|c'
Tree = RegexParser().build_tree(string)
nfa = Tree.root.createNFA()

dfa = DFA(nfa)

dfa.create(nfa)
