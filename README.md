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

Idea :

```python
def sum(a: int, b: int):
    return "{0} + {1} = {2}".format(a, b, a + b)


inputs = (
    (1, 2),
    (7, 9),
    (22, 33),
    (10, 100),
)
f_code = elf(sum)

f_code_register: dict = {}

for i, args in enumerate(inputs):
    f_code_register[i] = f_code(*args)

print(f_code_register)

print("\n`sum` on input 2:\n\t", f_code_register[2]())

# we kept stored the execution information - (...code(...arguments)) in a function-object
# and we executed it as when needed , without the need of passing arguments

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

## pyutils.printing

### cprint

This is an alternative to python-native print function , for printing coloured outputs on console/stdout .

Drawbacks :

- only allows some limited (yet standars) colors .
- converts entire output in one color ( which is obvious as it's made though ) .
- does'nt allow bold with colors .
- not much extra options .

Usage :

```python
from pyutils.printing import cprint

cprint("hello","I am Blue").blue()
cprint("This is a heading \n\n").header()
cprint("This is a heading \n\n").bold()
```

All color extention functions :-

- `.header()`
- `.blue()`
- `.cyan()`
- `.green()`
- `.warning()`
- `.fail()`
- `.bold()`
- `.underline()`

## pyutils.typecheck

### @strict

This is an argument checking decorator . It's sole purpose is to check typehints in function arguments .

Drawbacks :

-

Usage :

```python
from pyutils.typecheck import strict


@strict
def sum(a: int, b: int) -> int:
    return a+b

print(sum(1,3.8)) # <- will raise ArgumentTypeError

```

### TypeCheck

This is a base class for defining a Schema dataclass .

Usage :

```python
from pyutils.printing import cprint
from pyutils.typecheck import TypeCheck, strict
import dataclasses

@dataclasses.dataclass(frozen=True)
class User(TypeCheck):
    name: str
    age: int
    contacts: tuple = (...,)

    # Field Validators :
    name_validator = lambda value: value.islower()
    contacts_validator = lambda value: all([v.isdigit() and len(v) == 10 for v in value])
    
    # User Defined Methods :
    def max_contacts_validation(self) -> None:
        if len(self.contacts) > 3:
            raise ValueError('user contact must have 10 digits')

@strict
def print_user_info(user: list):
    validated_user = User(*user)
    validated_user.max_contacts_validation() # a custom validation
    cprint(f"""
        User : {validated_user.name} ( {validated_user.age} )
        Contacts : {",".join([f'*{a_contact}' for a_contact in validated_user.contacts])}
        validated_user
    """).bold()
    
```

Field Validator : `<field_name>._validator = callable -> bool`


### CoercedType

This is a Base Class for defining a custom type object that have coercion rules specified with it .

Usage :

```python

from pyutils.typecheck import TypeCheck, strict, CoercedType

@dataclass(frozen=True)
class Age(CoercedType):
    value: int
    coercion: dict = field(
        default_factory=lambda: {
            int: int,
            float: int,
            dict: lambda value: int(value["age"]),
            str: int
        }
    )
@dataclass(frozen=True)
class User(TypeCheck):
    name: str
    age: Age
    contacts: tuple = (...,)

    # Field Validators :
    name_validator = lambda value: value.islower()
    contacts_validator = lambda value: all([v.isdigit() and len(v) == 10 for v in value])
    
    # User Defined Methods :
    def max_contacts_validation(self) -> None:
        if len(self.contacts) > 3:
            raise ValueError('user contact must have 10 digits')

@strict
def print_user_info(user: list):
    validated_user = User(*user)
    validated_user.max_contacts_validation() # a custom validation
    cprint(f"""
        User : {validated_user.name} ( {validated_user.age.value} )
        Contacts : {",".join([f'*{a_contact}' for a_contact in validated_user.contacts])}
        validated_user
    """).bold()

print_user_info(["ankit",Age('89'),('9871241665',)])
```

