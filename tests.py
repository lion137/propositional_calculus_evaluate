#
# Tests file
#

from eval import *
import pytest


def test_eval():
    assert process("a && (a =>b) => b") == "Formula is tautology"
    assert process("(P || (Q || R)) <=>((P || Q) || R)") == "Formula is tautology"
    assert process("~(Q && P) <=> (~P || ~Q)") == "Formula is tautology"
    assert process("((P => Q) && (Q => R)) => (P => R)") == "Formula is tautology"
    assert process("~(Q && P) <=> (~P || Z)") == "Formula is satisfiable"
    assert process("P && Q") == "Formula is satisfiable"


def test_bal_parenthesis1():
    assert bal_parenthesis("()") is True
    assert bal_parenthesis("(()") is False
    assert bal_parenthesis("())") is False


def test_after_letter():
    assert after_letter("(A => ~B)") is True
    assert after_letter("(A => B~)") is False
    assert after_letter("(A(B) => B)") is False
    assert after_letter("()") is True


def test_after_left_paren():
    assert after_left_paren("(A || B") is True
    assert after_left_paren("(~A || B") is True
    assert after_left_paren("((A) || B") is True
    assert after_left_paren("(=> ~A") is False


def test_operands_operators_number():
    assert operands_operators_number("") is True
    assert operands_operators_number("A => A ~") is True
    assert operands_operators_number("A => A => ~A => ") is False


def test_formula_start():
    assert formula_start("") is True
    assert formula_start("( )(") is True
    assert formula_start("=>") is False
    assert formula_start("~=>sss") is True
    assert formula_start("a~~a~") is True


def test_check():
    assert check("") is True
    assert check("~(A)") is True
    assert check("~)") == "Syntax error"
    assert check("(AA => AA") == "Invalid symbols"
    assert check("(A => ") == "Syntax error"
    assert check("A => A)") == "Syntax error"
    assert check("~A => ~") == "Syntax error"



