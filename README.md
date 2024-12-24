# About

`f` is the Python implementation of `f-utils` [systematics](https://github.com/f-utils/general/blob/main/docs/systematics.md) to ensure constructive type safety.

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

Directly from this git repository with some of these branches:
1. `main`: the current stable version
2. `dev`: some working in progress

With `pip`:
```bash
# main branch
pip install git+https://github.com/f-utils/f
# dev branch
pip install git+https://github.com/f-utils/f/tree/dev
```

With `uv`:
```bash
# main branch
uv add git+https://github.com/f-utils/f
# dev branch
uv add git+https://github.com/f-utils/f --branch dev
```

# Usage

See:
- [user](./doc/user.md): with the user manual
- [ref](./doc/ref.md): with the reference manual

See also:
- [philosophy](https://github.com/f-utils/general/blob/main/docs/systematics.md)): with `f-utils` philosophy
- [systematics](https://github.com/f-utils/general/blob/main/docs/systematics.md): with an exposition on the systematics

