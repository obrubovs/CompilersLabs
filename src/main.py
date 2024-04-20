from RegexParser import RegexParser
from automaton.DFA import DFA
from graph.graph import graph_png

string = 'bca'
Tree = RegexParser().build_tree(string)
nfa = Tree.root.createNFA()


print(nfa.stateDict)


def dict2dot(dictionary):

    graph = []

    graph.append('graph A {')

    nodes = {}
    i = 0
    for start, dict in dictionary.items():
        if start not in nodes.keys():
            nodes.update({start:i})
            i += 1
        for transmit, node_list in dict.items():
            for node in node_list:
                if node not in nodes.keys():
                    nodes.update({node: i})
                    i += 1

                graph.append('  ' + str(nodes.get(start)) + ' -> ' + str(nodes.get(node)) + f' [label = {transmit}]')

    for k, v in nodes.items():
        graph.append(f'{v}')

    graph.append('}')

    return graph


graph_png(nfa.stateDict, 'graph')

dfa = DFA(nfa)
print(dfa)