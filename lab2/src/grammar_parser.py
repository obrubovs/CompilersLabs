import json

def grammar_json_parser(file_from):

    grammar = dict()

    data = json.load(open(file_from, 'r'))

    startsymbol = data['grammar']['startsymbol']
    nonterminals = data['grammar']['nonterminalsymbols']
    nonterminals = list(nonterminals)
    start_index = nonterminals.index(startsymbol)
    nonterminals.insert(0, nonterminals.pop(start_index))


    terminals = data['grammar']['terminalsymbols']
    terminals = set(terminals)

    production_dicts = data['grammar']['productions']

    grammar['nonterminals'] = nonterminals
    grammar['terminals'] = terminals
    grammar['rules'] = production_dicts
    grammar['start'] = startsymbol

    return grammar

def immediate_recursion_eliminator(grammar_dict):
    nonterminals = grammar_dict['nonterminals']
    # nonterminals = list(grammar_dict['nonterminals'])
    terminals = grammar_dict['terminals']
    rules = grammar_dict['rules']
    start = grammar_dict['start']
    new_rules = list()

    for i in range(len(nonterminals)):
        nt_i = nonterminals[i]
        i_new_rule = dict()

        nt_i_productions = list(filter(lambda r: r['lhs'] == nt_i, rules))
        if nt_i_productions:
            nt_i_productions = nt_i_productions[0]
            nt_i_productions = nt_i_productions['rhs']
        else:
            break

        nt_i_new_productions = list()

        for j in range(i):
            nt_j = nonterminals[j]


            nt_j_productions = list(filter(lambda r: r['lhs'] == nt_j, rules))
            nt_j_productions = nt_j_productions[0]
            nt_j_productions = nt_j_productions['rhs']

            # for rule in rules:
            #     # проавила i-го нетерминала
            #     if rule['lhs'] == nt_i:
            #         nt_i_productions = rule['rhs']
            #     # проавила j-го нетерминала
            #     elif rule['lhs'] == nt_j:
            #         nt_j_productions = rule['rhs']




            for production_i in nt_i_productions:
                nt_i_new_prod = list()

                # если первый символ текущей продукции nt_i равен nt_j
                if production_i[0] == nt_j:
                    nt_j_new_prod = list()

                    for production_j in nt_j_productions:
                        # если последний символ продукции второго терминала nt_j = eps

                        if production_j[-1] == 'eps':
                            production_j = production_j[:-1]

                        nt_i_new_productions.append(production_j + production_i[1:])
                        print(f'{production_j + production_i[1:]} added to new production')

                elif production_i not in nt_i_new_productions:

                    nt_i_new_productions.append(production_i)
                    print(f'{production_i} added to new production')

                # обновление грамматики
        i_new_rule['lhs'] = nt_i
        i_new_rule['rhs'] = nt_i_new_productions
        print(i_new_rule)


        # nonterminals += list(upd_nonterms)


        if i == 0:
            for k in rules:
                if k['lhs'] == nt_i:
                    i_new_rule = k

        upd_nonterms, i_rule = direct_left_recursion_eliminator(i_new_rule)

        for nt in upd_nonterms:
            if nt not in nonterminals:
                nonterminals.append(nt)

        new_rules.extend(i_rule)

    nonterminals = list(set(nonterminals))
    set_element_index(nonterminals, start, 0)

    new_grammar = dict()
    new_grammar['nonterminals'] = nonterminals
    new_grammar['terminals'] = terminals
    new_grammar['rules'] = new_rules
    new_grammar['start'] = start

    return new_grammar

def direct_left_recursion_eliminator(rule):

    new_nonterminals = list()
    new_nonterminals.append(rule['lhs'])

    new_rules = list()

    alpha = []
    beta = []

    for production in rule['rhs']:
        if production[0] == rule['lhs'] and len(production) >= 1:

            # добавление нового нетерминального символа
            new_nonterm = rule['lhs'] + '1'

            if new_nonterm not in new_nonterminals:
                new_nonterminals.append(new_nonterm)

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
        if beta:
            for b in beta:
                b.append(new_nonterm)
                if b[0] == 'eps':
                    b = b[1:]
                beta_rule['rhs'].append(b)
        else:
            b = new_nonterm
            beta_rule['rhs'].append([new_nonterm])
        new_rules.append(beta_rule)

    else:
        new_rules.append(rule)


    return new_nonterminals, new_rules


def left_factorisation(grammar_dict):
    rules = grammar_dict['rules']
    new_rules = list()
    new_nonterminals = list()
    for rule in rules:
        nonterm = rule['lhs']
        productions = rule['rhs']
        commonTerminal = str()

        if productions:
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
            new_nonterminals.append(new_nonterm)

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
                        beta.append(['eps'])
                    else:
                        beta.append(b)
                else:
                    alpha.append(i)


            new_rules.append({'lhs': nonterm, 'rhs': alpha})
            new_rules.append({'lhs': new_nonterm, 'rhs': beta})

        else:
            new_rules.append(rule)


    upd_nonterminals = grammar_dict['nonterminals'] + new_nonterminals

    new_grammar = dict()
    new_grammar['nonterminals'] = upd_nonterminals
    new_grammar['terminals'] = grammar_dict['terminals']
    new_grammar['rules'] = new_rules
    new_grammar['start'] = grammar_dict['start']
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

def set_element_index(list: list, element, index:int):
    element_index = list.index(element)
    list.insert(index, list.pop(element_index))


def unreachable_symbols_elimination(grammar: dict):
    start = grammar['start']
    rules = grammar['rules']
    nonterminals = grammar['nonterminals']
    reachable_symbols = set()
    reachable_nt = list()
    reachable_nt.append(start)

    for nt in reachable_nt:
        new_reachable_symbols = set()
        rule = list(filter(lambda r: r['lhs'] == nt, rules))
        rule = rule[0]

        for production in rule['rhs']:
            for symbol in production:
                if symbol in nonterminals and symbol not in reachable_nt:
                    reachable_nt.append(symbol)
                new_reachable_symbols.add(symbol)

        if reachable_symbols == (reachable_symbols.update(new_reachable_symbols)):
            break
        else:
            reachable_symbols.update(new_reachable_symbols)

    new_rules = list()
    for nt in reachable_nt:
        rule = list(filter(lambda r: r['lhs'] == nt, rules))
        rule = rule[0]
        new_rule = list()
        for production in rule['rhs']:
            new_production = list()
            for symbol in production:
                if symbol in reachable_symbols:
                    new_production.append(symbol)
                else:
                    break
            new_rule.append(new_production)
        new_rules.append({'lhs': nt, 'rhs': new_rule})

    new_terminals = list(reachable_symbols - set(reachable_nt))
    set_element_index(new_terminals, start, 0)

    new_grammar = dict()
    new_grammar['nonterminals'] = reachable_nt
    new_grammar['terminals'] = start
    new_grammar['rules'] = new_rules
    new_grammar['start'] = grammar['start']
    return new_grammar

grammar = grammar_json_parser('test6.json')

print("~~~ Изначальная грамматика ~~~")
print_grammar(grammar)

grammar = immediate_recursion_eliminator(grammar)
print("~~~ Избавление от левой рекурсии ~~~")
print_grammar(grammar)

grammar = left_factorisation(grammar)
print("~~~ Левая факторизация ~~~")
print_grammar(grammar)

# grammar = unreachable_symbols_elimination(grammar)
print("~~~ Избавление от недосттижимых символов ~~~")
print_grammar(grammar)