#
# Tests file
#

from eval import *

assert process("a && (a =>b) => b") == "Formula is tautology"  # tautology modus ponens
assert process("b&&~ b") == "Formula is not satisfiable"
assert process("(P || (Q || R)) <=>((P || Q) || R)") == "Formula is tautology"
assert process("~(Q && P) <=> (~P || ~Q)") == "Formula is tautology"
assert process("((P => Q) && (Q => R)) => (P => R)") == "Formula is tautology"
assert process("~(Q && P) <=> (~P || Z)") == "Formula is satisfiable"
assert process("P && Q") == "Formula is satisfiable"





