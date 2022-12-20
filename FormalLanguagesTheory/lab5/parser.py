from pprint import pprint
import io
import re

config = {
    "arrow": "->_def",
    "final_flag": "is_final_def",
    "init_flag": "is_initial_def",
    "close_flag": "c_def",
    "keep_flag": "k_def",
    "open_flag": "o_def",
    "eps": "eps_def",
    "any": "any_def",
}


def parse_config(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    for line in lines:
        line = "".join(filter(lambda x: not x.isspace(), line))
        if not line:
            continue
        key, value = line.split("=")
        assert key in config
        assert value != ""
        assert ";" not in value
        config[key] = value

    assert not config["final_flag"].startswith("label=")
    assert not config["init_flag"].startswith("label=")


def parse_mfa(filename):
    with open(filename, "r") as f:
        raw = f.read()
    raw = "".join(list(filter(lambda x: x != "\n", raw)))
    raw = raw.split(";")
    raw = list(filter(bool, raw))
    declarations = list(map(lambda x: x.strip(), raw))

    return [parse_declaration(declaration) for declaration in declarations]


def parse_declaration(declaration):
    id1 = re.search(r"[^\s]+", declaration)[0]
    assert id1
    declaration = declaration[len(id1) :]
    declaration = declaration.strip()
    if declaration.startswith(config["arrow"]):
        declaration = declaration[len(config["arrow"]) :]
        declaration = declaration.strip()

        id2 = re.search(r"[^\s]+", declaration)[0]
        assert id2
        declaration = declaration[len(id2) :]
        declaration = declaration.strip()

        symbol = re.search(r"[^\s]+", declaration)[0]
        if symbol == config["eps"]:
            symbol = "eps"
        elif symbol == config["any"]:
            symbol = "any"
        assert (
            len(symbol) == 1
            or symbol == config["eps"]
            or symbol == any
            or symbol.isdigit
        )
        declaration = declaration[len(symbol) :]
        declaration = declaration.strip()

        memory_flags = []
        while declaration:
            flag = re.search(r"[^\s]+", declaration)[0]
            assert flag
            if flag == config["close_flag"]:
                memory_flags.append("c")
            elif flag == config["open_flag"]:
                memory_flags.append("o")
            elif flag == config["keep_flag"]:
                memory_flags.append("◊")
            else:
                raise Exception("unknown flag")
            declaration = declaration[len(flag) :]
            declaration = declaration.strip()

        return (
            "edge",
            {"from": id1, "to": id2, "symbol": symbol, "memory": memory_flags},
        )

    else:

        node_flags = []
        label = None
        while declaration:
            if declaration.startswith("label="):
                if label is not None:
                    raise Exception("нельзя определять node_label дважды")
                label_declaration = re.search(r"label=\"(.*)\"", declaration)
                if not label_declaration:
                    raise Exception(
                        f"вы явно что-то напутали в объявении узла {declaration}"
                    )
                label = label_declaration.groups()[0]
                declaration = declaration[len(label_declaration[0]) :]
                declaration = declaration.strip()
            else:
                flag = re.search(r"[^\s]+", declaration)[0]
                assert flag
                if flag == config["init_flag"]:
                    node_flags.append("init_flag")
                elif flag == config["final_flag"]:
                    node_flags.append("final_flag")
                else:
                    raise Exception("unknown flag")

                declaration = declaration[len(flag) :]
                declaration = declaration.strip()

        return ("node", {"id": id1, "label": label, "flags": node_flags})


parse_config("config.txt")
