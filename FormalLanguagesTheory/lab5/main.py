from mfa import MFA
from parser import *

import sys

if __name__ == '__main__':
    parsed, config = parse_mfa(sys.argv[1])
    print('PARSED')

    for x in parsed:
        print(x)
    print(config)

    mfa = MFA(parsed, config)
    mfa.create_graph()