# pyutils

<details>  
  <summary><b>Installation</b></summary>    

### Methods of Installing Python Package directly from Git
###### NOTE : you will be installing directly from GITHUB

###### Table of Contents  
[Installation Method 1](#method-1--with-symbolic-linking---e-)  

[Installation Method 2](#method-2--direct-url)

[Installation Method 3](#method-3--direct-url-with-tag-specification)


#### Method 1 : with symbolic linking ( -e )

- within requirements file :
    ```txt
    # requirements.txt
    -e git+https://github.com/masterPiece93/pyutils.git#egg=pyutils
    ```

    ```sh
    pip install -r requirements.txt
    ```

- direct
    ```sh
    pip install -e git+https://github.com/masterPiece93/pyutils.git#egg=pyutils
    ```

output of pip-freeze command :
```
-e git+https://github.com/masterPiece93/pyutils.git@7c8a56f4040e578b1dc3059a9cef321bca192cf8#egg=google_drive_examples
```

this value `7c8a56f4040e578b1dc3059a9cef321bca192cf8` in the above pip-freeze output , is the latest commit hash of the repository .

> Note : if you are mentioning `-e` , it is mandatory to attach `#egg=<your-pkg-name>` in the url .

[Usefulness of symbolic link](#benefits-of-using-symbolic-link)


#### Method 2 : direct url

- within requirements file :
    ```txt
    # requirements.txt
    git+https://github.com/masterPiece93/pyutils.git
    ```

    ```sh
    pip install -r requirements.txt
    ```

- direct
    ```sh
    pip install git+https://github.com/masterPiece93/pyutils.git
    ```

output of freeze command :
```
pyutils==1.0.0
```


#### Method 3 : direct url with Tag Specification

- within requirements file :
    ```txt
    # requirements.txt
    git+https://github.com/masterPiece93/pyutils.git@v1.0.0
    ```

    ```sh
    pip install -r requirements.txt
    ```

- direct
    ```sh
    pip install git+https://github.com/masterPiece93/pyutils.git@v1.0.0
    ```

output of freeze command :
```
pyutils==1.0.0
```

---
</details>

---

## Library Usage 

## .

### elf

This is a function when when applied on any conventional python function , returns a formulated callable function-object , which when called ,
executes that conventional functions on specified inputs .

Usage :

```python
from pyutils import elf

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

- Defining a schema made easy with `TypeCheck` .
- It just a simple python dataclass . your dataclass will simply inherit `TypeCheck` class to make it a schema .
- The annotations mentioned on the dataclass will be typechecked .
- you can even write validators for each dataclass field you have mentioned .

Usage :

- **How to specify Field**
  
  Field : `<field_name>:<type>`
  > NOTE : it is just like a simple python `dataclass`

- **How to specify Field Validator** :

  Field Validator : `<field_name>._validator = callable -> bool`

```python

# A basic example of sample usage

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

1.
```python
"""
Custom Exception Handling Feature
=================================

you can define custom exception classes of your own , which
when specified withing the schema classes , will be automatically
used as callbacks to transfer ( raise Exception ) details about error to you .

- Feature Specifications
  you are provided with two class variables , namely :
    - validator_exception
    - type_exception
  both accept only two type of values :
    - :Callable
    - :Exception subclasses
  As both of these are used as callbacks , upon being called,
  the object/function recieves *args , which are the details of error

  Callback Args
    - validator_exception
      - name: str | field name on which the validation was applied
      - value: Any | the value that was passed for that field
      - validation_name: str | name of the validation, as registered in the schema
    - type_exception
      - name: str | field name on which the validation was applied
      - current_type: type | the actual type of the value that is passed
      - expected_type: type | the type that was specified for this field on the schema

- How to Use Feature

  # Method 1
  @dataclasses.dataclass(frozen=True)
  class YourSchema(TypeCheck):
    # Fields
    ...
    # Validations
    ...

    # Exception
    validator_exception = ValidationExceptionCls
    type_exception = TypeExceptionCls

    ...

  # Method 2
  @dataclasses.dataclass(frozen=True)
  class YourSchema(TypeCheck):
    # Fields
    ...
    # Validations
    ...

    # Exception
    validator_exception = validation_exception_callback_fn
    type_exception = type_exception_callback_fn

    ...
"""

# Demonstrating Method 1

# A Custom Exception cls for Handling Validations
class ValidationFailed(Exception):

    def __init__(self, name, value, validation_name):
        self.name = name
        self.value = value
        self.validation_name = validation_name

    __str__ = lambda self: f"Invalid value for field - `{self.name}`"

# A Custom Exception cls for Handling Type Errors
class TypeCheckFailed(Exception):

    def __init__(self, name, current_type, expected_type):
        self.name = name
        self.current_type = current_type
        self.expected_type = expected_type

    __str__ = lambda self: f"Invalid Type for field - `{self.name}`, expected - `{self.expected_type}`, but got - `{self.current_type}`"

@dataclass(frozen=True)
class RequestBodySchema(TypeCheck):

    username: str
    firstname: str
    lastname: str
    email: str
    created_by: int
    age : Optional[int] = None

    # Constants
    MAX_AGE = 25
    
    # Field Validators
    username_validator = lambda value: value.islower()
    firstname_validator = lastname_validator = lambda value: ' ' not in value
    age_validator = lambda value: value < RequestBodySchema.MAX_AGE if value else True

    # Exceptions
    validator_exception = ValidationFailed
    type_exception = TypeCheckFailed

# Driver Code
if __name__ == '__main__':
    # Place where you'll validate your data against the schema :

    try:
        data = {
            "username": "anki8290",
            "firstname": "ankit",
            "lastname": "kumar",
            "email": "ankit8290@gmail.com",
            "created_by": 7,
            "age": 24
        }

        validated_data = RequestBodySchema(**data)
    except ValidationFailed as e: # < exception cls that your registered with schema
        print(e.name, e.value, e.validator_name) # demonstrating the values that you get on the object
    except TypeCheckFailed as e:  # < exception cls that your registered with schema
        print(e.name, e.current_type, e.expected_type) # demonstrating the values that you get on the object
```

2.
```python
"""
An Advanced Approach to Custom Exception Handling: Decorator Pattern
=====================================================================

This is an elegent ( yet advanced ) approach of handling the
custom exceptions with schema .
It uses a decorator based approach .
"""

def type_bad_request(name, current_type, expected_type):
    raise BadRequest(
        custom_message=f"Invalid {name}"
    ,   code="TYPE"
    )
def validation_bad_request(name, value, validation_name):
    __code__ = "VALIDATION"
    if validation_name == 'view_validator':
        __code__ = 'UNSUPPORTED-VIEW'
    raise BadRequest(
        custom_message=f"Invalid {name}"
    ,   code=__code__
    )

def exception_callbacks(_type: Callable=None, _validation: Callable=None): # <-- move this to better location
    """Rigister Exception Callbacks with TypeChecking Dataclass
    Args:
        _type (Callable, optional): callback for TypeError. Defaults to None.
        _validation (Callable, optional): callback for ValidationError. Defaults to None.
    """
    def _wrapper(cls):
        setattr(cls, "validator_exception", _validation)
        setattr(cls, "type_exception", _type)
        return cls
    return _wrapper
@exception_callbacks(_type=type_bad_request, _validation=validation_bad_request)
@dataclasses.dataclass(frozen=True)
class QueryParams(TypeCheck):
    view: str = 'month'
    supported_views = {'month','week','week-detail'}
    view_validator = lambda v: v.lower() in QueryParams.supported_views
```

[refer this practical flask server codebase for live usage of `TypeCheck`](#)

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

### CustomType

This is an Abstract Base Class for defining a type object that can be used as typehint in a [TypeCheck](#typecheck) schema .

Usage :

1. 
```python
# =========
# Example 1
# =========
import dataclasses
from pyutils.typecheck import TypeCheck, registry, CustomType
from typing import Any, List, Optional


# a custom type of our own
class IntList(CustomType):

    @staticmethod
    def guard(value: Any) -> bool:
    """TypeGurad
    This function will actually check if the value is a List of integers or not .
    """
    if isinstance(value, list) and all([isinstance(element, int) for element in value]):
        return True
    return False 

# Schema
@dataclasses.dataclass(frozen=True)
class SampleSchema(TypeCheck):
    """Sample Schema - for the testing purpose
    """
    data2: IntList
    value1: Optional[IntList]
    value2: str

# demonstration 1:
try:
    data: dict = {
        "data2": [1,2,3],
        "value1": [2],
        "value2": "2"
    }
    SampleSchema(**data)
except Exception:
    print("failed")
else:
    print("passed") # << this will be printed

# ---

# demonstration 2:
try:
    INCORRECT_VALUE = "3"
    data: dict = {
        "data2": [1,2,3],
        "value1": [2, INCORRECT_VALUE],
        "value2": "2"
    }
    SampleSchema(**data)
except Exception:
    print("failed") # << this will be printed
else:
    print("passed")

# ---

"""
Explaination :
--------------

* In first demonstration ,
"passed" will be printed on console .

* In second demonstration,
"failed" will be printed on console , because
a string value has been added to the data , which is
annotated as `IntList` .
"""
```

2.

```python
# ======================================
# Example 2 : alternate way of Example 1
# ======================================
import dataclasses
from pyutils.typecheck import TypeCheck, registry, CustomType
from typing import Any, List, Optional

# a custom type of our own
class IntList(CustomType): ...

# seperately writing the guard ( this can be kept in a seperate file for re-use)
def is_int_list(value: Any) -> bool:
    """TypeGurad
    This function will actually check if the value is a List of integers or not .
    """
    if isinstance(value, list) and all([isinstance(element, int) for element in value]):
        return True
    return False 

if __name__ == "__main__":

    # registering the guard function seperately onto the custum type
    setattr(IntList, "guard", staticmethod(is_int_list))

    # Schema
    @dataclasses.dataclass(frozen=True)
    class SampleSchema(TypeCheck):
        """Sample Schema - for the testing purpose
        """
        data2: IntList
        value1: Optional[IntList]
        value2: str
```

### Registerng `typing.*` typeguards

We can also register guard function for a specific  `typing.*` builtin type-hint .

Usage :

```python
import dataclasses
from pyutils.typecheck import TypeCheck, registry, CustomType
from typing import Any, List, Optional

# a typeguard function for list of strings :
def is_str_list(value: Any) -> bool:
    """TypeGurad
    This function will actually check if the value is a List of strings or not .
    """
    if isinstance(value, list) and all([isinstance(element, str) for element in value]):
        return True
    return False 
# a typeguard function for list of ints :
def is_int_list(value: Any) -> bool:
    """TypeGurad
    This function will actually check if the value is a List of integers or not .
    """
    if isinstance(value, list) and all([isinstance(element, int) for element in value]):
        return True
    return False 

# main
if __name__ == "__main__":
    registry[List[str]]=is_str_list
    registry[List[int]]=is_int_list
    
    # Schema
    @dataclasses.dataclass(frozen=True)
    class SampleSchema(TypeCheck):
        """Sample Schema - for the testing purpose
        """
        data1: List[str]
        data2: List[int]
        value1: Optional[List[int]]
        value2: str
    
    try:
        SampleSchema(**{
            "data1": ["a", "n", 1],
            "data2": [1, 2, 3],
            "value1": [1, 2, 3],
            "value2": "ankit"
        })
    except Exception as e:
        print(f"""
        Exception From Demonstration 1:
        {e}
        """)
    
```

---------------

## Local Development

Executing Tests :
```shell
python3 setup.py test

# it will execute all the tests listed in `pyutils.tests/` folder 
```

Creating a Build :
```shell
python3 setup.py bdist_wheel

```

Checking the correctness of a Build :
```shell
check-wheel-contents <path-to-dist-folder>

```