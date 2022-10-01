from itertools import islice


def grammar_parc():
    all_lines = []
    all_rulles = []
    nonterms = set()
    terms = set()
    with open('test.txt') as f:
        new = f.read().splitlines()
        lines = islice(new, 0, 2)
        rules = islice(new, 2, None)
        all_lines += [line.replace(" ", "") for line in lines]
        all_rulles += [line.split(' -> ') for line in rules]
    nonterms = all_lines[0].split("=")[1].split(',')
    terms = all_lines[1].split("=")[1].split(',')
    return nonterms, terms, all_rulles


def get_term_forms(dict_name, nonterms, all_rulles):
    dict_name = dict_name.fromkeys(nonterms, [])
    for key in dict_name.keys():
        rulles_list = []
        for rule in all_rulles:
            if rule[0] == key:
                rulles_list.append(rule[1].replace(" ", ""))
        dict_name[key] = rulles_list
    return dict_name


def sign_changes(rulles_dict, term_forms_dict, sign):
    for rule in rulles_dict:
        rule[1] = list(rule[1])
        for i in range(len(rule[1])):
            if rule[1][i] in term_forms_dict.keys():
                rule[1][i] = sign
        rule[1] = "".join(rule[1])

    return rulles_dict


def classes_dividing(rules_simplified,num):
    rules_to_class_dict = dict()
    for nonterm, simple_rules in rules_simplified.items():
        s = list(set(simple_rules))
        s.sort()
        r = "|".join(s)
        if r in rules_to_class_dict:
            rules_to_class_dict[r]["nonterms"].append(nonterm)
        else:
            rules_to_class_dict[r] = {"nonterms" : [nonterm], "class_number" : num}
            num += 1

    devided_classes = [(r[1]["nonterms"], r[1]["class_number"]) for r in rules_to_class_dict.items()]
    return devided_classes, num

def dict_changes(nonterms, devided_classes, rules_copy_dict):
    dict_classes = dict()
    dict_classes = dict_classes.fromkeys(nonterms, [])
    for i in range(len(devided_classes)):
        for j in range(len(devided_classes[i][0])):
            if devided_classes[i][0][j] in dict_classes.keys():
                dict_classes[devided_classes[i][0][j]] = devided_classes[i][1]
    for key in dict_classes.keys():
        if dict_classes[key] == []:
            dict_classes[key] = num
            num += 1



    for rule in rules_copy_dict:
        rule[1] = list(rule[1])
        for i in range(len(rule[1])):
            if rule[1][i] in dict_classes.keys():
                rule[1][i] = str(dict_classes[rule[1][i]])
        rule[1] = "".join(rule[1])

    return devided_classes, rules_copy_dict, dict_classes
def helper(term_rules, dict_classes):
    replaced_rules = []
    for rule in term_rules:
        replaced_rule = ""
        for term in rule:
            if term in dict_classes:
                replaced_rule += str(dict_classes[term])
            else:
                replaced_rule += term
        replaced_rules.append(replaced_rule)
    replaced_rules.sort()
    return "|".join(replaced_rules)

def classes_checking(devided_classes, term_forms_dict, dict_classes, num):
    has_work = True
    while has_work:
        has_division = False
        for i, devided_clazz in enumerate(devided_classes):
            class_nonterms, class_number = devided_clazz
            pivot = helper(term_forms_dict[class_nonterms[0]], dict_classes)
            new_classes = dict()
            for nonterm in class_nonterms[1 : ]:
                replaced_rules = helper(term_forms_dict[nonterm], dict_classes)
                if replaced_rules != pivot:
                    has_division = True
                    if replaced_rules in new_classes:
                        new_class_number = new_classes[replaced_rules]
                    else:
                        new_class_number = num + 1
                        new_classes[replaced_rules] = new_class_number
                        num += 1
                    dict_classes[nonterm] = new_class_number
                    devided_classes[i][0].remove(nonterm)
                    for c in devided_classes:
                        if c[1] == new_class_number:
                            c[0].append(nonterm)
                            break
                    else:
                        devided_classes.append(([nonterm], new_class_number))
        has_work = has_division
    return devided_classes, num

def main():
    nonterms, terms, all_rules = grammar_parc()
    _, _, rules_copy_dict = grammar_parc()
    term_forms_dict = dict()
    rules_copy = dict()
    term_forms_dict = get_term_forms(term_forms_dict, nonterms, all_rules)

    classes_of_rules = term_forms_dict.copy()
    new_all_rules = sign_changes(all_rules, term_forms_dict, "_")

    rules_copy = get_term_forms(rules_copy, nonterms, new_all_rules)
    rules_simplified = {elem[0]: elem[1] for elem in rules_copy.items()}

    devided_classes = []
    num = 0
    devided_classes, num = classes_dividing(rules_simplified, num)
    devided_classes, rules_copy_dict, dict_classes = dict_changes(nonterms,devided_classes,rules_copy_dict)
    devided_classes, num = classes_checking(devided_classes,term_forms_dict,dict_classes, num)

    # classes
    ans = []
    # rules
    r = {}

    for nontermz, class_number in devided_classes:
        r.update({class_number: nontermz})

    print(list(r.values()))
    for class_number, nontermz in r.items():
        words = []
        for elem in term_forms_dict[nontermz[0]]:
            c = ""
            for letter in elem:
                if letter in nonterms and letter != r[dict_classes[letter]][0]:
                    letter = r[dict_classes[letter]][0]
                c += letter
            if c in words:
                continue
            words.append(c)
            print(nontermz[0], " -> ", c)
main()