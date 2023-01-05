import graphviz
import networkx as nx
from pprint import pprint
from copy import copy, deepcopy


class MFA:
    def __init__(self, declarations):
        self.nodes = set()
        self.edges = set()
        self.lables = {}
        self.inits = set()
        self.finals = set()
        memory_len = -1

        # here add what we parsed
        for dtype, dec in declarations:
            if dtype == "node":
                node_id = dec["id"]
                self.nodes.add(node_id)

                if dec["label"]:
                    self.lables[dec["id"]] = dec["label"]

                for flag in dec["flags"]:
                    if flag == "init_flag":
                        self.inits.add(node_id)
                    elif flag == "final_flag":
                        self.finals.add(node_id)
                    else:
                        raise Exception(f"unknown flag {flag}")

            elif dtype == "edge":
                node_id1 = dec["from"]
                node_id2 = dec["to"]
                symbol = dec["symbol"]
                memory = dec["memory"]

                # check equality length
                if memory_len == -1:
                    memory_len = len(memory)
                else:
                    assert len(memory) == memory_len

                # check is symbol normal
                if symbol.isdigit():
                    assert int(symbol) <= memory_len and int(symbol) > 0
                else:
                    assert (
                        symbol == "eps" or symbol == "any" or len(symbol) == 1
                    )

                self.nodes.add(node_id1)
                self.nodes.add(node_id2)

                self.edges.add((node_id1, node_id2, symbol, tuple(memory)))

        # start conditions size must be one
        assert len(self.inits) == 1
        self.find_traps()

        self.set_alphabeth()
        self.normalize_edges()
        # is deterministic
        self.detect_edges_flags()

    def find_traps(self):
        self.numbering = dict([(x, i) for (i, x) in enumerate(self.nodes)])
        self.rev_numbering = dict([(i, x) for (i, x) in enumerate(self.nodes)])
        network = nx.MultiDiGraph()
        [
            network.add_edge(self.numbering[x[0]], self.numbering[x[1]])
            for x in self.edges
        ]
        connection_num = nx.all_pairs_node_connectivity(network)
        connection = {}
        for key, value in connection_num.items():
            nums = set(filter(lambda x: value[x] == 1, value.keys()))
            nums.add(key)
            connection[self.rev_numbering[key]] = set(
                map(lambda x: self.rev_numbering[x], nums)
            )
        self.traps = set()
        for n in self.nodes:
            if not self.finals & connection[n]:
                self.traps.add(n)

    def set_alphabeth(self):
        self.alphabeth = set(
            filter(
                lambda x: x != "eps" and x != "any" and not x.isdigit(),
                map(lambda x: x[2], self.edges),
            )
        )

    def normalize_edges(self):
        # replace all "any" for transition set by every symbol
        any_edges = set(filter(lambda x: x[2] == "any", self.edges))
        for ae in any_edges:
            c = list(copy(ae))
            for alpha in self.alphabeth:
                c[2] = alpha
                self.edges.add(tuple(c))
            self.edges.discard(ae)

            # collect all in "any"
        # for every edge
        for node in self.nodes:
            # all what come out
            transits = set(filter(lambda x: x[0] == node, self.edges))
            # split by groups
            groups = dict([(node, set()) for node in self.nodes])
            for transit in transits:
                groups[transit[1]].add(transit[2:])

            to_pop = [
                key if not value else None for key, value in groups.items()
            ]
            [groups.pop(key) if key else None for key in to_pop]

            # for every distanation
            for destination in groups:
                # print('##############')
                # print(node, '->', destination,)
                # print(groups[destination])

                flags_to_alpha = dict(
                    [(y, set()) for _, y in groups[destination]]
                )
                [flags_to_alpha[y].add(x) for x, y in groups[destination]]
                print("F2A", flags_to_alpha)
                for key_combination, alphas_set in flags_to_alpha.items():
                    # print(key_combination, alphas_set, self.alphabeth)
                    if alphas_set == self.alphabeth:
                        # print('CAN COLLECT', key_combination)
                        s = set(
                            map(
                                lambda alpha: (
                                    node,
                                    destination,
                                    alpha,
                                    key_combination,
                                ),
                                self.alphabeth,
                            )
                        )
                        print(s)
                        self.edges = self.edges.difference(s)
                        self.edges.add(
                            (node, destination, "any", key_combination)
                        )

        pprint(self.edges)

    def detect_edges_flags(self):
        self.deterministic = set()
        for node in self.nodes:
            print("NODE", node)
            transits = set(filter(lambda x: x[0] == node, self.edges))
            if len(transits) == 0:
                continue
            if len(transits) == 1:
                self.deterministic.add(transits.pop())
                continue
            if any(
                filter(
                    lambda x: x[2] == "any" or x[2] == "eps" or x[2].isdigit(),
                    transits,
                )
            ):
                continue
            for alpha in self.alphabeth:
                alpha_transits = set(filter(lambda x: x[2] == alpha, transits))
                if len(alpha_transits) == 1:
                    self.deterministic.add(alpha_transits.pop())

        self.readings = set(filter(lambda edge: edge[2].isdigit(), self.edges))
        for e in self.edges:
            print(e, any(map(lambda x: x != "c", e[3])))
            for x in e[3]:
                print(x, "c", x == "c")
        self.writings = set(
            filter(
                lambda edge: any(map(lambda x: x != "c", edge[3])), self.edges
            )
        )
        self.memory_independend = set(
            filter(lambda edge: not edge[2].isdigit(), self.edges)
        )
        pprint(self.deterministic)

    def create_graph(self):
        dot = graphviz.Digraph()

        for node_id, label in self.lables.items():
            dot.node(node_id, label)
        for node_id in self.nodes:
            dot.node(
                node_id,
                shape="doublecircle"
                if node_id in self.finals
                else "egg"
                if node_id in self.inits
                else "box"
                if node_id in self.traps
                else "circle",
            )

        for edge in self.edges:
            color = "red" if edge in self.readings else "black"
            color += ":blue" if edge in self.memory_independend else ":black"
            color += ":green" if edge in self.writings else ":black"
            color += ";0.33"
            dot.edge(
                edge[0],
                edge[1],
                label=", ".join([edge[2]] + list(edge[3])),
                penwidth="3.5" if edge in self.deterministic else "2",
                color=color,
            )
        dot.render("graph")
