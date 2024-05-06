from RegexParser import RegexParser
from automaton.NFA import NFA
from typing import Dict
from constants.constants import Consts
import queue

class DFA:
    startState: int
    acceptingStates: set
    stateDict: Dict[int, Dict[str, int]] #таблица переходов с однозначным значением конечного состочния
    Alphabet = set

    def __init__(self, nfa: NFA):
        self.stateDict = {}
        self.acceptingStates = set()
        self.Alphabet = set()

        self.create(nfa)
        # self.minimize()

    def create(self, nfa: NFA): # aka алгоритм Томпсона

        state_arr = []

        alphabet = nfa.makeAlphabet()
        alphabet.discard(Consts.epsSymbol)
        self.Alphabet = alphabet

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

    def minimize(self):
        marked = self.makeTable()
        n = len(marked)
        component = [-1 for _ in range(n)]

        componentCnt = 0
        for i in range(n):
            if component[i] == -1:
                component[i] = componentCnt
                for j in range(i + 1, n):
                    if not marked[i][j]:
                        component[j] = componentCnt
                componentCnt += 1

        newStateDict = {}
        for fromState, valueDict in self.stateDict.items():
            newFromState = component[fromState]
            for sign, toState in valueDict.items():
                newToState = component[toState]
                newStateDict.setdefault(newFromState, {})[sign] = newToState
        self.stateDict = newStateDict
        self.startState = component[self.startState]
        self.acceptingStates = {component[state] for state in self.acceptingStates}


    def makeTable(self):
        qState = queue.Queue()
        nState = len(self.getAllStates())
        marked = [[False for _ in range(nState)] for _ in range(nState)]

        for i in range(nState):
            isTerminal_i = i in self.acceptingStates # если состояние явлется конечным
            for j in range(nState):
                isTerminal_j = j in self.acceptingStates # если состояние явлется конечным
                if not marked[i][j] and isTerminal_i != isTerminal_j:
                    marked[i][j] = marked[j][i] = True
                    qState.put({i, j})

        while not qState.empty():
            statePair = list(qState.get())
            for sign in self.Alphabet:
                for edge0 in self.getReverseEdges(statePair[0], sign):
                    for edge1 in self.getReverseEdges(statePair[1], sign):
                        if not marked[edge0][edge1]:
                            marked[edge0][edge1] = marked[edge1][edge0] = True
                            qState.put({edge0, edge1})
        return marked



    def getAllStates(self):
        stateSet = set()
        for fromState, valueDict in self.stateDict.items():
            stateSet.add(fromState)
            for _, toState in valueDict.items():
                stateSet.add(toState)
        return stateSet

    def getReverseEdges(self, toState, sign):
        reverseEdgeList = []
        for state, valueDict in self.stateDict.items():
            if sign in valueDict.keys():
                if valueDict[sign] == toState:
                    reverseEdgeList.append(state)

        return reverseEdgeList
    def check(self, data: str):
        curState = self.startState
        for i in range(len(data)):

            toState = self.stateDict.get(curState, {}).get(data[i], None)
            print(str(i) + ' ' + data[i])
            if toState is None:
                print("Not match")
                return False
            curState = toState

        if curState not in self.acceptingStates:
            print("Not Match")
            return False
        print("Match")
        return True


