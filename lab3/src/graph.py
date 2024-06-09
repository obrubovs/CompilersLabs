from graphviz import Digraph

def make_edge(parent_id, child_id):
    return str(f'   {parent_id} -> {child_id}')
def make_node(node_name, node_id):
    return str(f'    {node_id} [label="{node_name}"]')

def print_graph(dict, filename='graph.dot'):
    dot = Digraph(comment='A')



    dict_to_dot(dict, dot)


    dot.format = 'png'
    dot.render()
    # graph_filename = filename
    # (graph, ) = pydot.graph_from_dot_file(graph_filename)
    # outputfile_name = filename + '.png'
    # graph.write_png(outputfile_name)




# объявление списка в описании обхекта
def dict_to_dot(graph_dict:dict, dot:Digraph, iterator=None, parent_id=None):
    if parent_id:
        i = iterator
    else:
        i = 1
        parent_id = i

    for k, v in graph_dict.items():
        dot.node(str(parent_id), k)


        i += 1
        child_id = i

        dot.edge(str(parent_id), str(child_id))
        parent_id = child_id

        for e in v:
            if isinstance(e, dict):
                dict_to_dot(e, dot, i, parent_id)
            else:
                # i += 1
                # child_id = i
                # if e == '}' or e == '{':
                #     e = str('"') + e + str('"')
                dot.node(str(child_id), e)
                dot.edge(str(parent_id), str(child_id))
                i += 1