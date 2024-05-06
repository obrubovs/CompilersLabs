import pydot
from collections.abc import Iterable

def dict_to_graphlist(automat):
    nfa_dict = automat.stateDict

    graph = []

    graph.append('digraph A {')
    graph.append('layout = "dot"')

    nodes = {}
    i = 0
    # graph.append(' -> 0 [label = start]')
    for start, dict in nfa_dict.items():
        if start not in nodes.keys():
            nodes.update({start:i})
            i += 1
        for transmit, node_list in dict.items():
            if isinstance(node_list, Iterable):
                for node in node_list:
                    if node not in nodes.keys():
                        nodes.update({node: i})
                        i += 1

                    graph.append('  ' + str(nodes.get(start)) + ' -> ' + str(nodes.get(node)) + f' [label = {transmit}]')

            else:
                node = node_list
                if node not in nodes.keys():
                    nodes.update({node: i})
                    i += 1

                graph.append('  ' + str(nodes.get(start)) + ' -> ' + str(nodes.get(node)) + f' [label = {transmit}]')



    for k, v in nodes.items():
        graph.append(f'{v}')
        if k in automat.acceptingStates:
            graph.append('[shape = doublecircle]')
        if k == automat.startState:
            graph.append('[style=filled, fillcolor=grey]')

    graph.append('}')

    return graph

def list_to_dotfile(list, filename):
    output_filename = filename + '.dot'
    with open(output_filename, "w") as output:
        for row in list:
            output.write(str(row) + '\n')

def graph_png(dict, filename):
    graphlist = dict_to_graphlist(dict)
    list_to_dotfile(graphlist, filename)
    dotfile_name = filename + ".dot"
    (graph,) = pydot.graph_from_dot_file(dotfile_name)
    outputfile_name = filename + '.png'
    graph.write_png(outputfile_name)