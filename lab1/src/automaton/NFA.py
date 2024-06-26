from typing import Dict, List
# from RegexParser import RegexParser
class NFA:
    startState: str
    acceptingStates: [str]
    stateDict: Dict[str, Dict[str, List[str]]] #таблица переходов

    def __init__(self):
        self.stateDict = {}
        self.acceptingStates = []

    def add(self, startState, finishState, transition):
        if startState not in self.stateDict.keys():
            self.stateDict[startState] = {}
            self.stateDict[startState][transition] = [finishState]
        elif transition not in self.stateDict[startState].keys():
            self.stateDict[startState][transition] = [finishState]
        else:
            self.stateDict[startState][transition].append(finishState)

    def makeAlphabet(self):
        Alphabet = set()
        for stsrt, dict in self.stateDict.items():
            for transmit, list in dict.items():
                if transmit not in Alphabet:
                    Alphabet.add(transmit)

        return Alphabet













