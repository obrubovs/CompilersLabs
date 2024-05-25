import unittest

from grammar_parser import \
    immediate_recursion_eliminator, \
    direct_left_recursion_eliminator, \
    left_factorisation, \
    unreachable_symbols_elimination, \
    grammar_json_parser


class grammarTester(unittest.TestCase):
    def test_G0_grammar(self):
        init_grammar = grammar_json_parser('test.json')
        target_grammar = \
        {'nonterminals': ['E', 'F', 'T1', 'E1', 'T'],
         'terminals': {')', '*', '(', 'a', '+'},
         'rules': [{'lhs': 'E1', 'rhs': [['+', 'T', 'E1'], ['eps']]},
                   {'lhs': 'E', 'rhs': [['T', 'E1']]},
                   {'lhs': 'T1', 'rhs': [['*', 'F', 'T1'], ['eps']]},
                   {'lhs': 'T', 'rhs': [['T1']]},
                   {'lhs': 'F', 'rhs': [['a'], ['(', 'E', ')']]}],
         'start': 'E'}
        eliminated_lr = immediate_recursion_eliminator(init_grammar)

        self.assertEqual(target_grammar, eliminated_lr)

