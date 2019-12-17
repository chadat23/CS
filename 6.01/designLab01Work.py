#
# File:   designLab01Work.py
# Author: 6.01 Staff
# Date:   02-Sep-11
#
# Below are templates for your answers to three parts of Design Lab 1

# -----------------------------------------------------------------------------

def fib(n):
    if n == 0 or n == 1:
        return n
    return fib(n - 1) + fib(n - 2)


# -----------------------------------------------------------------------------

class V2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'V2[{self.x}, {self.y}]'

    def __add__(self, other):
        return self.add(other)

    def add(self, other):
        return V2(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        return self.mul(other)

    def mul(self, number):
        return V2(self.x * number, self.y * number)


# -----------------------------------------------------------------------------

class Polynomial:
    def __init__(self, terms):
        self.terms = [float(t) for t in terms]

    def __str__(self):
        text = ''
        for i, term in enumerate(self.terms[::-1]):
            if not i:
                text = f'{term:.3f}'
            elif i == 1:
                text = f'{term:.3f} z + {text}'
            else:
                text = f'{term:.3f} z**{i} + {text}'
        return text

    def coeff(self, i):
        return self.terms[i * (-1) - 4]

    def add(self, other):
        if len(self.terms) > len(other.terms):
            longer = self.terms
            shorter = other.terms
        else:
            longer = other.terms
            shorter = self.terms

        terms = []
        for i, term in enumerate(longer[::-1]):
            if i < len(shorter):
                val = shorter[i * (-1) - 1]
            else:
                val = 0
            terms.insert(0, term + val)

        return Polynomial(terms)

    def __add__(self, other):
        return self.add(other)

    def mul(self, other):
        coeffs = {}
        for i, term_s in enumerate(self.terms[::-1]):
            for j, term_o in enumerate(other.terms[::-1]):
                coeffs[i + j] = coeffs.get(i + j, 0) + term_s * term_o

        keys = sorted(coeffs.keys(), reverse=True)
        terms = [coeffs[k] for k in keys]

        return Polynomial(terms)

    def __mul__(self, other):
        return self.mul(other)

    def val(self, v):
        # length = len(self.terms)
        #
        # total = 0
        # for i, term in enumerate(self.terms):
        #     total += term * v**(length - i - 1)
        #
        # return total

        #  Horner’s rule
        def horner(i):
            if not i:
                return self.terms[0]
            return horner(i - 1) * v + self.terms[i]

        return horner(len(self.terms) - 1)

    def __call__(self, x):
        return self.val(x)

    def roots(self):
        terms = self.terms

        if len(terms) > 3:
            return "Error: Order too high to solve for roots."
        elif len(terms) == 2:
            return -terms[1]/terms[0]

        comp = (terms[1]**2 - 4 * terms[0] * terms[2])

        if comp >= 0:
            pos = (-terms[1] + comp**0.5) / (2 * terms[0])
            neg = (-terms[1] - comp**0.5) / (2 * terms[0])
        else:
            pos = complex(-terms[1] / (2 * terms[0]), abs(comp)**0.5 / (2 * terms[0]))
            neg = complex(-terms[1] / (2 * terms[0]), -abs(comp)**0.5 / (2 * terms[0]))

        return [pos, neg]


print(fib(0))
print(fib(6))
print()

a = V2(1.0, 2.0)
b = V2(2.2, 3.3)
print(f'Vectors as strings: a = {a}, b = {b}')
print(f'Vector "a" properties: x = {a.x}, y = {a.y}')
print(f'a.add(b) + b = {a.add(b)}')
print(f'a.add(b).mul(-1) = {a.add(b).mul(-1)}')
print(f'V2(1.1, 2.2) + V2(3.3, 4.4) = {V2(1.1, 2.2) + V2(3.3, 4.4)}')
print()

p1 = Polynomial([1, 2, 3])
print('p1 = Polynomial([1, 2, 3])')
print(f'print(p1) yields: "{p1}"')
p2 = Polynomial([100, 200])
print('p2 = Polynomial([100, 200])')
print(f'print(p2) yields: "{p2}"')
print(f'p1.add(p2) = {p1.add(p2)}')
print(f'p1 + p2 = {p1 + p2}')
print(f'p1(1) = {p1(1)}')
print(f'p1(-1) = {p1(-1)}')
print(f'(p1 + p2)(10) = {(p1 + p2)(10)}')
print(f'p1.mul(p1) = {p1.mul(p1)}')
print(f'p1 * p2 = {p1 * p1}')
print(f'p1 * p2 + p1 = {(p1 * p2) + p1}')
print(f'p1.roots() = {p1.roots()}')
print(f'p2.roots() = {p2.roots()}')
p3 = Polynomial([3, 2, -1])
print('p3 = Polynomial([3, 2, -1]')
print(f'p3.roots() = {p3.roots()}')
print(f'(p1 * p2).roots() = {(p1 * p2).roots()}')
