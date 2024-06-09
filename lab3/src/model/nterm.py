from __future__ import annotations
from dataclasses import dataclass
from typing import Union

SYMBOL = Union[str, 'Nonterminal']


@dataclass(frozen=True)
class Nonterminal:
    symbol: str

    @classmethod
    def from_string(cls, s: str) -> SYMBOL:
        s = s.strip()
        if s.startswith("'") and s.endswith("'") and len(s) > 2:
            return s[1:-1]
        return Nonterminal(s)

    def __repr__(self):
        return f'Nonterminal({self.symbol})'

    def __eq__(self, other):
        return isinstance(other, Nonterminal) and self.symbol == other.symbol


EPSYLON_SYMBOL = Nonterminal('ε')
