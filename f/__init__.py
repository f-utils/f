import sys
import os
sys.path.append(os.path.dirname(__file__))
from main import _

_.t(None,       'empty type')
_.t(int,        'integers numbers')
_.t(float,      'float numbers')
_.t(bool,       'booleans')
_.t(range,      'integer ordered sequences')
_.t(str,        'strings')
_.t(tuple,      'static ordered sequences')
_.t(list,       'dynamic ordered sequences')
_.t(frozenset,  'static sequences')
_.t(set,        'dynamic unordered sequences')
_.t(dict,       'key and value sets')
_.t(bytes,      'bytes representation')
_.t(bytearray,  'bytes sequences')
_.t(memoryview, 'memory access')

