# pyutils

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
d = imdict(a=2,b=[1,2])
```
