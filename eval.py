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
