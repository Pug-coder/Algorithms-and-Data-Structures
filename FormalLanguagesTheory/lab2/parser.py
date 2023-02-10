import re
from more_itertools import locate

from cfg import CFG
from rule import *


class CFG_Parser:
    def __init__(self, filename):
        with open(filename, "r") as f:
            print("####file#####")
            string = f.read()
            print(string)
            print("#############\n")
            self.string = "".join(filter(lambda x: not str.isspace(x), string))

    def glance(self):
        if self.string == "":
            return False
        return self.string[0]

    def next(self):
        if self.string == "":
            return False
        ret = self.string[0]
        self.string = self.string[1:]
        return ret

    def get_nterm(self):
        match = re.match("^\[[A-Z,a-z]+\]", self.string)
        if not match:
            return False

        nterm = match.group(0)
        self.string = self.string[len(nterm) :]
        return Nterm(nterm)

    def get_term_or_eps(self):
        if self.glance().isalpha():
            return Term(self.next())
        if self.glance() == "|":
            return self.next()
        # if self.glance() == 'ε':
        #     self.next()
        #     return 'eps'
        #     # return Epsilon()

    def get_arrow(self):
        if self.glance() == "-":
            if self.next() == "-" and self.next() == ">":
                return "->"
            else:
                raise Exception("OBMANKA")

        return False

    def parse_seq(self):
        shtuchki = []
        while self.string:
            to_append = (
                self.get_nterm() or self.get_term_or_eps() or self.get_arrow()
            )
            if not to_append:
                break
            shtuchki.append(to_append)

        assert self.string == ""
        return list(filter(bool, shtuchki))

    def parse_rules(self):
        seq = self.parse_seq()
        rules_set = set()
        rules_raw = []
        arrow_index = -1
        while arrow_index:
            try:
                arrow_index = seq.index("->")
                second_arrow_index = seq.index("->", arrow_index + 1)
            except:
                rules_raw.append(seq)
                break

            rules_raw.append(seq[: second_arrow_index - 1])
            seq = seq[second_arrow_index - 1 :]

        for rule_list in rules_raw:
            assert rule_list[1] == "->"
            left, rights = rule_list[0], rule_list[2:]

            if rights == []:
                new_rule = Rule(left, [Epsilon()])
                print("NEW RULE:", new_rule)
                rules_set.add(new_rule)
                continue

            if rights[0] == "|":
                new_rule = Rule(left, [Epsilon()])
                print("NEW RULE:", new_rule)
                rules_set.add(new_rule)
                rights = rights[1:]

            list_candidate = []
            while rights:
                if rights[0] == "|":
                    assert list_candidate != []
                    new_rule = Rule(left, list_candidate)
                    print("NEW RULE:", new_rule)
                    rules_set.add(new_rule)
                    list_candidate = []
                else:
                    list_candidate.append(rights[0])
                rights = rights[1:]

            assert list_candidate != []
            new_rule = Rule(left, list_candidate)
            print("NEW RULE:", new_rule)
            rules_set.add(new_rule)

            # idx = list(locate(rights, lambda x: x == '|'))
            # for i,j in zip([0]+idx, idx+[None]):
            #     print(i, j, rights[i:j], idx)
            #     new_rule = Rule(left, rights[i:j] if i != j else [Epsilon()])
            #     print('NEW RULE:', new_rule)
            #     rules_set.add(new_rule)

        return CFG(rules_set)
