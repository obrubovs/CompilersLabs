import uuid

from constants.constants import Consts
from automaton.NFA import NFA
class Node:
    value: str
    leftChild = None
    rightChild = None

    def __init__(self, value, leftNode=None, rightNode=None):
        self.value = value
        self.leftChild = leftNode
        self.rightChild = rightNode
    def createNFA(self):
        leftNFA = self.leftChild.createNFA() if self.leftChild is not None else self.leftChild
        rightNFA = self.rightChild.createNFA() if self.rightChild is not None else self.rightChild
        return self.joinNFA(leftNFA, rightNFA)

    def joinNFA(self, leftNFA, rightNFA):
        nfa = NFA()

        state1, state2 = str(uuid.uuid4()), str(uuid.uuid4())

        # заполнение таблицы переходов
        nfa.add(state1, state2, self.value)

        nfa.startState = state1
        nfa.acceptingStates.append(state2)

        return nfa


class OrNode(Node):
    def __init__(self, leftNode=None, rightNode=None):
        super().__init__(Consts.orSymbol, leftNode, rightNode)

    def joinNFA(self, leftNFA, rightNFA):
        nfa = NFA()

        # дополнение таблицы переходов
        nfa.stateDict.update(leftNFA.stateDict)
        nfa.stateDict.update(rightNFA.stateDict)

        # начальный и конечный переходы
        state1, state2 = str(uuid.uuid4()), str(uuid.uuid4())

        nfa.startState = state1
        nfa.acceptingStates.append(state2)

        # заполнение таблицы переходов
        nfa.add(state1, leftNFA.startState, Consts.epsSymbol)
        nfa.add(state1, rightNFA.startState, Consts.epsSymbol)

        for acceptState in leftNFA.acceptingStates:
            nfa.add(acceptState, state2, Consts.epsSymbol)

        for acceptState in rightNFA.acceptingStates:
            nfa.add(acceptState, state2, Consts.epsSymbol)

        return nfa

class AndNode(Node):
    def __init__(self, leftNode=None, rightNode=None):
        super().__init__(Consts.andSymbol, leftNode, rightNode)

    def joinNFA(self, leftNFA, rightNFA):
        nfa = NFA()

        # дополнение таблицы переходов
        nfa.stateDict.update(leftNFA.stateDict)
        nfa.stateDict.update(rightNFA.stateDict)

        nfa.startState = leftNFA.startState

        # заполнение таблицы переходов

        #eps переходы между односимвольными переходами
        for acceptState in leftNFA.acceptingStates:
            nfa.add(acceptState, rightNFA.startState, Consts.epsSymbol)

        for acceptState in rightNFA.acceptingStates:
            nfa.acceptingStates.append(acceptState)

        return nfa

class StarNode(Node):
    def __init__(self, leftNode=None, rightNode=None):
        super().__init__(Consts.starSymbol, leftNode, rightNode)


    def joinNFA(self, leftNFA, rightNFA):
        nfa = NFA()

        # дополнение таблицы переходов
        nfa.stateDict.update(leftNFA.stateDict)

        state1, state2 = str(uuid.uuid4()), str(uuid.uuid4())

        nfa.startState = state1
        nfa.acceptingStates.append(state2)

        # заполнение таблицы переходов
        nfa.add(state1, state2, Consts.epsSymbol)
        nfa.add(state1, leftNFA.startState, Consts.epsSymbol)

        for acceptState in leftNFA.acceptingStates:
            nfa.add(acceptState, state2, Consts.epsSymbol)

        for acceptState in leftNFA.acceptingStates:
            nfa.add(acceptState, leftNFA.startState, Consts.epsSymbol)

        return nfa