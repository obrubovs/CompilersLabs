import json

def grammar_json_parser(file_from):

    grammar = dict()

    data = json.load(open(file_from, 'r'))

    nonterminals = data['grammar']['nonterminalsymbols']
    nonterminals = set(nonterminals)


    terminals = data['grammar']['terminalsymbols']
    terminals = set(terminals)

    production_dicts = data['grammar']['productions']

    grammar['nonterminals'] = nonterminals
    grammar['terminals'] = terminals
    grammar['rules'] = production_dicts
    grammar['start'] = data['grammar']['startsymbol']

    return grammar

def left_recursion_eliminator(grammar_dict):

    nonterminals = grammar_dict['nonterminals']
    terminals = grammar_dict['terminals']
    rules = grammar_dict['rules']
    start = grammar_dict['start']
    new_rules = list()


    for rule in rules:
        alpha = []
        beta = []

        for production in rule['rhs']:
            if production[0] == rule['lhs'] and len(production) >= 1:

                # добавление нового нетерминального символа
                new_nonterm = rule['lhs'] + '1'
                nonterminals.add(new_nonterm)

                alpha.append(production[1:])

                new_rule = dict()
                new_rule['lhs'] = new_nonterm

            else:
                beta.append(production)

        if alpha:
            alpha_rule = dict()
            beta_rule = dict()
            new_nonterm = rule['lhs']+'1'
            alpha_rule['lhs'] = new_nonterm
            alpha_rule['rhs'] = list()
            for a in alpha:
                a.append(new_nonterm)
                alpha_rule['rhs'].append(a)
            alpha_rule['rhs'].append(['eps'])

            new_rules.append(alpha_rule)

            beta_rule['lhs'] = rule['lhs']
            beta_rule['rhs'] = list()
            for b in beta:
                b.append(new_nonterm)
                beta_rule['rhs'].append(b)

            new_rules.append(beta_rule)

        else:
            new_rules.append(rule)




            # for symbol in production:
            #
            #     if (rule['lhs'] == symbol['-name']) and (production.index(symbol) == 0):
            #         new_rule = dict()
            #         new_rhs = list()
            #
            #
            #         for i in rule['rhs'][1:]:
            #             new_rhs.append(i)
            #
            #
            #         new_rule['lhs'] = new_nonterm
            #         new_rule['rhs'] = new_rhs
            #         new_rules.append(new_rule)
            #         break

    new_grammar = dict()
    new_grammar['nonterminals'] = nonterminals
    new_grammar['terminals'] = terminals
    new_grammar['rules'] = new_rules
    new_grammar['start'] = start

    return new_grammar



def print_grammar(grammar_dict):
    print('~~~ Terminals ~~~')
    for t in grammar_dict['terminals']:
        print(t)


    print('\n~ Non-terminals ~')
    for nt in grammar_dict['nonterminals']:
        if nt == grammar_dict['start']:
            print(f'{nt} – start symbol')
        else:
            print(nt)


    print('\n~~~~ Rules ~~~~')
    for r_dict in grammar_dict['rules']:
        left = r_dict['lhs']
        # right = str()
        for prod in r_dict['rhs']:
            right = ' '.join(prod)
            print(f'{left} -> {right}')

grammar = grammar_json_parser('test.json')
print_grammar(grammar)
grammar = left_recursion_eliminator(grammar)
print_grammar(grammar)
