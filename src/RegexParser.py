from constants.constants import Consts
from nodes.node import Node, AndNode, OrNode, StarNode
from RegexTree import RegexTree


class RegexParser:

    i = 0

    def parser(self, regexStr: str):

        regexStr = regexStr.replace(' ', '')
        nodeList = self.create_nodelist(regexStr)
        tree_node = self.build_tree_node(nodeList)
        return self.build_tree(tree_node)

    def create_nodelist(self, regexStr: str):
        nodeList = []
        while self.i < len(regexStr) and regexStr[self.i] != Consts.closeSymbol:
            nodeList.append(self.create_node(regexStr))
            self.i += 1
        return nodeList

    def build_tree(self, node: list):
        tree = RegexTree()
        tree.root = node
        return tree

    def create_node(self, regexStr: str):

        elem = regexStr[self.i]

        if elem not in Consts.controlSymbols:  # not (,),*,|,•
            return Node(elem)
        if elem in Consts.allOperators:  # *,|,•
            return elem
        if elem == Consts.openSymbol:
            self.i += 1
            return self.parser(regexStr)
        if elem == Consts.closeSymbol:
            return

    def build_tree_node(self, nodeLst: list):
        nodeLst = self._parseStar(nodeLst)
        nodeLst = self._parseAnd(nodeLst)
        nodeLst = self._parseOr(nodeLst)

        if len(nodeLst) != 1:
            raise Exception("Ошибка в процессе построения дерева: больше, чем 1 элемент в массиве")

        return nodeLst[0]

    def _parseStar(self, nodeLst):
        updLst = []
        for i in range(len(nodeLst)):
            node = nodeLst[i]

            if node == Consts.starSymbol:
                if i == 0:
                    raise Exception("Ошибка: неверная постановка символа *")

                node = StarNode(updLst.pop())
            updLst.append(node)

        return updLst

    def _parseAnd(self, nodeLst):
        i = 0
        updLst = []
        isPreviousNode = False

        while i < len(nodeLst):
            node = nodeLst[i]

            if node == Consts.andSymbol:
                if i == 0 or i == len(nodeLst) - 1 or \
                        nodeLst[i - 1] in [Consts.orSymbol, Consts.andSymbol, Consts.openSymbol] or \
                        nodeLst[i + 1] in [Consts.orSymbol, Consts.andSymbol, Consts.closeSymbol, Consts.starSymbol]:
                    raise Exception("Ошибка: неверная постановка символа •")

                node = AndNode(updLst.pop(), nodeLst[i + 1])
                i += 1
                isPreviousNode = False
            elif isinstance(node, Node):
                if isPreviousNode:
                    node = AndNode(updLst.pop(), node)
                isPreviousNode = True
            else:
                isPreviousNode = False
            updLst.append(node)

            i += 1
        return updLst

    def _parseOr(self, nodeLst: list):
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


string = input()
Tree = RegexParser().parser(string)

print(Tree)
print(Tree.root)


