from parser import parse

EPS = 'ε'


def filling(file: str):
    nonterms_dict, rules_dict = parse(file)
    is_epsilon_generative = set()

    for nonterm, value in nonterms_dict.items():
        if 'ε' in value:
            is_epsilon_generative.add(nonterm)
    cfg = CFG(nonterms_dict, rules_dict, is_epsilon_generative)

    return cfg

def find_generative(nonterm, nonterm_list, rules, only_term):
    new_list = [elem for elem in nonterm_list if elem != nonterm]
    for nt in new_list:
        if nonterm in rules[nt] and all (
            nt in only_term for nt in new_list
        ):
            only_term.append(nt)
        if nonterm not in rules[nt]:
            pass
        if nonterm in rules[nt]:
            only_term.append(nt)

class CFG:
    def __init__(
            self,
            nonterms: dict[str:list[str]] = None,
            rules: dict[str:list[str]] = None,
            is_epsilon_generative: set[str] = None,
            eps_context: list[str] = None
    ):
        self.nonterms = nonterms
        self.rules = rules
        self.is_epsilon_generative = is_epsilon_generative
        self.eps_context = eps_context


    # FIXME: не рассмотренны циклические правила
    def delete_non_generative(self):
        only_term = []
        for nonterm, value in self.rules.items():
            for val in value:
                if all(
                        symb not in self.rules.keys() and
                        EPS not in val
                        for symb in val
                ):
                    only_term.append(nonterm)

        is_generating = []
        for nonterm, value in self.rules.items():
            for val in value:
                nonterms_check_list = []
                nonterms_check_list = [
                    symb for symb in val
                    if symb in self.rules.keys()
                ]
                if all(
                        nonterm in only_term
                        for nonterm in nonterms_check_list
                ) and nonterms_check_list:
                    is_generating.append(nonterm)

                if nonterm in nonterms_check_list:
                    if all(
                      nt in only_term
                      for nt in nonterms_check_list if nt != nonterm
                    ):
                        if EPS in value:
                            is_generating.append(nonterm)
                    else:
                        ...
                    #if EPS in value:
                    #    is_generating.append(nonterm)
        return only_term, is_generating

file = 'input1.txt'
cfg = filling(file)
print(cfg.rules)
only_term, is_generating = cfg.delete_non_generative()
print(only_term)
print(is_generating)
