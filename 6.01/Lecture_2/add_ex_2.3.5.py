def slow_mod(a, b):
    if a < b:
        return a
    return slow_mod(a - b, b)

a, b = 5, 2
print(f'slowmod({a}, {b}) = {slow_mod(a, b)}')
a, b = 6, 2
print(f'slowmod({a}, {b}) = {slow_mod(a, b)}')
a, b = 8, 3
print(f'slowmod({a}, {b}) = {slow_mod(a, b)}')
a, b = 4, 6
print(f'slowmod({a}, {b}) = {slow_mod(a, b)}')
