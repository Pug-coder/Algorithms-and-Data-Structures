from mfa import MFA
from parser import *

if __name__ == '__main__':
    parsed = parse_mfa('automata.mfa')
    print('PARSED')
    for x in parsed:
        print(x)

    mfa = MFA(parsed)
    mfa.create_graph()