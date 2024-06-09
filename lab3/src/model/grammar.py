from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from model.nterm import Nonterminal, EPSYLON_SYMBOL
from model.production import Production


@dataclass(frozen=True)
class CFG:
    _start: Nonterminal
    _productions: list[Production]

    @property
    def start(self) -> Nonterminal:
        return self._start

    @property
    def productions(self) -> list[Production]:
        return self._productions.copy()

    def get_productions_lhs(self,
                            left: Nonterminal,
                            productions_repacement: Optional[list[Production]] = None) -> list[Production]:
        ret = []
        for p in (productions_repacement or self.productions):
            if p.lhs == left:
                ret.append(p)
        return ret

    def get_productions_rhs(self,
                            right: Nonterminal,
                            productions_repacement: Optional[list[Production]] = None) -> list[Production]:
        ret = []
        for p in (productions_repacement or self.productions):
            if right in p.rhs:
                ret.append(p)
        return ret

    def add_postfix(self, nterm: Nonterminal, postfix: str = '′') -> Nonterminal:
        nterms = set(self.nterms)
        while (ret := Nonterminal(nterm.symbol + postfix)) in nterms:
            pass
        return ret

    def get_first(self, item: Nonterminal | str) -> list[str]:
        if isinstance(item, str):
            return [item]
        if item == Nonterminal('ε'):
            return []
        ret = []
        changed = True
        while changed:
            changed = False
            for p in self.get_productions_lhs(item):
                if p.rhs[0] == item:
                    continue
                follow = self.get_first(p.rhs[0])
                for term in follow:
                    if term not in ret:
                        ret.append(term)
                        changed = True
        return list(sorted(ret, key=lambda x: -len(x)))

    def get_follow(self, item: Nonterminal, ignore_nterms: Optional[list[Nonterminal]] = None) -> list[str]:
        if ignore_nterms is None:
            ignore_nterms = [item]
        else:
            ignore_nterms = ignore_nterms.copy() + [item]

        ret = []
        if item == self.start:
            ret.append('$')

        changed = True
        while changed:
            changed = False
            for p in self._productions:
                for r, rnext in zip(p.rhs, p.rhs[1:] + (None,)):
                    if r == item:
                        print(p)
                        if rnext in ignore_nterms:
                            continue

                        if rnext is None and p.lhs not in ignore_nterms:
                            f = self.get_follow(p.lhs, ignore_nterms + [r])
                            ignore_nterms += [p.lhs]
                            for f_item in f:
                                if f_item not in ret and f_item != Nonterminal('ε'):
                                    ret.append(f_item)
                                    changed = True
                            continue
                        f = self.get_first(rnext)
                        for f_item in f:
                            if f_item not in ret and f_item != Nonterminal('ε'):
                                ret.append(f_item)
                                changed = True
                        if Nonterminal('ε') in f:
                            f = self.get_follow(rnext, ignore_nterms + [r])
                            ignore_nterms += [rnext]
                            for f_item in f:
                                if f_item not in ret and f_item != Nonterminal('ε'):
                                    ret.append(f_item)
                                    changed = True

        return ret

    @classmethod
    def fromstring(cls, s: str, start: Optional[Nonterminal] = None) -> CFG:
        productions = list()
        start = None
        for line in s.split('\n'):
            line = line.strip()
            if len(line) == 0:
                continue

            p_s = Production.from_string(line)
            if start is None:
                start = p_s[0].lhs
            for p in p_s:
                productions.append(p)

        if start is None:
            start = Nonterminal('S')
            productions = {Production(start, (EPSYLON_SYMBOL,))}

        return CFG(start, productions)

    @property
    def nterms(self) -> list[Nonterminal]:
        ret = []

        for p in self._productions:
            i = p.lhs
            if i not in ret:
                ret.append(i)
            for i in p.rhs:
                if i not in ret and isinstance(i, Nonterminal):
                    ret.append(i)

        return ret

    def copy_with(self,
                  start: Optional[Nonterminal] = None,
                  productions: Optional[list[Production]] = None) -> CFG:

        return CFG(start or self.start, productions or self.productions)

    def __eq__(self, __value: CFG):
        return self._start == __value._start \
            and len(self._productions) == len(__value._productions) \
            and set(self._productions) == set(__value._productions)

    def remove_direct_left_recursion(self, nterm: Nonterminal) -> CFG:
        new_productions = list()
        productions = self.productions

        new_nterm = self.add_postfix(nterm, '′')
        has_recursion = False

        for p in productions:
            if p.lhs != nterm:
                new_productions.append(p)
            else:
                if p.rhs[0] == nterm:
                    if not has_recursion:
                        has_recursion = True
                    new = Production(new_nterm, p.rhs[1:] + (new_nterm,))
                    new_productions.append(new)
                    new = Production(new_nterm, p.rhs[1:])
                    new_productions.append(new)
                else:
                    new_productions.append(p)
                    new = Production(nterm, p.rhs + (new_nterm,))
                    new_productions.append(new)

        if not has_recursion:
            new_productions = productions

        return self.copy_with(productions=new_productions)

    def remove_arb_left_recursuion(self) -> CFG:
        nterms = self.nterms
        productions = self.productions

        for i, nterm_i in enumerate(nterms):
            for j in range(i):
                nterm_j = nterms[j]
                prods_i = self.get_productions_lhs(nterm_i, productions_repacement=productions)
                prods_j = self.get_productions_lhs(nterm_j, productions_repacement=productions)

                for p in prods_i:
                    if p.rhs[0] == nterm_j:
                        productions.remove(p)
                        for subproduction in prods_j:
                            new = Production(p.lhs, subproduction.rhs + p.rhs[1:])
                            productions.append(new)

            productions = ((self
                            .copy_with(productions=productions)
                            .remove_direct_left_recursion(nterm_i))
                           .productions)

        return CFG(self.start, productions)
