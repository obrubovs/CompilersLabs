from __future__ import annotations
from dataclasses import dataclass
from typing import Union, Iterable

from model.nterm import Nonterminal, SYMBOL


@dataclass(frozen=True)
class Production:
    lhs: Nonterminal
    rhs: tuple[SYMBOL, ...]

    @classmethod
    def from_string(cls, s: str) -> list[Production]:
        lhs, tail = s.split('->')
        rhs_s = tail.split('|')

        ret = []
        for rhs_str in rhs_s:
            rhs = list(map(Nonterminal.from_string, rhs_str.split()))
            ret.append(Production(Nonterminal.from_string(lhs), tuple(rhs)))
        return ret

    @classmethod
    def repr_multiple(cls, productions: Iterable[Production], arrow_sep='\t-> ', eq_sep=' | ') -> str:
        productions = list(productions)
        return (productions[0].lhs.symbol + arrow_sep +
                eq_sep.join(map(lambda p: ' '.join(map(str, p.rhs)), productions)))

    def __repr__(self):
        return f'{self.lhs} -> ' + ' '.join(map(str, self.rhs))
