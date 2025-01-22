# About

`f` is the Python implementation of `f-utils` systematics to ensure constructive type safety by means of parametric polymorphisms.

# Structure

```
f/
|-- __init__.py ........ import main.py and define basics TYPES
`-- main.py ............ define the systematics
```

# Dependencies

The project has no internal dependencies. The only external dependency is `python3`. 
> Recommended `python >=v3.12`.

# Install

The installation is from this git repository under some of the following branches:
1. `main`: the current stable version
2. `dev`: some working in progress

With `git`:
```bash
# main branch
git clone https://github.com/f-utils/f /path/to/your/venv/lib/python3/site-packages/f
# dev branch
git clone https://github.com/f-utils/f/tree/dev /path/to/your/venv/lib/python3/site-packages/f
```

With `pip`:
```bash
# main branch
pip install git+https://github.com/f-utils/f
# dev branch
pip install git+https://github.com/f-utils/f/tree/dev
```

With [uv](https://github.com/astral-sh/uv):
```bash
# main branch
uv add git+https://github.com/f-utils/f
# dev branch
uv add git+https://github.com/f-utils/f --branch dev
```

With [py](https://github.com/ximenesyuri/py):
```bash
# main branch
py add f-utils/f --from github
# dev branch 
py add f-utils/f:dev --from github
```

# Usage

Just import the class `f`:

```python
from f import f
```

For more details, see:
- [user](./doc/user.md): user manual
- [ref](./doc/ref.md): reference manual

See also:
- [philosophy](https://github.com/f-utils/general/blob/main/docs/philosophy.md)): with `f-utils` philosophy
- [systematics](https://github.com/f-utils/general/blob/main/docs/systematics.md): with an exposition on `f-utils` systematics
