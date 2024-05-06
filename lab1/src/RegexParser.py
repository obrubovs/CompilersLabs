from constants.constants import Consts
from nodes.node import Node, AndNode, OrNode, StarNode
from RegexTree import RegexTree


class RegexParser:
    i = 0

    def build_tree(self, regexStr: str):
        noded_list = self.parser(regexStr)
        tree = RegexTree()
        tree.root = noded_list
        return tree

    def parser(self, regexStr: str):

        regexStr = regexStr.replace(' ', '')
        nodelist = self.create_nodelist(regexStr)
        return self.create_tree_node(nodelist)
        # return self.build_tree(tree_node)

    def create_nodelist(self, regexStr: str):
        nodeList = []
        while self.i < len(regexStr) and regexStr[self.i] != Consts.closeSymbol:
            nodeList.append(self.create_node(regexStr))
            self.i += 1
        return nodeList

    def create_node(self, regexStr: str):

        elem = regexStr[self.i]

        if elem not in Consts.allSymbols:  # not (,),*,|,•
            return Node(elem)
        if elem in Consts.logicalOperators:  # *,|,•
            return elem
        if elem == Consts.openSymbol:
            self.i += 1
            return self.parser(regexStr)
        if elem == Consts.closeSymbol:
            return

    def create_tree_node(self, nodeLst: list):
        nodeLst = self.parseStar(nodeLst)
        nodeLst = self.parseAnd(nodeLst)
        nodeLst = self.parseOr(nodeLst)

        if len(nodeLst) != 1:
            raise Exception("Ошибка в процессе построения дерева: больше, чем 1 элемент в массиве")

        return nodeLst[0]

    def parseStar(self, nodeLst):
        updLst = []
        for i in range(len(nodeLst)):
            node = nodeLst[i]

            if node == Consts.starSymbol:
                if i == 0:
                    raise Exception("Ошибка: неверная постановка символа *")

                node = StarNode(updLst.pop())
            updLst.append(node)

        return updLst

    def parseAnd(self, nodeLst):
        # i = 0
        updLst = []
        isPreviousNode = False
        for i in range(len(nodeLst)):
            # while i < len(nodeLst):
            node = nodeLst[i]

            # if node == Consts.andSymbol:
            #     if i == 0 or i == len(nodeLst) - 1 or \
            #             nodeLst[i - 1] in [Consts.orSymbol, Consts.andSymbol, Consts.openSymbol] or \
            #             nodeLst[i + 1] in [Consts.orSymbol, Consts.andSymbol, Consts.closeSymbol, Consts.starSymbol]:
            #         raise Exception("Ошибка: неверная постановка символа •")
            #
            #     node = AndNode(updLst.pop(), nodeLst[i + 1])
            #     i += 1
            #     isPreviousNode = False
            if isinstance(node, Node):
                if isPreviousNode:
                    node = AndNode(updLst.pop(), node)
                isPreviousNode = True
            else:
                isPreviousNode = False
            updLst.append(node)

            # i += 1
        return updLst

    def parseOr(self, nodeLst: list):
        i = 0
        updLst = []

        while i < len(nodeLst):
            node = nodeLst[i]

            if node == Consts.orSymbol:
                if i == 0 or i == len(nodeLst) - 1 or \
                        nodeLst[i - 1] in [Consts.orSymbol, Consts.andSymbol, Consts.openSymbol] or \
                        nodeLst[i + 1] in [Consts.orSymbol, Consts.andSymbol, Consts.closeSymbol, Consts.starSymbol]:
                    raise Exception("Ошибка: неверная постановка символа |")
                node = OrNode(updLst.pop(), nodeLst[i + 1])
                i += 1
            updLst.append(node)
            i += 1

        return updLst


# string = 'aab*|c'
# Tree = RegexParser().build_tree(string)

# if Tree.root.leftNode is not None:
# def tree_output(tree_root):
#     tree = tree_root
#     print(type(tree))
#     if tree.rightChild is None:
#         if tree.leftChild is None:
#             print(tree.value)
#         else:
#             print(tree.leftChild.value)
#     else:
#         print(tree.rightvalue)

        # print(tree_root.value)

    #     if tree_root.rightChild is not None:
    #         tree_output(tree_root.rightChild)
    #
    #     # tree_output(tree_root.leftChild)
    # else:
    #     tree_output(tree_root.leftChild)

# tree_output(Tree.root)
# print(type(Tree))
# print(type(Tree.root.leftChild))
    # print(Tree.root.value)
    # print(Tree.root.leftChild.value)
    # print(Tree.root.value)
# print(Tree.root)
