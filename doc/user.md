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

> **Remark.** Following the `f-utils` philosophy, the class `f` should be imported directly, without a namespace:
> ```python
> # use this
> from f import f
> # instead of
> import f
> ```

# Basic Flow

With `f` being imported, the systematics can be applied according to the following flow: 

```python
# import the class `f`
from f import f

# initialize a spectrum
f.func('my_name', 'function description', my_std_return)
# turn a type into an accessible type
f.type(my_type, 'type description')
# extends the initialized function "my_func" with a return to the accessible type "my_type"
f.extend('my_func', my_type, return_func_my_type)
# eventually update the standard return function of "my_func"
f.update('my_func', 'std')(my_new_std_return)
# eventually update the return function for the "my_type"
f.update('my_func', 'body')(my_type, new_return_func_my_type)
```

To use the spectrum one should then attach it to function:

```python
# attach a global variable to the initialized spectrum
my_func = f.set('my_func')
```

# Detailed Description

Let us now describe with more details what is happening in the previous flow. As discussed in the `f-utils` [systematics](https://github.com/f-utils/general/docs/systematics.md), the `f-utils` libs define `f-systems`, whose `state` is defined into two levels:
1. `globally`: provided by the current collection of all accessible types and all accessible spectra on that
2. `locally`: provided by the current content of a given spectrum.

The `global state` of a `f-system` is, therefore, given by the following dictionaries:

- `TYPES`: with the current accessible types
- `FUNCS`: with the current accessible spectra

When one imports the class `f` it comes endowed with the `bare global state`, which is the minimal state of the `f-system`:

- `TYPES`: contains the following `bare accessible types`, which are the basic builtin Python types:
```python
TYPES = {
    None:         "empty type",
    int:          "integers numbers",
    float:        "float numbers",
    bool:         "booleans",
    range:        "integer ordered sequences",
    str:          "character ordered sequences",
    tuple:        "static ordered sequences",
    list:         "dynamic ordered sequences",
    frozenset:    "static unordered sets",
    set:          "dynamic unordered sets",
    dict:         "dynamic key value pair",
    bytes:        "bytes representation",
    bytearray:    "bytes ordered sequences",
    memoryview:   "memory access"
}
```
- `FUNCS`: the empty dictionary, meaning that there is no `bare accessible spectra` in a `f-system`.

After importing the class `f`, one can modify the `global state` of the `f-system` by initializing a function spectrum in it:

```python
f.func(
    'some_spectrum_name',
    'spectrum description',
    lambda *args, **kwargs: 'Some standard message.'
)
```

Above, the `lambda` function defines the `standard return` of the spectrum. Of course, it can be any previously defined function, not necessarily a `lambda` function. For instance, one could defined:

```python
def whatever(*args, **kwargs):
    # do whatever you want

f.func(
    'some_spectrum_name',
    'spectrum description',
    whatever
)
```

# Example

# Custom `TYPES` And `FUNCS`

# The Info Method

