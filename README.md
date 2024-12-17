# About

`f` is the Python implementation of a strategy that allows constructive type safety through a specific "systematics", as described [below](#systematics). There are no dependencies.

> The same strategy could be easily implemented in any dynamically typed functional programming language which admits class-level entities, as Javascript and Ruby.

# Systematics

In `safe`, functions have a `spectrum`, which consists of all current function information, generalizing its Python `signature`. By definition, the function is created when one *initialize* its `spectrum`, which can be *extended* or *updated* in any posterior moment. 

## Structural Functions

The definition and manipulation of the `spectrum` involves the following *structural functions*.

```
structural functions
------------------------
name            scope
----------------------------------------------------------------
func            creates a function by initializing its spectrum
extend          extends the spectrum of a function
update          updates the spectrum of a function
spec            gets the function spectrum
```

One can think of the `spectrum` as the "state" of a function, which is defined by:
1. the acceptable variable types (which define the function `domain`)
2. the functions which are returned for each acceptable variable type (defining the function `body`).

If called with variables of acceptable types (i.e, in its `domain`), the corresponding returning function is returned. Else, it returns its *standard return*.

The function is *initialized* with an "empty state", which means that:
1. it has a characterizing string (its `name`)
2. it has no acceptable variable types (i.e, it has an empty `domain`)
3. it has been defined its "standard return" (denoted by `std`)

To *extend* a function means therefore to extend its "state" by adding:
1. a new acceptable type to its `domain`;
2. a corresponding returning function to its `body`.

Similarly, to *update* a function means to update its "state" by updating:
1. its standard return `std`
2. or the returning function of an acceptable type in the `domain`.

So, in essence, the function `spectrum` is a tuple consisting of the following components:

```
spetrum components
----------------------
component     type        description
---------------------------------------------------------------------
name          str         the function name 
std           function    the standard return function     
domain        list        the accessible types
body          dict        the returning functions of the domain types
```

## The Class `_`

The `safe` lib actually provides a class `_` of which the above structural functions occurs as class methods. Since `safe` is to be used in constructionist approaches, the idea is to think of `_` as a primitive class, so that it would be included outside a namespace:

```python
# use the following
from safe import _
# instead of 
import safe
```
The structural functions could then be called as

```python
_.func('my_function', std_return)
_.extend(my_function, new_type, new_return)
_.update(my_function, existing_type, new_return)
_.spec(my_funcion)
```

There are also available aliases:
```
aliases
-------------
function        alias
-------------------------
func            f
extend          e
update          u
spec            s
```

## Global State

After initialized, functions spectra are stored in a list called `FUNCS`. On the other hand, by construction, each function spectrum inside `FUNCS` returns a different function for each *acceptable type* in its `domain`. Together with `FUNCS`, the class `_` also provides a dictionary `TYPES` containing entries in the form `{some_type: ' description'}`. A type can be added to the domain of a function in `FUNCS` (i.e, a type can be an acceptable type) only it is a key in `TYPES`. The elements of `TYPES` are the *accessible types*.

Therefore, `TYPES` and `FUNCS` provides all "acceptable entities", which means that they define the "global functional state" of a constructive system using `safe`. 

> One should notice that, since `FUNCS` is a class member, its value is shared by any module in the project that imports the class `_`.

## Accessible Types

By default, the `safe` library provides the following accessible types:

```
...
```

You can add new types to the dictionary `TYPES` using the `_.type` structural function.

```
to continue...
```

