from copy import deepcopy
from rule import *


class CFG:
    def __init__(self, rules_set):
        self.rules = rules_set
        self.terms = self.get_terms(rules_set)
        self.nterms = self.get_nterms(rules_set)
        self.start = Nterm("[S]")

        self.rules2 = set()
        self.Nstreak = set()
        self.buid_dependency_graph()
        self.find_nullables()

    def __str__(self):
        return "\n".join(
            [
                "#" * 15,
                "Grammar:",
                *sorted(list(map(lambda x: "    " + str(x), self.rules))),
                "Nullables: " + str(self.N0),
                "#" * 15,
            ]
        )

    ############################################################
    #           useful tools
    ############################################################

    def get_rules_by_lelft_nerm(self, nterm):
        return set(filter(lambda x: x.left == nterm, self.rules))

    @staticmethod
    def get_streak(nterm):
        return Nterm(nterm.name[:-1] + "']")

    def convert_rule_to_nterms2(self, rule):
        return Rule(
            Nterm2([rule.left]), self.split_rights_to_nterms2(rule.rights)
        )

    def split_rights_to_nterms2(self, rights):
        nterms2_list = []
        list_candidate = []
        while rights:
            if list_candidate == [] or rights[0] in self.N0:
                list_candidate.append(rights[0])
                rights = rights[1:]
            else:
                nterms2_list.append(Nterm2(list_candidate))
                list_candidate = []
        nterms2_list.append(Nterm2(list_candidate))
        return nterms2_list

    # def update_rules2(self, rules2):
    #     for rule2 in rules2:
    #         self.rules2.add(rule2)
    #         self.Nstreak.add(rule2.left)
    #         self.Nstreak |= rule2.rights

    ############################################################
    #           подготовка
    ############################################################

    def get_terms(self, rules_set):
        terms_set = set()
        for rule in rules_set:
            rule_list = [rule.left] + rule.rights
            for tnt in rule_list:
                if isinstance(tnt, Term):
                    terms_set.add(tnt)
        return terms_set

    def get_nterms(self, rules_set):
        nterms_set = set()
        for rule in rules_set:
            rule_list = [rule.left] + rule.rights
            for tnt in rule_list:
                if isinstance(tnt, Nterm):
                    nterms_set.add(tnt)
        # for t in nterms_set:
        #     # print()(t)
        return nterms_set

    """
    Строит граф зависимостей в КСГ
    используется в конструкторе
    не меняет объект
    """

    def buid_dependency_graph(self):
        child_relations = {}
        parent_relations = {}
        for rule in self.rules:
            left = rule.left
            rights = list(filter(lambda x: isinstance(x, Nterm), rule.rights))

            if left not in child_relations:
                child_relations[left] = set(rights)
            else:
                child_relations[left].update(rights)

            for right in rights:
                if right not in parent_relations:
                    parent_relations[right] = set([left])
                else:
                    parent_relations[right].add(left)

        self.child_relations = child_relations
        self.parent_relations = parent_relations

        return self

    """
    Ищет нетермы, которые МОГУТ раскрыться в eps
    Сохраняет множество таких нетермов в поле объекта N0 , а остальные в N1
    """

    def find_nullables(self):
        self.N0 = set()
        flag = True
        tmp = deepcopy(self.rules)
        while flag:
            flag = False
            for rule in tmp:
                if len(rule.rights) == 1 and isinstance(
                    rule.rights[0], Epsilon
                ):
                    flag = True
                    self.N0.add(rule.left)
                    tmp.remove(rule)
                    break
                if all(
                    map(lambda x: isinstance(x, Nterm), rule.rights)
                ) and all(map(lambda x: x in self.N0, rule.rights)):
                    self.N0.add(rule.left)
                    flag = True
                    tmp.remove(rule)
                    break

        self.N1 = self.nterms - self.N0
        return self

    ############################################################
    #           первичная отчистка
    ############################################################

    """
    Создает новый объект, в правилах которого удалены недостижимые нетерминалы
    """

    def remove_unreachable_symbols(self):

        # скажем, что стартовый символ достижим
        self.reachable = set([self.start])
        # про остальные пока не понятно
        unallocated = self.nterms.difference(self.reachable)

        while True:
            upow = len(unallocated)

            unallocated_copy = deepcopy(unallocated)
            for nterm in unallocated_copy:
                # если у трема есть родитель и этот родитель достижим, значит терм достижим
                if (
                    nterm in self.parent_relations
                    and set(self.parent_relations[nterm]) & self.reachable
                ):
                    # то пересаживаем его к достижимым
                    self.reachable.add(nterm)
                    unallocated.remove(nterm)

            new_upow = len(unallocated)

            if new_upow == upow:
                break

        new_rules = set(filter(lambda x: x.left in self.reachable, self.rules))

        return CFG(new_rules)

    """
    Возвращает новый объект, в котором удалены nonegenerating правила
    (nongenerating - непораждающие. Для них в правой части всегда стоит хотя бы один нетерминал)
    """

    def remove_nongenerating_rules(self):
        genetaring_nterm = set()
        for rule in self.rules:
            left = rule.left
            rights = rule.rights
            if all(map(lambda x: isinstance(x, Term), rights)):
                genetaring_nterm.add(left.name)
        while True:
            upow = len(genetaring_nterm)
            for rule in self.rules:
                left = rule.left
                rights = rule.rights
                flag = True
                for r in rights:
                    if isinstance(r, Nterm) and not r.name in genetaring_nterm:
                        flag = False
                        break
                if flag:
                    genetaring_nterm.add(left.name)

            new_upow = len(genetaring_nterm)
            if upow == new_upow:
                break
        new_rules = []
        for rule in self.rules:
            rights = rule.rights
            if any(
                map(
                    lambda x: isinstance(x, Nterm)
                    and not x.name in genetaring_nterm,
                    rights,
                )
            ):
                continue
            new_rules.append(rule)
        return CFG(new_rules)

    def clean(self):
        return self.remove_nongenerating_rules().remove_unreachable_symbols()

    ############################################################
    #           убираем nullables в начале правых частей
    #           aka создаем streaked
    ############################################################

    """
    Создаем notnullable-копии nullable нетерминалов
    Возвращает правила раскрытия для nullable'
    """

    def get_streaked_rules(self):
        print("\n------------------")
        print("CREATING NOTNULLABLE COPIES")
        new_productions = set()
        print(self.nterms)
        # для каждого nullable нетерминала
        for nterm in self.N0:
            print("DEALING WITH NTERM", nterm)
            # получаем все правые части продукций для конкретного нетерминала nterm
            rights_set = map(
                lambda x: x.rights, self.get_rules_by_lelft_nerm(nterm)
            )
            streaked = CFG.get_streak(nterm)

            for rights in rights_set:
                if rights == [Epsilon()] or not rights:
                    continue

                if any(
                    map(lambda x: isinstance(x, Term) or x in self.N1, rights)
                ):
                    new_rule = Rule(streaked, rights)
                    print("    new rule:", new_rule)
                    new_productions.add(new_rule)
                    continue

                if all(map(lambda x: x in self.N0, rights)):
                    while rights and rights != tuple([Epsilon()]):
                        first = rights[0]
                        # если мы все еще считываем префикс из nullable нетерминалов
                        if first in self.N0:
                            # сразу отрезаем первый nullable нетерминал
                            rights = rights[1:]
                            new_rule = Rule(
                                streaked, [CFG.get_streak(first)] + rights
                            )
                            print("    new rule:", new_rule)
                            new_productions.add(new_rule)
                    continue
        print("------------------")
        return new_productions

    def replace_nullables_in_the_beginning_of_right_parts(self):
        def loop(grammar):
            nullable_start_rules = set(
                filter(lambda x: x.rights[0] in grammar.N0, grammar.rules)
            )
            new_rules = set()
            for nullable_start_rule in nullable_start_rules:
                # пусть есть правило A -> B gamma, B in N0
                # создаем правило A -> B' gamma
                rule_copy1 = deepcopy(nullable_start_rule)
                rule_copy1.rights[0] = CFG.get_streak(rule_copy1.rights[0])
                new_rules.add(rule_copy1)
                print(f"replacing {nullable_start_rule}")
                print("    with", rule_copy1)
                # создаем правило A -> eps gamma
                if len(nullable_start_rule.rights) > 1:
                    rule_copy2 = deepcopy(nullable_start_rule)
                    rule_copy2.rights = rule_copy2.rights[1:]
                    new_rules.add(rule_copy2)
                    print("    with", rule_copy2)

            return new_rules, nullable_start_rules

        print("\n------------------")
        print("REPLACING OCCURENCES WITH STREAKED AND NOTHING")
        rules = self.rules
        to_add, to_delete = loop(self)
        while to_add or to_delete:
            rules = (rules | to_add) - to_delete
            to_add, to_delete = loop(CFG(rules))
        print("------------------")
        return CFG(rules)

    def build_lemma1_satisfying_grammar(self):
        grammar_with_streaked = CFG(self.rules | self.get_streaked_rules())
        return (
            grammar_with_streaked.replace_nullables_in_the_beginning_of_right_parts()
        )

    ############################################################
    #           переходим к "большим" нетерминалам
    #           https://www.sciencedirect.com/science/article/pii/S0019995870904468
    ############################################################

    def get_nstreak_start_set(self):
        l = list(
            map(
                lambda x: set(self.convert_rule_to_nterms2(x).rights),
                self.rules,
            )
        )
        if l:
            return set.union(*l)
        return set()

    def get_nstreak_update_from_rules2(self, rules2):
        l = list(map(lambda x: set([x.left]) | set(x.rights), rules2))
        if l:
            return set.union(*l)
        return set()

    def build_rules2(self):
        print("\n------------------")
        print("BUILDING RIGHT-CONTEXT RULES")
        self.Nstreak |= self.get_nstreak_start_set()
        print("NEW ITERATION")
        new_rules2 = (
            self.build_type1_rules2()
            | self.build_type2_rules2()
            | self.build_type3_rules2()
        )
        while new_rules2:
            self.rules2 |= new_rules2
            self.Nstreak |= self.get_nstreak_update_from_rules2(new_rules2)
            print("NEW ITERATION")
            new_rules2 = (
                self.build_type1_rules2()
                | self.build_type2_rules2()
                | self.build_type3_rules2()
            )
        print("------------------\n")
        return self

    def build_type1_rules2(self):
        # есть правило B -> gamma1

        # B in self.N1
        # gamma in self.N0*
        # [B gamma] in self.Nstreak

        # тогда добавим правило [B gamma] -> gamma1 + gamma
        new_rules = set()
        for B in self.N1:
            for rule in self.get_rules_by_lelft_nerm(B):
                gamma1 = rule.rights
                for Bgamma in filter(lambda x: x[0] == B, self.Nstreak):
                    gamma = Bgamma[1:]
                    new_rule = Rule(
                        Bgamma, self.split_rights_to_nterms2(gamma1 + gamma)
                    )
                    if not new_rule in self.rules2:
                        new_rules.add(new_rule)
                        print("new rule type 1:", new_rule)
        return new_rules

    def build_type2_rules2(self):
        # b in self.terms
        # A in self.N0
        # gamma1, gamma2 in self.N0*
        # [b gamma1 A gamma2] in self.Nstreak

        # Есть правило A -> gamma, gamma != eps

        # тогда добавим [b gamma1 A gamma2] -> [b] gamma + gamma2
        new_rules = set()
        for nterm2 in filter(lambda x: isinstance(x[0], Term), self.Nstreak):
            b = Nterm2([nterm2[0]])
            g1Ag2 = nterm2[1:]
            for i, A in enumerate(g1Ag2):
                g1 = g1Ag2[:i]
                g2 = g1Ag2[i + 1 :]
                for rule in filter(
                    lambda x: x.left == A and x.rights != [Epsilon()],
                    self.rules,
                ):
                    g = rule.rights
                    new_rule = Rule(
                        nterm2, [b] + self.split_rights_to_nterms2(g + g2)
                    )
                    if not new_rule in self.rules2:
                        new_rules.add(new_rule)
                        print("new rule type 2:", new_rule)
        return new_rules

    def build_type3_rules2(self):
        # b in self.terms
        # gamma in self.N0+
        # [b gamma] in self.Nstreak

        # тогда добавим [b gamma] -> [b]
        new_rules = set()
        for nterm2 in filter(
            lambda x: len(x) >= 2 and isinstance(x[0], Term), self.Nstreak
        ):
            b = nterm2[0]
            new_rule = Rule(nterm2, [Nterm2([b])])
            if not new_rule in self.rules2:
                new_rules.add(new_rule)
                print("new rule type 3:", new_rule)
        return new_rules

    ############################################################
    #           композиция методов
    ############################################################

    def after_all(self):
        converted = set(
            map(lambda x: self.convert_rule_to_nterms2(x), self.rules)
        )
        new_rules = set(map(lambda x: x.to_term(), converted | self.rules2))
        return CFG(new_rules)

    def lab_pipelene(self):
        try:
            return (
                self.clean()
                .build_lemma1_satisfying_grammar()
                .build_rules2()
                .after_all()
                .clean()
            )
        except RightContextDuplication as e:
            print("\n" + "!" * 50)
            print(e)
            print(
                "Оказалось, что грамматика не LL(k)\nВот промежуточная версия:"
            )
            for x in self.rules | self.rules2:
                print(x)
