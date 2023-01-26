from parser import parse
from copy import copy
from itertools import product

nonterms_dict = {}
nonterms_dict = parse('input.txt')



is_epsilon_generative = set()
for nonterm, value in nonterms_dict.items():
    if 'ε' in value:
        is_epsilon_generative.add(nonterm)

#print(is_epsilon_generative)
eps_gen_nonterms_dict = copy(nonterms_dict)

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

#print(is_epsilon_generative)
#print(nonterms_dict)
#print(eps_gen_nonterms_dict)


final = {}
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
    final = comb_finding(eps_gen_nonterms_dict)
    #print(final)

    for nonterm, value in final.items():
        for i, symb in enumerate(value):
            if symb == 'ε':
                del value[i]
            if 'ε' in symb:
                value[i] = symb.replace('ε', '')
    #print(final)
    return final
