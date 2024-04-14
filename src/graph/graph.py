import pydot

def dict_to_graphlist(dictionary):

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

def list_to_dotfile(list):
    with open("file.dot", "w") as output:
        for row in list:
            output.write(str(row) + '\n')

def graph_png(path, outputfile):
    (graph,) = pydot.graph_from_dot_file(path)
    outputfile_name = outputfile + '.png'
    graph.write_png(outputfile_name)