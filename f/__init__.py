from f.main import f

f.t.db()

f.t.i(None,       'empty type')
f.t.i(int,        'integers numbers')
f.t.i(float,      'float numbers')
f.t.i(bool,       'booleans')
f.t.i(range,      'integer ordered sequences')
f.t.i(str,        'strings')
f.t.i(tuple,      'static ordered sequences')
f.t.i(list,       'dynamic ordered sequences')
f.t.i(frozenset,  'static sequences')
f.t.i(set,        'dynamic unordered sequences')
f.t.i(dict,       'key and value sets')
f.t.i(bytes,      'bytes representation')
f.t.i(bytearray,  'bytes sequences')
f.t.i(memoryview, 'memory access')

f.s.db()
