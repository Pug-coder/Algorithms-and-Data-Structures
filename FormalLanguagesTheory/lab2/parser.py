def parse(file):
    with open(file) as f:
        nontertms_dict = {}
        rules_dict = {}
        new = f.read().splitlines()
        for i in new:
            n = i.split()
            nontertms_dict[n[0]] = [elem for elem in n[2] if elem != '|']
        for i in new:
            n = i.split()
            rules_dict[n[0]] = n[2].split('|')
    return nontertms_dict, rules_dict
