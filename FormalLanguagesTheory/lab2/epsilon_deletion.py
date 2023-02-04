from parser import parse
from copy import copy
from itertools import product


nonterms_dict = {}
nonterms_dict, rules_dict = parse('input1.txt')
final = {}
is_epsilon_generative = set()
for nonterm, value in nonterms_dict.items():
    if 'ε' in value:
        is_epsilon_generative.add(nonterm)

eps_gen_nonterms_dict = copy(nonterms_dict)


# Поиск ε-порождающих нетерминалов
def eps_check(eps_gen_nonterms_dict, nonterms_dict):
    flag = False
    for nonterm, value in eps_gen_nonterms_dict.items():
        if nonterm in is_epsilon_generative:
            continue
        for symbol in value:
            if symbol in is_epsilon_generative:
                if nonterm in is_epsilon_generative:
                    continue
                flag = True
                is_epsilon_generative.add(nonterm)
                del nonterms_dict[nonterm]
                continue
    if flag:
        eps_check(eps_gen_nonterms_dict, nonterms_dict)


eps_check(eps_gen_nonterms_dict, nonterms_dict)


def check_if_eps_in_start(eps_gen_nonterms_dict):
    new_rule = {}
    for nonterm in list(eps_gen_nonterms_dict.keys())[0]:
        if 'ε' in eps_gen_nonterms_dict[nonterm]:
            for val in eps_gen_nonterms_dict.values():
                if nonterm in val:
                    continue
                new_rule[str(nonterm + "'")] = [nonterm, 'ε']
                return new_rule


def comb_finding(eps_gen_nonterms_dict):
    for nonterm, val in eps_gen_nonterms_dict.items():
        ans = []
        l = [0 for k in range(len(val))]
        for i, el in enumerate(val):
            if el not in is_epsilon_generative:
                l[i] = 1
        combs = make_list_of_comb(l)
        for comb in combs:
            s = ''
            for i, el in enumerate(val):
                if el * comb[i] == '':
                    continue
                s += el * comb[i]
            if s != '':
                ans.append(s)
        final[nonterm] = ans
    return final


def make_list_of_comb(l):
    pos = [i for i, e in enumerate(l) if e == 1]
    ans = []
    new = [0 for i in range(len(l)-len(pos))]
    d = product([0, 1], repeat=len(new))

    for e in d:
        ans.append(list(e))

    for i in pos:
        if i != len(l):
            for j in ans:
                j.insert(i,1)
        else:
            for j in ans:
                j.append(1)
    return ans


def eps_deletion():
    new_rule = check_if_eps_in_start(eps_gen_nonterms_dict)
    final = comb_finding(eps_gen_nonterms_dict)
    for nonterm, value in final.items():
        for i, symb in enumerate(value):
            if symb == 'ε':
                del value[i]
            if 'ε' in symb:
                value[i] = symb.replace('ε', '')
    if new_rule:
        for nt, rule in new_rule.items():
            final[nt] = [i for i in rule]
    return final
