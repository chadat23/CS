import pdb
# import lib601.sm as sm
from copy import deepcopy

from state_machine import SM
import string
import operator

add_op = operator.add
sub_op = operator.sub
mul_op = operator.mul
div_op = operator.truediv


class BinaryOp:

    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.op = self.math_op

    def __str__(self):
        return self.opStr + '(' + \
               str(self.left) + ', ' + \
               str(self.right) + ')'

    def eval(self, env):

        op = deepcopy(self)
        e = deepcopy(env)

        if isinstance(op.left, BinaryOp) or isinstance(op.left, Number) or op.left.name in e:
            left = op.left.eval(e)
        else:
            left = op.left

        if isinstance(op.right, BinaryOp) or isinstance(op.right, Number) or op.right.name in e:
            right = op.right.eval(e)
        else:
            right = op.right

        if isinstance(left, float) and isinstance(right, float):
            return op.op(left, right)
        op.left = left
        op.right = right

        return op

    __repr__ = __str__


class Sum(BinaryOp):
    opStr = 'Sum'

    math_op = add_op


class Prod(BinaryOp):
    opStr = 'Prod'

    math_op = mul_op


class Quot(BinaryOp):
    opStr = 'Quot'

    math_op = div_op


class Diff(BinaryOp):
    opStr = 'Diff'

    math_op = sub_op


class Assign(BinaryOp):
    opStr = 'Assign'
    math_op = None

    def eval(self, env):
        env[self.left.name] = self.right


class Number:
    def __init__(self, val):
        self.value = val

    def __str__(self):
        return 'Num(' + str(self.value) + ')'

    def eval(self, env):
        return self.value

    __repr__ = __str__


class Variable:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Var(' + self.name + ')'

    def eval(self, env):
        var = env.get(self.name)
        if var:
            if not isinstance(var, Variable):
                return var.eval(env)
            return var
        return self.name

    __repr__ = __str__


# characters that are single-character tokens
seps = ['(', ')', '+', '-', '*', '/', '=']


# Convert strings into a list of tokens (strings)
def tokenize(text):
    def tokenize_helper(text, i, j):
        if text[i] == ' ':
            # a space was hit and should be skipped
            return j, None
        if text[i] in seps:
            # a special char was hit, should be noted and moved on from
            return j, text[i]
        if j == len(text):
            # the end of the text was hit, whatever's mid works is the last token
            return j, text[i: j]
        if text[j] not in seps and text[j] != ' ':
            # the next token char should be accounted for
            return tokenize_helper(text, i, j + 1)
        # the end of a token has been hit
        return j, text[i: j]

    tokens = []
    index = 0
    while index < len(text):
        index, val = tokenize_helper(text, index, index + 1)
        if val:
            tokens.append(val)

    return tokens


# tokens is a list of tokens
# returns a syntax tree:  an instance of {\tt Number}, {\tt Variable},
# or one of the subclasses of {\tt BinaryOp} 
def parse(tokens):
    def parseExp(index):
        left_tree = tokens[index]
        index += 1
        if left_tree == '(':
            left_tree, index = parseExp(index)
        if numberTok(left_tree):
            return Number(float(left_tree)), index
        if variableTok(left_tree):
            return Variable(left_tree), index
        while tokens[index] == ')':
            if index < len(tokens) - 1:
                index += 1
        op = tokens[index]
        index += 1
        right_tree, index = parseExp(index)
        if op == '+':
            return Sum(left_tree, right_tree), index
        if op == '-':
            return Diff(left_tree, right_tree), index
        if op == '*':
            return Prod(left_tree, right_tree), index
        if op == '/':
            return Quot(left_tree, right_tree), index
        if op == '=':
            return Assign(left_tree, right_tree), index

    (parsedExp, nextIndex) = parseExp(0)
    return parsedExp


# token is a string
# returns True if contains only digits
def numberTok(token):
    if not hasattr(token, '__iter__'):
        return False
    for char in token:
        if char not in string.digits:
            return False
    return True


# token is a string
# returns True its first character is a letter
def variableTok(token):
    if not hasattr(token, '__iter__'):
        return False
    for char in token:
        if char in string.ascii_letters:
            return True
    return False


# thing is any Python entity
# returns True if it is a number
def isNum(thing):
    return type(thing) == int or type(thing) == float


# Run calculator interactively
def calc():
    env = {}
    while True:
        e = input('%')  # prints %, returns user input
        print('%', parse(tokenize(e)).eval(env))  # your expression here
        print('   env ='), env


# exprs is a list of strings
# runs calculator on those strings, in sequence, using the same environment
def calcTest(exprs):
    env = {}
    for e in exprs:
        print('%', e)  # e is the experession
        print(parse(tokenize(e)).eval(env))  # your expression here
        print('   env =', env)


# Simple tokenizer tests
'''Answers are:
['fred']
['777']
['777', 'hi', '33']
['*', '*', '-', ')', '(']
['(', 'hi', '*', 'ho', ')']
['(', 'fred', '+', 'george', ')']
['(', 'hi', '*', 'ho', ')']
['(', 'fred', '+', 'george', ')']
'''


def testTokenize():
    print(tokenize('fred '))
    print(tokenize('777 '))
    print(tokenize('777 hi 33 '))
    print(tokenize('**-)('))
    print(tokenize('( hi * ho )'))
    print(tokenize('(fred + george)'))
    print(tokenize('(hi*ho)'))
    print(tokenize('( fred+george )'))


# Simple parsing tests from the handout
'''Answers are:
Var(a)
Num(888.0)
Sum(Var(fred), Var(george))
Quot(Prod(Var(a), Var(b)), Diff(Var(cee), Var(doh)))
Quot(Prod(Var(a), Var(b)), Diff(Var(cee), Var(doh)))
Assign(Var(a), Prod(Num(3.0), Num(5.0)))
'''


def testParse():
    print(parse(['a']))
    print(parse(['888']))
    print(parse(['(', 'fred', '+', 'george', ')']))
    print(parse(['(', '(', 'a', '*', 'b', ')', '/', '(', 'cee', '-', 'doh', ')', ')']))
    print(parse(tokenize('((a * b) / (cee - doh))')))
    print(parse(tokenize('(a = (3 * 5))')))


####################################################################
# Test cases for EAGER evaluator
####################################################################

def testEval():
    env = {}
    Assign(Variable('a'), Number(5.0)).eval(env)
    print(Variable('a').eval(env))
    env['b'] = 2.0
    print(Variable('b').eval(env))
    env['c'] = 4.0
    print(Variable('c').eval(env))
    print(Sum(Variable('a'), Variable('b')).eval(env))
    print(Sum(Diff(Variable('a'), Variable('c')), Variable('b')).eval(env))
    Assign(Variable('a'), Sum(Variable('a'), Variable('b'))).eval(env)
    print(Variable('a').eval(env))
    print(env)


# Basic calculator test cases (see handout)
testExprs = ['(2 + 5)',
             '(z = 6)',
             'z',
             '(w = (z + 1))',
             'w'
             ]


# calcTest(testExprs)

class Tokenizer(SM):
    startState = ''

    def getNextValues(self, state, inp):
        if inp == " " or inp in seps or \
                ((state in seps or state == ' ') and (inp in string.ascii_letters or inp in string.digits)):
            return inp, state
        return state + inp, ''


def test_Tokenizer():
    print(Tokenizer().transduce('fred '))
    print(Tokenizer().transduce('777 '))
    print(Tokenizer().transduce('777 hi 33 '))
    print(Tokenizer().transduce('**-)( '))
    print(Tokenizer().transduce('(hi*ho) '))
    print(Tokenizer().transduce('(fred + george) '))


def tokenize(inputString):
    return [c for c in Tokenizer().transduce(inputString + ' ') if c != '' and c != ' ']


def test_tokenize():
    print(tokenize('fred'))
    print(tokenize('777'))
    print(tokenize('777 hi 33'))
    print(tokenize('**-)('))
    print(tokenize('(hi*ho)'))
    print(tokenize('(fred + george) '))


####################################################################
# Test cases for LAZY evaluator
####################################################################

# Simple lazy eval test cases from handout
'''Answers are:
Sum(Var(b), Var(c))
Sum(2.0, Var(c))
6.0
'''


def testLazyEval():
    env = {}
    Assign(Variable('a'), Sum(Variable('b'), Variable('c'))).eval(env)
    print(Variable('a').eval(env))
    env['b'] = Number(2.0)
    print(Variable('a').eval(env))
    env['c'] = Number(4.0)
    print(Variable('a').eval(env))


# Lazy partial eval test cases (see handout)
lazyTestExprs = ['(a = (b + c))',
                 '(b = ((d * e) / 2))',
                 'a',
                 '(d = 6)',
                 '(e = 5)',
                 'a',
                 '(c = 9)',
                 'a',
                 '(d = 2)',
                 'a']
# calcTest(lazyTestExprs)

## More test cases (see handout)
partialTestExprs = ['(z = (y + w))',
                    'z',
                    '(y = 2)',
                    'z',
                    '(w = 4)',
                    'z',
                    '(w = 100)',
                    'z']

calcTest(partialTestExprs)
