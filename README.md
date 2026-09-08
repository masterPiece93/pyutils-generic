# pyutils_generic

![Dynamic TOML Badge](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2FmasterPiece93%2Fpyutils-generic%2Frefs%2Fheads%2Fmain%2Fpyproject.toml&query=%24.project.version&logoColor=%23000000&label=latest%20version&labelColor=black)

[![PyPI - Version](https://img.shields.io/pypi/v/pyutils-generic)](https://pypi.org/project/pyutils-generic) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyutils-generic) ![PyPI - Status](https://img.shields.io/pypi/status/pyutils-generic) ![PyPI - License](https://img.shields.io/pypi/l/pyutils-generic)

[![tests](https://github.com/masterPiece93/pyutils-generic/actions/workflows/tests.yml/badge.svg)](https://github.com/masterPiece93/pyutils-generic/actions/workflows/tests.yml) [![coverage](https://raw.githubusercontent.com/masterPiece93/pyutils-generic/badges/coverage.svg)](https://github.com/masterPiece93/pyutils-generic/actions/workflows/tests.yml) [![Pylint](https://github.com/masterPiece93/pyutils-generic/actions/workflows/pylint.yml/badge.svg)](https://github.com/masterPiece93/pyutils-generic/actions/workflows/pylint.yml) [![Upload Python Package](https://github.com/masterPiece93/pyutils-generic/actions/workflows/release.yml/badge.svg)](https://github.com/masterPiece93/pyutils-generic/actions/workflows/release.yml) ![PyPI - Types](https://img.shields.io/pypi/types/pyutils-generic?color=pink)

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
    -e git+https://github.com/masterPiece93/pyutils_generic.git#egg=pyutils_generic
    ```

    ```sh
    pip install -r requirements.txt
    ```

- direct
    ```sh
    pip install -e git+https://github.com/masterPiece93/pyutils_generic.git#egg=pyutils_generic
    ```

output of pip-freeze command :
```
-e git+https://github.com/masterPiece93/pyutils_generic.git@7c8a56f4040e578b1dc3059a9cef321bca192cf8#egg=google_drive_examples
```

this value `7c8a56f4040e578b1dc3059a9cef321bca192cf8` in the above pip-freeze output , is the latest commit hash of the repository .

> Note : if you are mentioning `-e` , it is mandatory to attach `#egg=<your-pkg-name>` in the url .

[Usefulness of symbolic link](#benefits-of-using-symbolic-link)


#### Method 2 : direct url

- within requirements file :
    ```txt
    # requirements.txt
    git+https://github.com/masterPiece93/pyutils_generic.git
    ```

    ```sh
    pip install -r requirements.txt
    ```

- direct
    ```sh
    pip install git+https://github.com/masterPiece93/pyutils_generic.git
    ```

output of freeze command :
```
pyutils_generic==1.0.0
```


#### Method 3 : direct url with Tag Specification

- within requirements file :
    ```txt
    # requirements.txt
    git+https://github.com/masterPiece93/pyutils_generic.git@v1.0.0
    ```

    ```sh
    pip install -r requirements.txt
    ```

- direct
    ```sh
    pip install git+https://github.com/masterPiece93/pyutils_generic.git@v1.0.0
    ```

output of freeze command :
```
pyutils_generic==1.0.0
```

NOTE : since this is a private repo , you need a use PAT for external usages .

##### Install in a Docker Container :
we use Docker's `mount secrets` for this purpose 
- Add following in your Dockerfile : 

  ```Dockerfile
  # Install git
  RUN apt-get update && \
      apt-get install -y git
  
  # secret retreival
  RUN --mount=type=secret,id=api_key,target=/run/secrets/api_key_file \
     API_KEY=$(cat /run/secrets/api_key_file) && \
     pip install --no-cache-dir git+https://masterPiece93:$API_KEY@github.com/masterPiece93/pyutils_generic.git 
  ```

- Build docker command :
  ```sh
  # mounting build time secert
  DOCKER_BUILDKIT=1 docker build --secret id=api_key,src=./PAT.txt -t datti:latest .
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
from pyutils_generic import elf

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
## pyutils_generic.immutables

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
from pyutils_generic.immutables import ReadOnlyDictWrapper

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
from pyutils_generic.immutables import imdict

d = imdict(a=2,b=[1,2])
```

### ReadOnlyMeta

This is a meta class , used to convert any class into `Read Only` .

## pyutils_generic.colored

### cprint

This is an alternative to python-native print function , for printing coloured outputs on console/stdout .

Drawbacks :

- only allows some limited (yet standars) colors .
- converts entire output in one color ( which is obvious as it's made though ) .
- does'nt allow bold with colors .
- not much extra options .

Usage :

- [Refer : examples](./examples/printing_coloured.py)

```python
"""
Sample Usage
"""
from pyutils_generic.printing import cprint

cprint("This is a blue message.").style(Palette.BLUE)
cprint("Hello, World!").style(B=True)
cprint("This is a heading \n\n").style(B=True, U=True)
```

- [Refer : docs :: colored](./docs/colored.md)

## pyutils_generic.typecheck

### @strict

This is an argument checking decorator . It's sole purpose is to check typehints in function arguments .

Drawbacks :

-

Usage :

```python
from pyutils_generic.typecheck import strict


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

from pyutils_generic.printing import cprint
from pyutils_generic.typecheck import TypeCheck, strict
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
    ...ReadOnlyMeta
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

from pyutils_generic.typecheck import TypeCheck, strict, CoercedType

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
from pyutils_generic.typecheck import TypeCheck, registry, CustomType
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
from pyutils_generic.typecheck import TypeCheck, registry, CustomType
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
from pyutils_generic.typecheck import TypeCheck, registry, CustomType
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

## pyutils_generic.schema

### JsonDictValidator

This is a simple schema defination and validation helper , that aims to be readable and very intutive . It's sole purpose is to check a json type data payload .

Drawbacks :

- it get's slower as the schema gets more nested and data to be validated becomes huge

Pros :

- the schema defined using this are very simple and basic ( for basic situations ) and very intutive so that all the expectations from the data to be validated are in a same structural format as the data itself would .

Usage :

```python
from pyutils_generic.schema import JsonDictValidator


# ===============
# main entrypoint
# ===============
# * demonstrates the usage of JsonDictValidator with IngestionMessage classes as an example
if __name__ == '__main__':

    # Defining a concrete implementation of JsonDictValidator for Ingestion Messages
    class IngestionMessage(JsonDictValidator):
        """A Simple Dict Validator for 
        Ingestion Message Json Payload
        """
        VALIDATION_SPECIFICATION: ClassVar[dict] = {    # Required
            # KEY       ( Req, type, default )
            "eventId":  (True, str, None),
            "username": (True, str, None),
            "url":      (True, str, None),
            "orgId":    (True, str, None),
            "tenancy":  (True, str, None),
            "orgName":  (True, dict, None, {
                "max_length":   (False, int, 100),
                "min_length":   (False, int, 0),
                "pattern":      (False, str, r"^[a-zA-Z0-9_]+$")
            }),
            "user":    (True, list, None, [{
                "first_name":   (True, str, None),
                "age":          (True, int, None),
                "email":        (False, str, ''),
            }]),
        }
        ALLOWED_EXTRA_KEYS: ClassVar[bool] = False      # Optional
        FORMATTERS: ClassVar[dict] = {                  # Optional
            "url": lambda value: value.lstrip("/"),
        }

        def validate(self, json_payload: dict, message_id: str) -> None:
            """Validate Ingestion Message"""
            # logging handler
            _logger = lambda msg, level: log.log(get_numeric_level(level), msg)
            # message formulation
            _message_wrapper = lambda log_msg: msg(log_msg, pubsub_message_id=message_id)
            # using default schema validation
            super().validate(json_payload, logger=_logger, message_wrapper=_message_wrapper)

    # Testing the IngestionMessage Validator
    try:
        IngestionMessage.ALLOWED_EXTRA_KEYS=True
    except AttributeError as e:
        assert str(e) == "Cannot modify constant 'ALLOWED_EXTRA_KEYS' on ReadOnly Class IngestionMessage"
    
    # Sample Payload for Testing
    data: dict = {
            "eventId":  '(True, str, None)',
            "username": '(True, str, None)',
            "url":      '/(True, str, None)/',
            "orgId":    '(True, str, None)',
            "tenancy":  '(True, str, None)',
            "orgName":  {
                "max_length": 100,
            },
            "user":    [
                {
                    "first_name":   'ankit',
                    "age":          33,
                },
                {
                    "first_name":   'john_doe',
                    "age":          28,
                    "email":        'john@example.com',
                }
            ],
            # "channel":  '(True, str, None)',
            # "extra":    '(True, str, None)',
        }

    # Validating the Sample Payload
    IngestionMessage().validate(
        data, '187129034567124876'
    )
    print(data) # Prints the validated and formatted data
```
---------------

## Local Development

Setup :
```bash
python3 -m venv .venv
source .venv/bin/activate

pip install -e ".[dev]"
```

Executing Tests :
```shell
python -m unittest discover -s pyutils_generic/tests -p 'test_*.py' -v

# it will execute all the tests listed in `pyutils_generic/tests` folder 
```

Creating a Build :

> All packaging metadata now lives in `pyproject.toml` (PEP 517/621). `setup.py`
> is kept only as a legacy shim (`setup()` with no args) — prefer `python -m build`
> over `python setup.py bdist_wheel`.

```shell
pip install build
python -m build

# produces both an sdist (.tar.gz) and a wheel (.whl) under dist/
```

Checking the correctness of a Build :
```shell
pip install check-wheel-contents twine

check-wheel-contents dist/*.whl
# -> dist/pyutils_generic-<version>-py3-none-any.whl: OK

twine check dist/*
# -> Checking dist/pyutils_generic-<version>-py3-none-any.whl: PASSED
# -> Checking dist/pyutils_generic-<version>.tar.gz: PASSED
```

> ✅ Verified: `python -m build` produces both wheel + sdist cleanly,
> `check-wheel-contents` reports `OK`, and `twine check` reports `PASSED` for
> both artifacts. The wheel includes the `py.typed` marker (PEP 561) and
> correctly excludes the `pyutils_generic.tests` package (see
> `[tool.setuptools.packages.find]` / `exclude` in `pyproject.toml`).

Coverage :

```bash
# single test
python3 -m coverage run -m unittest -v pyutils_generic.tests.test_dict_validator
```
```bash
# all tests
python3 -m coverage run -m unittest discover -s pyutils_generic/tests -p 'test_*.py'
```
```bash
# coverage report
python3 -m coverage report -m
```
```bash
# browsable HTML report
python3 -m coverage html   # -> htmlcov/index.html
```
