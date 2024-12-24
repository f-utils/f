# About

`f` is the Python implementation of `f-utils` [systematics](https://github.com/f-utils/general/blob/main/docs/systematics.md) to ensure constructive type safety. See there for more details.

# Structure

```
f/
|-- __init__.py ........ import main.py
`-- main.py ............ defining the systematics
```

# Usage

The lib `f` defines a namesake class with class-level information:
```
entity      kind          meaning
---------------------------------------------------------------
TYPES       dict          dictionary of accessible types
FUNCS       list          list of all function spectra
type        function      include a type as an acessible type
func        function      initialize a function spetrum
extend      function      extend the function spectrum
update      function      update the function spectrum
spec        function      returns the spectrum of a function
info        function      prints function spectrum in human readable way
```

# Install

```
pip .............. pip install git+https://github.com/f-utils/f 
poetry ........... poetry add git+https://github.com/f-utils/f
uv ............... uv add git+https://github.com/f-utils/f
```
