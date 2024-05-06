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
        right = ''
        for symbol in r_dict['rhs']:
            right += symbol['-name']
        print(f'{left} -> {right}')

grammar = grammar_json_parser('test.json')
print_grammar(grammar)
