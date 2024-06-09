from parse import  ParsedNode
from model.nterm import Nonterminal

def convert_RPN_factor(parsed: ParsedNode) -> ParsedNode:
    if parsed.nterm != Nonterminal('FACTOR'):
        raise RuntimeError(f'FACTOR Node expcted, but got {parsed.nterm}')

    new_targets = []

    for t in parsed.targets:
        if isinstance(t, str):
            pass
        elif t.nterm == Nonterminal('START_EXPR'):
            t = convert_RPN_start_expr(t)
        elif t.nterm == Nonterminal('FACTOR'):
            t = convert_RPN_factor(t)
        else:
            raise RuntimeError(f'Unexpected node at FACTOR: {t.nterm}')
        new_targets.append(t)

    if new_targets[0] == 'not':
        new_targets = new_targets[::-1]

    return ParsedNode(Nonterminal('FACTOR'), new_targets)


def convert_RPN_term_dot(parsed: ParsedNode) -> ParsedNode:
    if parsed.nterm != Nonterminal('TERM`'):
        raise RuntimeError(f'TERM` Node expcted, but got {parsed.nterm}')

    op_mul = None
    factor = None
    nested_expr = None
    for t in parsed.targets:
        if t.nterm == Nonterminal('TERM`'):
            nested_expr = convert_RPN_term_dot(t)
        elif t.nterm == Nonterminal('FACTOR'):
            factor = convert_RPN_factor(t)
        elif t.nterm == Nonterminal('OP_MUL'):
            op_mul = t

    if op_mul is None:
        raise RuntimeError(f'Node TERM` must contain OP_MUL node')
    if factor is None:
        raise RuntimeError(f'Node TERM` must contain TERM node')

    new_targets = [factor]

    if nested_expr is not None:
        nested_op = nested_expr.targets[-1]
        if nested_op == op_mul:
            new_targets += nested_expr.targets[:-1]
        else:
            replace_nested = ParsedNode(nested_expr.nterm, [new_targets[-1]] + nested_expr.targets)
            new_targets = new_targets[:-1]
            new_targets.append(replace_nested)

    new_targets.append(op_mul)

    return ParsedNode(Nonterminal('TERM`'), new_targets)


def convert_RPN_term(parsed: ParsedNode) -> ParsedNode:
    if parsed.nterm != Nonterminal('TERM'):
        raise RuntimeError(f'TERM Node expcted, but got {parsed.nterm}')
    f = convert_RPN_factor(parsed.targets[0])
    new_targets = [f]
    if len(parsed.targets) == 2:
        nested = convert_RPN_term_dot(parsed.targets[1])
        new_targets += nested.targets
    return ParsedNode(Nonterminal('TERM'), new_targets)


def convert_RPN_start_expr_dot(parsed: ParsedNode) -> ParsedNode:
    if parsed.nterm != Nonterminal('START_EXPR`'):
        raise RuntimeError(f'START_EXPR` Node expcted, but got {parsed.nterm}')

    op_sum = None
    term = None
    nested_expr = None
    for t in parsed.targets:
        if t.nterm == Nonterminal('START_EXPR`'):
            nested_expr = convert_RPN_start_expr_dot(t)
        elif t.nterm == Nonterminal('TERM'):
            term = convert_RPN_term(t)
        elif t.nterm == Nonterminal('OP_SUM'):
            op_sum = t

    if op_sum is None:
        raise RuntimeError(f'Node START_EXPR` must contain OP_SUM node')
    if term is None:
        raise RuntimeError(f'Node START_EXPR` must contain TERM node')

    new_targets = [term]

    if nested_expr is not None:
        nested_op = nested_expr.targets[-1]
        if nested_op == op_sum:
            new_targets += nested_expr.targets[:-1]
        else:
            new_targets.append(nested_expr)

    new_targets.append(op_sum)

    return ParsedNode(Nonterminal('START_EXPR`'), new_targets)


def convert_RPN_start_expr(parsed: ParsedNode) -> ParsedNode:
    if parsed.nterm != Nonterminal('START_EXPR'):
        raise RuntimeError(f'START_EXPR Node expcted, but got {parsed.nterm}')
    new_targets = []

    for t in parsed.targets:
        if not isinstance(t, ParsedNode):
            raise RuntimeError(f'Only nodes allowed in START_EXPR node, but got {t}')

        if t.nterm == Nonterminal('TERM'):
            t = convert_RPN_term(t)
            new_targets.append(t)
        elif t.nterm == Nonterminal('START_EXPR`'):
            t = convert_RPN_start_expr_dot(t)

            new_targets += t.targets
        else:
            new_targets.append(t)

    return ParsedNode(Nonterminal('START_EXPR'), new_targets)


def convert_RPN_calc_expr(parsed: ParsedNode) -> ParsedNode:
    if parsed.nterm != Nonterminal('CALC_EXPR'):
        raise RuntimeError(f'CALC_EXPR Node expcted, but got {parsed.nterm}')

    cmp_nodes = []
    not_cmp_nodes = []

    for target in parsed.targets:
        if isinstance(target, ParsedNode) and target.nterm == Nonterminal('OP_CMP'):
            cmp_nodes.append(target)
        else:
            not_cmp_nodes.append(target)

    if len(cmp_nodes) == 0:
        if len(not_cmp_nodes) != 1:
            raise RuntimeError('Can be only one node if no compare operation at CALC_EXPR')

        ncmp_node = not_cmp_nodes[0]

        if not isinstance(ncmp_node, ParsedNode):
            raise RuntimeError('Can be only nodes in CALC_EXPR')

        return convert_RPN_start_expr(ncmp_node)

    if len(cmp_nodes) != 1:
        raise RuntimeError('Can be only one compare operation at CALC_EXPR')

    cmp_node = cmp_nodes[0]
    if not isinstance(cmp_node, ParsedNode):
        raise RuntimeError('Can be only nodes in CALC_EXPR')

    new_targets = []
    for ncmp_node in not_cmp_nodes:
        if not isinstance(ncmp_node, ParsedNode):
            raise RuntimeError('Can be only node in CALC_EXPR targets')
        new_targets.append(convert_RPN_start_expr(ncmp_node))

    return ParsedNode(Nonterminal('CALC_EXPR'), new_targets + [cmp_node])


def convert_to_RPN(parsed: ParsedNode) -> ParsedNode:
    if parsed.nterm != Nonterminal('PROG'):
        raise RuntimeError(f'Only PROG node can be applied, got {parsed.nterm}')

    tgts = parsed.targets
    if len(tgts) != 1:
        raise RuntimeError(f'Only one target can be in PROG node, got {len(tgts)}')

    tgt = tgts[0]

    if not isinstance(tgt, ParsedNode):
        raise RuntimeError(f'Only nodes can be provided as a target be in PROG node, got {tgt}')

    return convert_RPN_calc_expr(tgt)