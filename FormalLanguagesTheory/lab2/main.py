from parser import CFG_Parser
import sys

parser_obj = CFG_Parser('tests/test1.txt')
grammar = parser_obj.parse_rules()

g2 = grammar.lab_pipelene()
print(g2)
