import unittest

from RegexParser import RegexParser
from RegexTree import RegexTree


class RegexParser_Tester(unittest.TestCase):

    def tree_to_list(self, tree: RegexTree):

        curNode = tree.root
        stack = []
        path = ""
        res = []

        while True:
            if curNode is not None:
                stack.append((path, curNode))
                curNode = curNode.leftChild

                path += "L"
            elif len(stack):
                path, curNode = stack.pop()
                value = curNode.value

                res.append((path, value))
                curNode = curNode.rightChild

                path += "R"
            else:
                break
        return res


    def TreesAreEqual(self, tree1: RegexTree, tree2: list):
        return self.tree_to_list(tree1) == tree2


    def test_OneElement(self):
        regex = 'a'
        targetTree = [("", 'a')]
        parsedTree = RegexParser().build_tree(regex)
        self.assertEqual(True, self.TreesAreEqual(parsedTree, targetTree))

    def test_AND(self):
        regex = "ab"
        parsedTree = RegexParser().build_tree(regex)
        targetTree = [('L', "a"), ('', "•"), ('R', "b")]

        self.assertEqual(True, self.TreesAreEqual(parsedTree, targetTree))


    def test_OR(self):
        regex = "a|b"
        parsedTree = RegexParser().build_tree(regex)
        targetTree = [('L', "a"), ('', "|"), ('R', "b")]

        self.assertEqual(True, self.TreesAreEqual(parsedTree, targetTree))

    def test_STAR(self):
        regex = "a*"
        parsedTree = RegexParser().build_tree(regex)
        targetTree = [('L', "a"), ('', "*")]

        self.assertEqual(True, self.TreesAreEqual(parsedTree, targetTree))

    def test_AND_ThreeElements(self):
        regex = "abc"
        parsedTree = RegexParser().build_tree(regex)
        targetTree = [('LL', "a"), ('L', "•"), ('LR', "b"), ('', "•"), ('R', "c")]

        self.assertEqual(True, self.TreesAreEqual(parsedTree, targetTree))

    def test_OR_ThreeElements(self):
        regex = "a|b|c"
        parsedTree = RegexParser().build_tree(regex)
        targetTree = [('LL', "a"), ('L', "|"), ('LR', "b"), ('', "|"), ('R', "c")]

        self.assertEqual(True, self.TreesAreEqual(parsedTree, targetTree))


    def test_AND_OR(self):
        regex = "ab|c"
        parsedTree = RegexParser().build_tree(regex)
        targetTree = [('LL', "a"), ('L', "•"), ('LR', "b"), ('', "|"), ('R', "c")]

        self.assertEqual(True, self.TreesAreEqual(parsedTree, targetTree))


    def test_OR_AND(self):
        regex = "a|bc"
        parsedTree = RegexParser().build_tree(regex)
        targetTree = [('L', "a"), ('', "|"), ('RL', "b"), ('', "•"), ('RR', "c")]

        self.assertEqual(True, self.TreesAreEqual(parsedTree, targetTree))


    def test_parserAndOrAnd(self):
        regex = "ab|cd"
        parsedTree = RegexParser().build_tree(regex)
        targetTree = [("LL", "a"), ("L", "•"), ("LR", "b"),
                    ("", "|"), ("RL", "c"), ("R", "•"),
                    ("RR", "d")]

        self.assertEqual(True, self.TreesAreEqual(parsedTree, targetTree))
