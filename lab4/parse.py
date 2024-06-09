from __future__ import annotations

from dataclasses import dataclass

from model.grammar import CFG
from model.nterm import Nonterminal


def _eq_lists(a: list[ParsedNode | str], b: list[ParsedNode | str]) -> bool:
    if len(a) != len(b):
        return False
    for ai in a:
        if ai not in b:
            return False
    return True


@dataclass
class ParsedNode:
    nterm: Nonterminal
    targets: list[ParsedNode | str]

    @property
    def parsed_len(self) -> int:
        ret = 0
        for t in self.targets:
            if isinstance(t, str):
                ret += len(t)
            else:
                ret += t.parsed_len
        return ret

    def __eq__(self, __value):
        return (isinstance(__value, ParsedNode)
                and self.nterm == __value.nterm
                and _eq_lists(self.targets, __value.targets))

    def construct_str_expr(self) -> str:
        ret = ''
        for t in self.targets:
            if isinstance(t, ParsedNode):
                ret += t.construct_str_expr()
            else:
                ret += ' ' + t + ' '
        # if len(self.targets) >= 3 and ret.strip()[0] != '(':
        #     ret = f'({ret})'
        return ret

    def as_dict(self) -> dict:
        targets = []
        for t in self.targets:
            if isinstance(t, str):
                targets.append(t)
            else:
                targets.append(t.as_dict())
        return {self.nterm.symbol: targets}


@dataclass
class ParseError(Exception):
    nterm: Nonterminal
    variants: list[str]


def parse_assign(grammar: CFG, in_str: str) -> ParsedNode:
    nterm = Nonterminal('OP_ASSIGN')
    first = grammar.get_first(nterm)

    for f in first:
        if in_str.startswith(f):
            return ParsedNode(nterm, [f])

    raise ParseError(nterm, first)


def parse_mul(grammar: CFG, in_str: str) -> ParsedNode:
    nterm = Nonterminal('OP_MUL')
    first = grammar.get_first(nterm)

    for f in first:
        if in_str.startswith(f):
            return ParsedNode(nterm, [f])

    raise ParseError(nterm, first)


def parse_sum(grammar: CFG, in_str: str) -> ParsedNode:
    nterm = Nonterminal('OP_SUM')
    first = grammar.get_first(nterm)

    for f in first:
        if in_str.startswith(f):
            return ParsedNode(nterm, [f])

    raise ParseError(nterm, first)


def parse_sign(grammar: CFG, in_str: str) -> ParsedNode:
    nterm = Nonterminal('SIGN')
    first = grammar.get_first(nterm)

    for f in first:
        if in_str.startswith(f):
            return ParsedNode(nterm, [f])

    raise ParseError(nterm, first)


def parse_cmp(grammar: CFG, in_str: str) -> ParsedNode:
    nterm = Nonterminal('OP_CMP')
    first = grammar.get_first(nterm)

    for f in first:
        if in_str.startswith(f):
            return ParsedNode(nterm, [f])

    raise ParseError(nterm, first)


def parse_factor(grammar: CFG, in_str: str) -> ParsedNode:
    nterm = Nonterminal('FACTOR')

    if in_str.startswith('I') or in_str.startswith('C'):
        return ParsedNode(nterm, [in_str[0]])

    if in_str.startswith('not'):
        targets = ['not']
        f = parse_factor(grammar, in_str[3:])

        return ParsedNode(nterm, targets + [f])

    if in_str.startswith('('):
        targets = ['(']
        in_str = in_str[1:]
        se = parse_start_expr(grammar, in_str)

        targets += [se]
        in_str = in_str[se.parsed_len:]
        if not in_str.startswith(')'):
            raise ParseError(nterm, [')'])
        targets += [')']

        return ParsedNode(nterm, targets)

    first = grammar.get_first(nterm)

    raise ParseError(nterm, first)


def parse_start_expr(grammar: CFG, in_str: str) -> ParsedNode:
    targets = []
    try:
        s = parse_sign(grammar, in_str)
        targets.append(s)
        in_str = in_str[s.parsed_len:]
    except:
        pass

    t = parse_term(grammar, in_str)

    targets.append(t)
    in_str = in_str[t.parsed_len:]

    try:
        opt_startdot = parse_start_expr_dot(grammar, in_str)
        targets.append(opt_startdot)
    except:
        pass

    return ParsedNode(Nonterminal('START_EXPR'), targets)


def parse_start_expr_dot(grammar: CFG, in_str: str) -> ParsedNode:
    targets = []
    s = parse_sum(grammar, in_str)

    targets.append(s)
    in_str = in_str[s.parsed_len:]
    t = parse_term(grammar, in_str)

    targets.append(t)
    in_str = in_str[t.parsed_len:]
    try:
        opt_startdot = parse_start_expr_dot(grammar, in_str)
        targets.append(opt_startdot)
    except:
        pass

    return ParsedNode(Nonterminal('START_EXPR`'), targets)


def parse_term(grammar: CFG, in_str: str) -> ParsedNode:
    targets = []
    f = parse_factor(grammar, in_str)

    targets.append(f)
    in_str = in_str[f.parsed_len:]
    try:
        opt_termdot = parse_term_dot(grammar, in_str)
        targets.append(opt_termdot)
    except:
        pass

    return ParsedNode(Nonterminal('TERM'), targets)


def parse_term_dot(grammar: CFG, in_str: str) -> ParsedNode:
    targets = []
    m = parse_mul(grammar, in_str)

    targets.append(m)

    in_str = in_str[m.parsed_len:]

    f = parse_factor(grammar, in_str)

    targets.append(f)
    in_str = in_str[f.parsed_len:]

    try:
        opt_termdot = parse_term_dot(grammar, in_str)
        targets.append(opt_termdot)
    except:
        pass

    return ParsedNode(Nonterminal('TERM`'), targets)


def parse_calc_expr(grammar: CFG, in_str: str) -> ParsedNode:
    nterm = Nonterminal('CALC_EXPR')
    follow = grammar.get_follow(nterm)
    targets = []

    s = parse_start_expr(grammar, in_str)

    targets.append(s)
    in_str = in_str[s.parsed_len:]

    simple_node = ParsedNode(nterm, targets)
    simple_in_str = in_str[simple_node.parsed_len:]

    try:
        op = parse_cmp(grammar, in_str)
    except ParseError as e:
        return simple_node

    targets.append(op)
    in_str = in_str[op.parsed_len:]

    try:
        s2 = parse_start_expr(grammar, in_str)
    except ParseError as e:
        return simple_node

    targets.append(s2)
    in_str = in_str[s2.parsed_len:]

    return ParsedNode(nterm, targets)


def parse_expr(grammar: CFG, in_str: str) -> ParsedNode:
    targets = []
    nterm = Nonterminal('EXPR')
    follow = grammar.get_follow(nterm)
    orig_in_str = in_str

    if in_str.startswith('C'):
        targets.append('C')
        in_str = in_str[1:]
    else:
        try:
            ce = parse_calc_expr(grammar, orig_in_str)
        except ParseError:
            raise ParseError(nterm, grammar.get_first(nterm))
        return ParsedNode(nterm, [ce])

    try:
        op = parse_assign(grammar, in_str)
    except ParseError as e:
        ce = parse_calc_expr(grammar, orig_in_str)

        return ParsedNode(nterm, [ce])

    targets.append(op)
    in_str = in_str[op.parsed_len:]

    try:
        ce = parse_calc_expr(grammar, in_str)
    except ParseError as e:
        ce = parse_calc_expr(grammar, orig_in_str)

        return ParsedNode(nterm, [ce])

    targets.append(ce)
    in_str = in_str[ce.parsed_len:]

    return ParsedNode(nterm, targets)


def parse_tail(grammar: CFG, in_str: str) -> ParsedNode:
    nterm = Nonterminal('TAIL')
    try:
        targets = []
        if not in_str.startswith(';'):
            raise ParseError(nterm, [';'])
        targets.append(';')
        in_str = in_str[1:]
        e = parse_expr(grammar, in_str)
        targets.append(e)
        in_str = in_str[e.parsed_len:]
        t = parse_tail(grammar, in_str)
        targets.append(t)
        return ParsedNode(nterm, targets)
    except ParseError:
        return ParsedNode(nterm, [])


def parse_ops(grammar: CFG, in_str: str) -> ParsedNode:
    nterm = Nonterminal('OPS')
    expr = parse_expr(grammar, in_str)
    in_str = in_str[expr.parsed_len:]
    t = parse_tail(grammar, in_str)
    return ParsedNode(nterm, [expr, t])


def parse_block(grammar: CFG, in_str: str) -> ParsedNode:
    nterm = Nonterminal('BLOCK')
    if not in_str.startswith('{'):
        raise ParseError(nterm, ['{'])
    in_str = in_str[1:]
    ops = parse_ops(grammar, in_str)
    in_str = in_str[ops.parsed_len:]
    if not in_str.startswith('}'):
        raise ParseError(nterm, ['}'])
    return ParsedNode(nterm, ['{', ops, '}'])


def parse_prog(grammar: CFG, in_str: str) -> ParsedNode:
    in_str = (in_str
              .replace(' ', '')
              .replace('\t', '')
              .replace('\r', '')
              )
    return ParsedNode(Nonterminal('PROG'), [parse_calc_expr(grammar, in_str)])
