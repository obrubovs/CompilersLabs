import unittest
import parse
from model.grammar import CFG
from model.nterm import Nonterminal
from parse import ParsedNode


class TestLL1Anasyzer(unittest.TestCase):
    G2str = """
        PROG -> BLOCK
        BLOCK -> '{' OPS '}'
        OPS -> EXPR TAIL
        TAIL -> ';' EXPR TAIL | ε
        EXPR -> 'C' OP_ASSIGN CALC_EXPR | CALC_EXPR
        CALC_EXPR -> START_EXPR | START_EXPR OP_CMP START_EXPR
    
        START_EXPR -> TERM START_EXPR` | TERM
        START_EXPR` -> OP_SUM TERM START_EXPR` | OP_SUM TERM 
    
        TERM -> FACTOR TERM` | FACTOR
        TERM` -> OP_MUL FACTOR TERM` | OP_MUL FACTOR
    
        FACTOR -> 'I' | 'C' | '(' START_EXPR ')' | FACTOR
        OP_CMP -> '=' | '<>' | '<' | '<=' | '>' | '>='
        SIGN -> '+' | '-'
        OP_SUM -> '+' | '-' | 'or'
        OP_MUL -> '*' | '/' | 'div' | 'mod' | 'and'
        OP_ASSIGN -> ':='
        """
    G2 = CFG.fromstring(G2str)

    def test_parser(self):

        G2 = CFG.fromstring(self.G2str)

        test_data = [
            (
                '{I+I}',
                ParsedNode(Nonterminal('PROG'), [
                    ParsedNode(Nonterminal('BLOCK'), [
                        '{',
                        ParsedNode(Nonterminal('OPS'), [
                            ParsedNode(Nonterminal('EXPR'), [
                                ParsedNode(Nonterminal('CALC_EXPR'), [
                                    ParsedNode(Nonterminal('START_EXPR'), [
                                        ParsedNode(Nonterminal('TERM'), [ParsedNode(Nonterminal('FACTOR'), ['I'])]),
                                        ParsedNode(Nonterminal('START_EXPR1'), [
                                            ParsedNode(Nonterminal('OP_SUM'), ['+']),
                                            ParsedNode(Nonterminal('TERM'), [ParsedNode(Nonterminal('FACTOR'), ['I'])]),
                                        ]),
                                    ])
                                ])
                            ]),
                            ParsedNode(Nonterminal('TAIL'), [])
                        ]),
                        '}'
                    ])
                ])

            ),
            (
                '{C := I}',
                ParsedNode(Nonterminal('PROG'), [
                    ParsedNode(Nonterminal('BLOCK'), [
                        '{',
                        ParsedNode(Nonterminal('OPS'), [
                            ParsedNode(Nonterminal('EXPR'), [
                                'C',
                                ParsedNode(Nonterminal('OP_ASSIGN'), [':=']),
                                ParsedNode(Nonterminal('CALC_EXPR'), [
                                    ParsedNode(Nonterminal('START_EXPR'), [
                                        ParsedNode(Nonterminal('TERM'), [
                                            ParsedNode(Nonterminal('FACTOR'), [
                                                'I'
                                            ]),
                                        ]),
                                    ]),
                                ]),
                            ]),
                            ParsedNode(Nonterminal('TAIL'), []),
                        ]),
                        '}'
                    ])
                ])
            ),
            (
                '{'
                '   C := I;'
                '   C := C + C - C <> I'
                '}',
                ParsedNode(Nonterminal('PROG'), [
                    ParsedNode(Nonterminal('BLOCK'), [
                        '{',
                        ParsedNode(Nonterminal('OPS'), [
                            ParsedNode(Nonterminal('EXPR'), [
                                'C',
                                ParsedNode(Nonterminal('OP_ASSIGN'), [':=']),
                                ParsedNode(Nonterminal('CALC_EXPR'), [
                                    ParsedNode(Nonterminal('START_EXPR'), [
                                        ParsedNode(Nonterminal('TERM'), [
                                            ParsedNode(Nonterminal('FACTOR'), [
                                                'I'
                                            ]),
                                        ]),
                                    ]),
                                ]),
                            ]),
                            ParsedNode(Nonterminal('TAIL'), [
                                ';',
                                ParsedNode(Nonterminal('EXPR'), [
                                    'C',
                                    ParsedNode(Nonterminal('OP_ASSIGN'), [':=']),
                                    ParsedNode(Nonterminal('CALC_EXPR'), [
                                        ParsedNode(Nonterminal('START_EXPR'), [
                                            ParsedNode(Nonterminal('TERM'), [ParsedNode(Nonterminal('FACTOR'), ['C'])]),
                                            ParsedNode(Nonterminal('START_EXPR1'), [
                                                ParsedNode(Nonterminal('OP_SUM'), ['+']),
                                                ParsedNode(Nonterminal('TERM'), [ParsedNode(Nonterminal('FACTOR'), ['C'])]),
                                                ParsedNode(Nonterminal('START_EXPR1'), [
                                                    ParsedNode(Nonterminal('OP_SUM'), ['-']),
                                                    ParsedNode(Nonterminal('TERM'),
                                                               [ParsedNode(Nonterminal('FACTOR'), ['C'])]),
                                                ])
                                            ])
                                        ]),
                                        ParsedNode(Nonterminal('OP_CMP'), ['<>']),
                                        ParsedNode(Nonterminal('START_EXPR'), [
                                            ParsedNode(Nonterminal('TERM'), [
                                                ParsedNode(Nonterminal('FACTOR'), ['I'])
                                            ])
                                        ]),
                                    ])
                                ]),
                                ParsedNode(Nonterminal('TAIL'), [])
                            ]),
                        ]),
                        '}'
                    ])
                ])
            ),
            (
                '{'
                '   C := I;'
                '   C := - C + C - C * I div C <> I'
                '}',
                ParsedNode(Nonterminal('PROG'), [
                    ParsedNode(Nonterminal('BLOCK'), [
                        '{',
                        ParsedNode(Nonterminal('OPS'), [
                            ParsedNode(Nonterminal('EXPR'), [
                                'C',
                                ParsedNode(Nonterminal('OP_ASSIGN'), [':=']),
                                ParsedNode(Nonterminal('CALC_EXPR'), [
                                    ParsedNode(Nonterminal('START_EXPR'), [
                                        ParsedNode(Nonterminal('TERM'), [
                                            ParsedNode(Nonterminal('FACTOR'), [
                                                'I'
                                            ]),
                                        ]),
                                    ]),
                                ]),
                            ]),
                            ParsedNode(Nonterminal('TAIL'), [
                                ';',
                                ParsedNode(Nonterminal('EXPR'), [
                                    'C',
                                    ParsedNode(Nonterminal('OP_ASSIGN'), [':=']),
                                    ParsedNode(Nonterminal('CALC_EXPR'), [
                                        ParsedNode(Nonterminal('START_EXPR'), [
                                            ParsedNode(Nonterminal('SIGN'), ['-']),
                                            ParsedNode(Nonterminal('TERM'), [ParsedNode(Nonterminal('FACTOR'), ['C'])]),
                                            ParsedNode(Nonterminal('START_EXPR1'), [
                                                ParsedNode(Nonterminal('OP_SUM'), ['+']),
                                                ParsedNode(Nonterminal('TERM'), [ParsedNode(Nonterminal('FACTOR'), ['C'])]),
                                                ParsedNode(Nonterminal('START_EXPR1'), [
                                                    ParsedNode(Nonterminal('OP_SUM'), ['-']),
                                                    ParsedNode(Nonterminal('TERM'),
                                                               [
                                                                   ParsedNode(Nonterminal('FACTOR'), ['C']),
                                                                   ParsedNode(Nonterminal('TERM1'), [
                                                                       ParsedNode(Nonterminal('OP_MUL'), ['*']),
                                                                       ParsedNode(Nonterminal('FACTOR'), ['I']),
                                                                       ParsedNode(Nonterminal('TERM1'), [
                                                                           ParsedNode(Nonterminal('OP_MUL'), ['div']),
                                                                           ParsedNode(Nonterminal('FACTOR'), ['C']),
                                                                       ]),
                                                                   ])
                                                               ]),
                                                ])
                                            ])
                                        ]),
                                        ParsedNode(Nonterminal('OP_CMP'), ['<>']),
                                        ParsedNode(Nonterminal('START_EXPR'), [
                                            ParsedNode(Nonterminal('TERM'), [
                                                ParsedNode(Nonterminal('FACTOR'), ['I'])
                                            ])
                                        ]),
                                    ])
                                ]),
                                ParsedNode(Nonterminal('TAIL'), [])
                            ]),
                        ]),
                        '}'
                    ])
                ])
            ),
        ]

        for test, target in test_data:
            assert parse.parse_prog(G2, test) == target
