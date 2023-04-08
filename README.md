# pyutils
## .

### elf

This is a function when when applied on any conventional python function , returns a formulated callable function-object , which when called ,
executes that conventional functions on specified inputs .

Usage :

```python
at_index = lambda l, i: l[i]


def raises(func, exception_cls=None):
    try:
        func()
    except Exception as e:
        if not exception_cls or (exception_cls and isinstance(e, exception_cls)):
            return True
    return False


at_index_delayed: elf = elf(at_index)([1, 2], 9)
assert raises(at_index_delayed, IndexError)
assert raises(at_index_delayed)

```
## pyutils.immutables

### ReadOnlyDictWrapper

This is a dict wrapper , used when you want to convert an already existing dict to a FINAL dict .

Key Points :

- can only add key-value pairs on declaration
- can't delete key-value pairs
- can't modify key-value pairs
- can make a copy of the dict object

Drawbacks :

- allows the value of keys to be mutables( list, dict etc ... )

Usage :

```python
from pyutils.immutables import ReadOnlyDictWrapper

d = ReadOnlyDictWrapper({"a":2,"b":[1,2]})
```

now 'd' will behave as a normal dict , but it's immutable now .


### imdict

This is an alternative to `dict` .

Key Points :

- can only add key-value pairs on declaration
- can't delete key-value pairs
- can't modify key-value pairs
- can make a copy of the dict object

Drawbacks :

- allows the value of keys to be mutables( list, dict etc ... )

Usage :

```python
from pyutils.immutables import imdict

d = imdict(a=2,b=[1,2])
```
