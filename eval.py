#!/usr/bin/python3

import operator as op
import string
import re
import functools
from itertools import product
import decimal
import sys
import readline
import rlcompleter

readline.parse_and_bind("tab: complete")

sys.dont_write_bytecode = True

readline.parse_and_bind("set editing-mode vi")

readline.parse_and_bind("tab: complete")

operands = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
bin_operators = ["&&", "||", "=>", "<=>"]
env = {}
AND = lambda x, y: x and y
OR = lambda x, y: x or y
IFT = lambda x, y: (not x) or y
IFO = lambda x, y: ((not x) or y) and ((not y) or x)
NOT = lambda x: not x
env.update({"&&": AND, "||": OR, "=>": IFT, "<=>": IFO, "~": NOT})


class Stack:
    def __init__(self):
        self.stack = []

    def push(self, x):
        self.stack.append(x)

    def pop(self):
        t = self.stack[-1]
        self.stack.pop()
        return t

    def size(self):
        return len(self.stack)

    def is_empty(self):
        return self.size() == 0

    def __str__(self):
        return str(self.stack)

    def __repr__(self):
        return str(self.stack)

    def peek(self):
        return self.stack[-1]

    def __eq__(self, other):
        return self.stack == other.stack


def tokenize(s):
    s = s.replace("(", " ( ")
    s = s.replace(")", " ) ")
    s = s.replace("=>", " => ")
    s = s.replace("< =>", "<=>")
    s = s.replace("<=>", " <=> ")
    s = s.replace("~", " ~ ")
    s = s.replace("&&", " && ")
    s = s.replace("||", " || ")
    s = s.split()
    s = "".join(e for e in s)
    s = s.replace("~~", "")
    s = s.replace("~~~", "~")
    s = s.replace("(", " ( ")
    s = s.replace(")", " ) ")
    s = s.replace("=>", " => ")
    s = s.replace("< =>", "<=>")
    s = s.replace("<=>", " <=> ")
    s = s.replace("~", " ~ ")
    s = s.replace("&&", " && ")
    s = s.replace("||", " || ")
    s = s.split()
    return s


def parse(s):
    token_list = tokenize(s)
    if not token_list:
        return None
    postfix_list = []  # return tokens
    op_stack = Stack()
    prec = {'~': 6, '&&': 5, '||': 4, '<=>': 3, '=>': 2, '(': 1}
    for token in token_list:
        if token in operands:
            postfix_list.append(token)
        elif token == '(':
            op_stack.push(token)
        elif token == ')':
            top = op_stack.pop()
            while top != '(':
                postfix_list.append(top)
                top = op_stack.pop()
        else:
            while (not op_stack.is_empty()) and (
                    prec[op_stack.peek()] >= prec[token]
            ):
                postfix_list.append(op_stack.pop())
            op_stack.push(token)
    while not op_stack.is_empty():
        postfix_list.append(op_stack.pop())
    return postfix_list


def compute(operand, *opers):
    try:
        res = env[operand](*opers)
        return res
    except ArithmeticError:
        raise ArithmeticError("Arithmetic Error")


def fill(form):
    for i, x in enumerate(form):
        if x in "01":
            form[i] = bool(int(x))
    return form


def fill_values(formula):
    """returns genexp with the all fillings with 0 and 1"""
    letters = "".join(set(re.findall("[A-Za-z]", formula)))
    for digits in product("10", repeat=len(letters)):
        table = str.maketrans(letters, "".join(digits))
        yield formula.translate(table)


def is_tautology(s):
    for x in fill_values(s):
        if not eval(x):
            return False
    return True


def is_sat(s):
    for x in fill_values(s):
        if eval(x):
            return True
    return False


def process(s):
    if is_tautology(s):
        return "Formula is tautology"
    elif is_sat(s):
        return "Formula is satisfiable"
    else:
        return "Formula is not satisfiable"


def eval(s):
    token_list = parse(s)
    stack = Stack()
    for t in token_list:
        if t in operands:
            stack.push(t)
        elif t in bin_operators:
            oper2 = stack.pop()
            oper1 = stack.pop()
            res = compute(t, bool(int(oper1)), bool(int(oper2)))
            stack.push(res)
        elif t == '~':
            oper = stack.pop()
            res = compute(t, bool(int(oper)))
            stack.push(res)
    ret = bool(int(stack.pop()))
    return ret


# formula correctness checks

# test for correct symbols, should be done before
def pre_check(s):
    v = tokenize(s)
    for t in v:
        if t not in bin_operators + ['~', '(', ')'] and not _operand_test(t):
            return False
    return True


def bal_parenthesis(v):
    v = tokenize(v)
    st = Stack()
    for t in v:
        if t == "(":
            st.push(t)
        if t == ")":
            if st.is_empty():
                return False
            else:
                st.pop()
    return st.is_empty()


# is operand check(is name)
def _operand_test(s):
    if s in operands:
        return True
    else:
        return False


# checks what is after operand, cant be paren, negation or operand
def after_letter(v):
    v = tokenize(v)
    lim = len(v)
    for i in range(lim - 1):
        if _operand_test(v[i]):
            if v[i + 1] == "(" or v[i + 1] == "~" or _operand_test(v[i + 1]):
                return False
    return True


def after_left_paren(v):
    v = tokenize(v)
    lim = len(v)
    for i in range(lim - 1):
        if v[i] == '(':
            a = v[i + 1] in operands
            b = v[i + 1] == '('
            c = v[i + 1] == '~'
            if not (a or b or c):
                return False
    return True


def operands_operators_number(v):
    if v == "":
        return True
    v = tokenize(v)
    operands_number = 0
    operators_number = 0
    for t in v:
        if t in operands:
            operands_number += 1
        if t in bin_operators:
            operators_number += 1
    return operands_number == operators_number + 1


def formula_start(v):
    v = v.strip()
    if len(v) == 0:
        return True
    if v[0] in operands or v[0] == '~' or v[0] == '(':
        return True
    else:
        return False


def check(v):
    if not pre_check(v):
        return "Invalid symbols"
    elif not bal_parenthesis(v) or not after_letter(v) or not after_left_paren(v) or not after_letter(v)\
            or not operands_operators_number(v) or not formula_start(v):
        return "Syntax error"
    else:
        return True


message = """Use single lower and upper case letters as operands,
          the only logical operators allowed are:
          ~   - negation;
          ||  - or;
          &&  - and;
          =>  - conditional;
          <=> - biconditional.
          After entering a formula program states if its tautology, satisfiable or not 
          satisfiable. For more info:
          https://github.com/lion137/propositional_calculus_evaluate"""


def repl(prompt="> "):
    while True:
        try:
            v = input(prompt)
            t = check(v)
            if t is not True:
                print(t)
                continue
            v = v.strip()
            if v.startswith("#"):
                continue
            if v == "help" or v == "-h" or v == "/h" or v == "-usage":
                print(message)
                continue
            if v is not None:
                if re.match("^(?![\\s\\S])|(^\\s+)", v):
                    pass
                else:
                    print(process(v))
        except NameError as ex:
            print("NameError:", ex)
        except SyntaxError as ex:
            print("SyntaxError:", ex)


if __name__ == '__main__':
    print("Propositional Logic Parser, press help, /h, -h or -usage for help")
    repl()
