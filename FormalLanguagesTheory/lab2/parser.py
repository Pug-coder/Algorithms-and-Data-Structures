def parse(file):
    with open(file) as f:
        nontertms_dict = {}
        new = f.read().splitlines()
        for i in new:
            n = i.split()
            nontertms_dict[n[0]] = [elem for elem in n[2] if elem != '|']
    return nontertms_dict

