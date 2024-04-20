from RegexParser import RegexParser
from automaton.DFA import DFA
# from automaton.NFA import NFA
from graph.graph import graph_png


regex = input("Regex please: ")
# regex = 'abcc|(dc)*'
# regex = 'aab*|c'
# regex = '1(00|11)*'
# regex = '((0|1)(0|1)(0|1))*'
# regex = '((0*00)|1)*'

Tree = RegexParser().build_tree(regex)
nfa = Tree.root.createNFA()

dfa = DFA(nfa)
dfa_min = DFA(nfa)
dfa_min.minimize()

# input = 'aab'
# input = 'aa'
# input = 'c'
# input = 'aabbbbbb'
# string = 'aabbbIU7c'

string = input("String please: ")


dfa.check(string)




# task 4

dictState_4 = {0: {'0': 1, '1':2}, 1: {'0': 4, '1':5}, 2: {'0': 0, '1':0}, 3: {'0': 5, '1':4}, 4: {'0': 3, '1':5}, 5: {'0': 3, '1':4}}
startState_4 = 0
acceptingStates_4 = {4, 5}

dfa_4 = DFA(nfa)
dfa_4.startState = 0
dfa_4.acceptingStates = {4, 5}
dfa_4.stateDict = {0: {'0': 1, '1':2}, 1: {'0': 4, '1':5}, 2: {'0': 0, '1':0}, 3: {'0': 5, '1':4}, 4: {'0': 3, '1':5}, 5: {'0': 3, '1':4}}
# dfa_4.minimize()

graph_png(nfa, 'NFA')
graph_png(dfa, 'DFA')
graph_png(dfa_min, 'DFA_min')
# graph_png(dfa_4, 'DFA_4')
