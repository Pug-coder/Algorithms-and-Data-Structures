class RightContextDuplication(Exception):
    pass


class Rule:
    def __init__(self, left, rights):
        self.left = left
        if set(rights) == set([Epsilon()]) or len(rights) == 0:
            self.rights = [Epsilon()]
        else:
            self.rights = list(filter(lambda x: x != Epsilon(), rights))

    def __hash__(self):
        return len(str(self.left)) + len(str(self.rights))

    def __eq__(self, o):
        return (
            isinstance(o, Rule)
            and self.left == o.left
            and self.rights == o.rights
        )

    def __str__(self):
        return f'{str(self.left)} -> {"".join(map(str, self.rights))}'

    def __repr__(self):
        return str(self)

    def __getitem__(self, i):
        return self.rights[i]

    def to_term(self):
        return Rule(
            self.left.to_term(), list(map(lambda x: x.to_term(), self.rights))
        )


class Term:
    def __init__(self, symbol):
        assert ord("a") <= ord(symbol) <= ord("z")
        self.symbol = symbol

    def __hash__(self):
        return ord(self.symbol)

    def __eq__(self, o):
        return isinstance(o, Term) and self.symbol == o.symbol

    def __repr__(self):
        return self.symbol

    def __str__(self):
        return self.symbol

    def to_term(self):
        return self


class Nterm:
    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return ord(self.name[-1])

    def __eq__(self, o):
        return isinstance(o, Nterm) and self.name == o.name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def to_term(self):
        return self


class Epsilon:
    def __init__(self):
        self.symbol = "ε"

    def __hash__(self):
        return ord(self.symbol)

    def __eq__(self, o):
        return isinstance(o, Epsilon) and self.symbol == o.symbol

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "ε"

    def to_term(self):
        return self


class Nterm2:
    def __init__(self, children):
        self.children = children
        if len(self[1:]) != len(set(self[1:])):
            raise RightContextDuplication(
                f"Попытка дважды присоединить один и тот же правый контекст: {self}"
            )

    def __str__(self):
        return "❬" + "".join(map(str, self.children)) + "❭"

    def __repr__(self):
        return str(self)

    def __eq__(self, o):
        if isinstance(o, Nterm2):
            return self.children == o.children

        if (
            isinstance(o, Nterm)
            or isinstance(o, Term)
            or isinstance(o, Epsilon)
        ):
            return len(self.children) == 1 and self[0] == o

        raise Exception(f"некоректное сравнение {self} и {o}")

    def __hash__(self):
        return 1  # :)

    def __add__(self, o):
        if isinstance(o, Nterm2):
            o_list = o.children
        elif (
            isinstance(o, Nterm)
            or isinstance(o, Term)
            or isinstance(o, Epsilon)
        ):
            o_list = [o]
        elif isinstance(o, list):
            o_list = o
        return Nterm2(
            self.children if self.children != [Epsilon()] else [] + o_list
        )

    def __getitem__(self, i):
        return self.children[i]

    def __len__(self):
        return len(self.children)

    def to_term(self):
        if len(self) == 1:
            return self[0]
        return Nterm("[" + str(self) + "]")
