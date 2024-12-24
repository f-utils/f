import sys
import os
sys.path.append(os.path.dirname(__file__))
from main import f

f.t(None,       'empty type')
f.t(int,        'integers numbers')
f.t(float,      'float numbers')
f.t(bool,       'booleans')
f.t(range,      'integer ordered sequences')
f.t(str,        'strings')
f.t(tuple,      'static ordered sequences')
f.t(list,       'dynamic ordered sequences')
f.t(frozenset,  'static sequences')
f.t(set,        'dynamic unordered sequences')
f.t(dict,       'key and value sets')
f.t(bytes,      'bytes representation')
f.t(bytearray,  'bytes sequences')
f.t(memoryview, 'memory access')

