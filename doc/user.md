# About

In this documentation we describe how to use the Python library [f-utils/f](https://github.com/f-utils/f).

# The Class `f`

The lib `f` defines a namesake class with class-level information:
```
entity      type          meaning
---------------------------------------------------------------
TYPES       dict          dictionary of accessible types
FUNCS       dict          dictionary of all function spectra
---------------------------------------------------------------
init        function      initializes the above dictionaries
type        function      turns a type into an acessible type
func        function      initializes a function spetrum
extend      function      extends the function spectrum
update      function      updates the function spectrum
set         function      attaches the spetrum to a function
spec        function      returns the spectrum of a function
info        function      prints function spectrum in a human readable way
```

The class-level functions come with aliases:

```
function    alias
-----------------------
init        i
type        t
func        f
extend      e
update      u
set         s
spec        S
info        I
```


Following the `f-utils` philosophy, the class `f` should be imported directly, without a namespace:
```python
# use the following
from f import f
# instead of
import f
```

# Basic Flow

With `f` imported, the systematics in essentially described by the following flow: 

```python
# import the class `f`
from f import f

# initialize a spectrum
f.func('my_func', 'function description', my_std_return)
# attach a global variable to the initialized spectrum
my_func = f.set('my_func')
# turn a type into an accessible type
f.type(my_type, 'type description')
# extends the initialized function "my_func" with a return to the accessible type "my_type"
f.extend('my_func', my_type, return_func_my_type)
# eventually update the standard return function of "my_func"
f.update('my_func', 'std')(my_new_std_return)
# eventually update the return function for the "my_type"
f.update('my_func', 'body')(my_type, new_return_func_my_type)
```

# Detailed Description

As described in the [systematics](https://github.com/f-utils/)

# Example

# Custom `TYPES` And `FUNCS`

# The Info Method

# Basic Types

```
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
```
