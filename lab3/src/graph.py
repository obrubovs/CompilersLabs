from __future__ import annotations
import graphviz
from graphviz import Digraph


def make_edge(parent_id, child_id):
    return str(f'   {parent_id} -> {child_id}')
def make_node(node_name, node_id):
    return str(f'    {node_id} [label="{node_name}"]')

def print_graph(dict, filename='graph.dot'):
    dot = Digraph(comment='A')

    DG = DotGraph(dict, dot)
    DG.dict_to_dot()
    DG.make_graph_file('png')


    # dot.format = 'png'
    # dot.render()
    # graph_filename = filename
    # (graph, ) = pydot.graph_from_dot_file(graph_filename)
    # outputfile_name = filename + '.png'
    # graph.write_png(outputfile_name)




# объявление списка в описании обхекта


class DotGraph:
    def __init__(self, dict: dict, dot: Digraph):
        self.iterator = 0
        self.dict = dict
        self.dot = dot

    def dict_to_dot(self, secondary_dict: dict = None, parent_id=None):
        if secondary_dict:
            working_dict = secondary_dict
        else:
            working_dict = self.dict

        if not parent_id:
            self.iterator = 1
            parent_id = self.iterator

        for k, v in working_dict.items():
            self.dot.node(str(parent_id), k)

            self.iterator += 1
            child_id = self.iterator

            self.dot.edge(str(parent_id), str(child_id))
            parent_id = child_id

            for e in v:

                if isinstance(e, dict):
                    self.dict_to_dot(e, parent_id)
                    self.iterator += 1
                else:
                    self.iterator += 1
                    child_id = self.iterator
                    self.dot.node(str(child_id), e)
                    self.dot.edge(str(parent_id), str(child_id))
                    # self.iterator += 1

    def make_graph_file(self, file_format:str):
        self.dot.format = 'png'
        self.dot.render()