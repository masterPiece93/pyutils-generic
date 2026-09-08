import collections
import copy

__all__ = [
    'ReadOnlyDictWrapper',
    'imdict',
    'ReadOnlyMeta'
]

class ReadOnlyDictWrapper(collections.abc.Mapping):
    """Wraps a dict
    Provides Read-Only Functionalities
    """

    def __init__(self, data: dict):
        if not isinstance(data, dict):
            raise Exception(f"{dict} expected . Got {type(data)}")
        self._data = copy.deepcopy(data)

    def __getitem__(self, key):
        return self._data[key]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def __str__(self):
        return str(self._data)


class imdict(dict):
    """Dict implementation.
    Blocks Mutable Operations
    """

    def __hash__(self):
        return id(self)

    def _immutable(self, *args, **kws):
        raise TypeError("object is immutable")

    __setitem__ = _immutable
    __delitem__ = _immutable
    clear = _immutable
    update = _immutable
    setdefault = _immutable
    pop = _immutable
    popitem = _immutable


class ReadOnlyMeta:
    """
    Abstract Base for ReadOnly Classes

    Prohibits the modification of class
        varibales .
    
    Usage:
        class Xyz(metaclass=ReadOnlyMeta):
            ...
    """
    def __setattr__(cls, name, value):
        if name in cls.__dict__:
            raise AttributeError(f"Cannot modify constant '{name}' on ReadOnly Class {cls.__qualname__}")
        super().__setattr__(name, value)
