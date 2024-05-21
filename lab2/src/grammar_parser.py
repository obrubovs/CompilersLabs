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

def immediate_recursion_eliminator(grammar_dict):
    nonterminals = list(grammar_dict['nonterminals'])
    terminals = grammar_dict['terminals']
    rules = grammar_dict['rules']
    start = grammar_dict['start']
    new_rules = list()

    for i in range(len(nonterminals)):
        nt_i = nonterminals[i]
        i_new_rule = dict()

        for j in range(i):
            nt_j = nonterminals[j]

            for rule in rules:
                # проавила i-го нетерминала
                if rule['lhs'] == nt_i:
                    nt_i_rules = rule['rhs']
                # проавила j-го нетерминала
                elif rule['lhs'] == nt_j:
                    nt_j_rules = rule['rhs']


            nt_i_new_productions = list()

            for production_i in nt_i_rules:
                nt_i_new_prod = list()

                # если первый символ текущей продукции nt_i равен nt_j
                if production_i[0] == nt_j:
                    nt_j_new_prod = list()

                    for production_j in nt_j_rules:
                        # если последний символ продукции второго терминала nt_j = eps

                        if production_j[-1] == 'eps':
                            production_j = production_j[:-1]

                        nt_i_new_productions.append(production_j + production_i[1:])
                        print(f'{production_j + production_i[1:]} added to new production')


                    # итерация по правилам j-го нетерминала
                    # for production_j in nt_j_rules:
                    #
                    #     # если последний символ продукции второго терминала nt_j = eps
                    #     if production_j[-1] == 'eps':
                    #         production_j = production_j[:-1]
                    #
                    #     # добавление правила nt_j и остаток правила nt_i
                    #     nt_i_new_productions.append(production_j + production_i[1:])
                    #     print(f'{production_j + production_i[1:]} added to nt_i production')
                else:

                    nt_i_new_productions.append(production_i)
                    print(f'{production_i} added to new production')

                # обновление грамматики
            i_new_rule['lhs'] = nt_i
            i_new_rule['rhs'] = nt_i_new_productions
            print(i_new_rule)

            upd_nonterms, i_rule = direct_left_recursion_eliminator(i_new_rule)

            nonterminals += list(upd_nonterms)

            new_rules.extend(i_rule)

        if i == 0:
            for k in rules:
                if k['lhs'] == nt_i:
                    new_rules.append(k)


    new_grammar = dict()
    new_grammar['nonterminals'] = set(nonterminals)
    new_grammar['terminals'] = terminals
    new_grammar['rules'] = new_rules
    new_grammar['start'] = start

    return new_grammar

# def direct_left_recursion_eliminator(grammar_dict):
#
#     nonterminals = grammar_dict['nonterminals']
#     terminals = grammar_dict['terminals']
#     rules = grammar_dict['rules']
#     start = grammar_dict['start']
#     new_rules = list()
#
#
#     for rule in rules:
#         alpha = []
#         beta = []
#
#         for production in rule['rhs']:
#             if production[0] == rule['lhs'] and len(production) >= 1:
#
#                 # добавление нового нетерминального символа
#                 new_nonterm = rule['lhs'] + '1'
#                 nonterminals.add(new_nonterm)
#
#                 alpha.append(production[1:])
#
#                 new_rule = dict()
#                 new_rule['lhs'] = new_nonterm
#
#             else:
#                 beta.append(production)
#
#         if alpha:
#             alpha_rule = dict()
#             beta_rule = dict()
#             new_nonterm = rule['lhs']+'1'
#             alpha_rule['lhs'] = new_nonterm
#             alpha_rule['rhs'] = list()
#             for a in alpha:
#                 a.append(new_nonterm)
#                 alpha_rule['rhs'].append(a)
#             alpha_rule['rhs'].append(['eps'])
#
#             new_rules.append(alpha_rule)
#
#             beta_rule['lhs'] = rule['lhs']
#             beta_rule['rhs'] = list()
#             for b in beta:
#                 b.append(new_nonterm)
#                 beta_rule['rhs'].append(b)
#
#             new_rules.append(beta_rule)
#
#         else:
#             new_rules.append(rule)
#
#
#
#
#             # for symbol in production:
#             #
#             #     if (rule['lhs'] == symbol['-name']) and (production.index(symbol) == 0):
#             #         new_rule = dict()
#             #         new_rhs = list()
#             #
#             #
#             #         for i in rule['rhs'][1:]:
#             #             new_rhs.append(i)
#             #
#             #
#             #         new_rule['lhs'] = new_nonterm
#             #         new_rule['rhs'] = new_rhs
#             #         new_rules.append(new_rule)
#             #         break
#
#     new_grammar = dict()
#     new_grammar['nonterminals'] = nonterminals
#     new_grammar['terminals'] = terminals
#     new_grammar['rules'] = new_rules
#     new_grammar['start'] = start
#
#     return new_grammar

def direct_left_recursion_eliminator(rule):

    new_nonterminals = set()
    new_nonterminals.add(rule['lhs'])

    new_rules = list()

    alpha = []
    beta = []

    for production in rule['rhs']:
        if production[0] == rule['lhs'] and len(production) >= 1:

            # добавление нового нетерминального символа
            new_nonterm = rule['lhs'] + '1'

            if new_nonterm in new_nonterminals:
                break
            new_nonterminals.add(new_nonterm)

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
            if b[0] == 'eps':
                b = b[1:]
            beta_rule['rhs'].append(b)

        new_rules.append(beta_rule)

    else:
        new_rules.append(rule)


    return new_nonterminals, new_rules


def left_factorisation(grammar_dict):
    rules = grammar_dict['rules']
    new_rules = list()
    new_nonterminals = set()
    for rule in rules:
        nonterm = rule['lhs']
        productions = rule['rhs']
        commonTerminal = str()
        for i in range(0, len(productions[0])): # итерация по первой продукции
            for j in range(1, len(productions)): # итерация по всем продукциям нетерминала
                if productions[0][:i+1] == productions[j][:i+1]:
                    commonTerminal = productions[0][:i+1]

        if commonTerminal:
            # добавление нового нетерминала
            nt_index = 1
            new_nonterm = nonterm + str(nt_index)
            while new_nonterm in grammar_dict['nonterminals']:
                nt_index += 1
                new_nonterm = nonterm + str(nt_index)
            new_nonterminals.add(new_nonterm)

            # создание новых правил
            alpha = list()
            beta = list()

            commonTerminalProduction = commonTerminal[:]
            commonTerminalProduction.append(new_nonterm)
            alpha.append(commonTerminalProduction)

            for i in productions:
                if i[:len(commonTerminal)] == commonTerminal:
                    b = i[len(commonTerminal):]
                    if len(b) == 0:
                        beta.append('eps')
                    else:
                        beta.append(b)
                else:
                    alpha.append(i)


            new_rules.append({'lhs': nonterm, 'rhs': alpha})
            new_rules.append({'lhs': new_nonterm, 'rhs': beta})


    new_grammar = dict()
    new_grammar['nonterminals'] = set(new_nonterminals)
    new_grammar['terminals'] = grammar['terminals']
    new_grammar['rules'] = new_rules
    new_grammar['start'] = grammar['start']
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
        right = str()
        for prod in r_dict['rhs']:

            right += ' '.join(prod) + ' | '
        print(f'{left} -> {right[:-2]}')

grammar = grammar_json_parser('test5.json')
print_grammar(grammar)
# grammar = direct_left_recursion_eliminator(grammar)
print_grammar(grammar)
grammar = immediate_recursion_eliminator(grammar)

grammar = left_factorisation_elimination(grammar)
print_grammar(grammar)
