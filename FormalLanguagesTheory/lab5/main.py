from mfa import MFA
from parser import *

import sys


'''
    Отразил в readme, но т.к. важно:
    Для гарантированного выполнения запускать в терминале
    python main.py 1
    dot -Tsvg graph.dot > graph.svg
'''
if __name__ == '__main__':
    parsed, config = parse_mfa(sys.argv[1])
    print('PARSED')

    for x in parsed:
        print(x)
    print(config)

    mfa = MFA(parsed, config)
    mfa.create_graph()