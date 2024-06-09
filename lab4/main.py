from __future__ import annotations
from RPN import convert_to_RPN

import json
import traceback

from model.grammar import CFG
from parse import parse_prog, ParseError
import pydot

"""

    PROG -> CALC_EXPR
    CALC_EXPR -> START_EXPR | START_EXPR OP_CMP START_EXPR
    
    # START_EXPR -> TERM | SIGN TERM | START_EXPR OP_SUM TERM
    
    START_EXPR -> TERM START_EXPR` | SIGN TERM START_EXPR` | TERM | SIGN TERM
    START_EXPR` -> OP_SUM TERM START_EXPR` | OP_SUM TERM 
    
    # TERM -> FACTOR | TERM OP_MUL FACTOR
    
    TERM -> FACTOR TERM` | FACTOR
    TERM` -> OP_MUL FACTOR TERM` | OP_MUL FACTOR
    
    FACTOR -> 'I' | 'C' | '(' START_EXPR ')' | 'not' FACTOR
    OP_CMP -> '=' | '<>' | '<' | '<=' | '>' | '>' '='
    SIGN -> '+' | '-'
    OP_SUM -> '+' | '-' | 'or'
    OP_MUL -> '*' | '/' | 'div' | 'mod' | 'and'
    OP_ASSIGN -> ':='
    
"""


def main():
    G1str = """
    PROG -> CALC_EXPR
    CALC_EXPR -> START_EXPR | START_EXPR OP_CMP START_EXPR
        
    START_EXPR -> TERM START_EXPR` | SIGN TERM START_EXPR` | TERM | SIGN TERM
    START_EXPR` -> OP_SUM TERM START_EXPR` | OP_SUM TERM 
        
    TERM -> FACTOR TERM` | FACTOR
    TERM` -> OP_MUL FACTOR TERM` | OP_MUL FACTOR
    
    FACTOR -> 'I' | 'C' | '(' START_EXPR ')' | 'not' FACTOR
    OP_CMP -> '=' | '<>' | '<' | '<=' | '>' | '>='
    SIGN -> '+' | '-'
    OP_SUM -> '+' | '-' | 'or'
    OP_MUL -> '*' | '/' | 'div' | 'mod' | 'and'
    OP_ASSIGN -> ':='
    """

    G2_string = """
                PROG -> CALC_EXPR
                CALC_EXPR -> START_EXP | START_EXP OP_CMP START_EXP
                
                START_EXPR -> TERM | TERM START_EXPR'
                START_EXPR' -> OP_SUM TERM | OP_SUM TERM START_EXPR'
                
                TERM -> FACTOR TERM' | FACTOR
                TERM' -> OP_MUL FACTOR TERM' | OP_MUL FACTOR
                
                FACTOR -> 'I' | 'C' | '(' START_EXPR ')'
                OP_CMP -> '=' | '<>' | '<' | '<=' | '>' | '>' '='
                SIGN -> '+' | '-'
                OP_SUM -> '+' | '-' | 'or'
                OP_MUL -> '*' | '/' | 'div' | 'mod' | 'and'
                OP_ASSIGN -> ':='
                
                """

    G1 = CFG.fromstring(G1str)
    G2 = CFG.fromstring(G2_string)
    print(G2)


    while True:
        txt = input('(?)> ')
        # txt = 'C+C'
        # txt = '(C+C*I)<I'
        # txt = '(C*C)'
        # txt = 'C+C*I*(C+C/I)'

        try:
            parsed = parse_prog(G2, txt)

            print(parsed.construct_str_expr())
            print(json.dumps(parsed.as_dict(), indent=2))

            # graph_dict = {'A': ['B', 'C'], 'B': ['A', 'D'], 'C': ['A'], 'D': ['B']}




            converted = convert_to_RPN(parsed)
            print(converted)
            print(json.dumps(converted.as_dict(), indent=2))
            print(converted.construct_str_expr())
        except ParseError as e:
            print(e)
            traceback.print_exc()
        # print(G1.get_first(Nonterminal(nterm)))
        # print(G1.get_follow(Nonterminal(nterm)))


if __name__ == '__main__':
    main()
