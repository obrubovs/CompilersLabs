from src.constants.constants import Consts
class Node:
    value: str
    leftChild = None
    rightChild = None

    def __init__(self, value, leftNode=None, rightNode=None):
        self.value = value
        self.leftChild = leftNode
        self.rightChild = rightNode


class OrNode(Node):
    def __init__(self, leftNode=None, rightNode=None):
        super().__init__(Consts.orSymbol, leftNode, rightNode)


class AndNode(Node):
    def __init__(self, leftNode=None, rightNode=None):
        super().__init__(Consts.andSymbol, leftNode, rightNode)


class StarNode(Node):
    def __init__(self, leftNode=None, rightNode=None):
        super().__init__(Consts.starSymbol, leftNode, rightNode)