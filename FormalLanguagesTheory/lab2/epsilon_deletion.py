from parser import parse
from copy import copy
from itertools import combinations
nonterms_dict = {}
nonterms_dict = parse('input.txt')

print(nonterms_dict)

is_epsilon_generative = set()
for nonterm, value in nonterms_dict.items():
    if 'ε' in value:
        is_epsilon_generative.add(nonterm)

print(is_epsilon_generative)
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

print(is_epsilon_generative)
print(nonterms_dict)
print(eps_gen_nonterms_dict)



c = ['A','b','C','d','A','C']
l = [0,0,0,0,0,0]
ans = []
for i, el in enumerate(c):
    if el not in is_epsilon_generative:
        l[i] = 1

s = ''
for i, el in enumerate(c):
    if el * l[i] == '':
        continue
    s += el*l[i]
ans.append(s)

for i, el in enumerate(c):
    if el in is_epsilon_generative:
        l[i] = 1
        s = ''
        for i1, el1 in enumerate(c):
            if el1 * l[i1] == '':
                continue
            s += el1 * l[i1]
        l[i] = 0
        ans.append(s)

s = ''
for el in c:
    s += str(el)
print(s)
for i, j in enumerate(s):
    if j in is_epsilon_generative:
        temp = s
        #s = s.replace(j, '', 1)
        s = s[:i] + s[i+1:]
        #if s in ans:
            #s = temp.replace(temp[i], '')
        #    s = temp[:i] + temp[i+1 : ]
        ans.append(s)
        s = temp
print(ans)
