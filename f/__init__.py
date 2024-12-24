import sys
import os
sys.path.append(os.path.dirname(__file__))
from main import f

import json
#print(f.TYPES)
#print(f.FUNCS)

f.t(int,        'integers numbers')
f.f('test', 'funcao teste', lambda *args, **kwargs: 'Mensagem de erro padrão')
f.e('test', int, lambda x: x+1)
f.e('test', (int, str), lambda x, y: str(x)+y)

f.i('test')
f.u('test', 'std')(lambda *args, **kwargs: 'Nova mensagem de erro')
test = f.set('test')
print(test(1))

f.u('test', 'body')(int, lambda x: x+2)
print(test(1))
#print(f.FUNCS)
#print(f.TYPES)

# f.t(None,       'empty type')

# f.t(float,      'float numbers')
# f.t(bool,       'booleans')
# f.t(range,      'integer ordered sequences')
# f.t(str,        'strings')
# f.t(tuple,      'static ordered sequences')
# f.t(list,       'dynamic ordered sequences')
# f.t(frozenset,  'static sequences')
# f.t(set,        'dynamic unordered sequences')
# f.t(dict,       'key and value sets')
# f.t(bytes,      'bytes representation')
# f.t(bytearray,  'bytes sequences')
# f.t(memoryview, 'memory access')

