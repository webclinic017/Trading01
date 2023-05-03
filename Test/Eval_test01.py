# https://proglib.io/p/dinamicheskoe-vypolnenie-vyrazheniy-v-python-funkciya-eval-2020-05-14

'''

Примечание
Для динамического выполнения кода можно также использовать функцию exec().
Основное различие между eval() и exec() состоит в том, что eval() может выполнять лишь выражения,
тогда как функции exec() можно «скормить» любой фрагмент кода Python.
'''

print( eval("2 ** 8"))
print( eval("1024 + 1024"))
print( eval("sum([8, 16, 32])"))
x = 100
print( eval("x * 2"))

print( eval("[it for it in range(10)]"))

code = compile("5 + 4", "<string>", "eval")
print(eval(code))

import math
code = compile("4 / 3 * math.pi * math.pow(25, 3)", "<string>", "eval")
print(eval(code))
