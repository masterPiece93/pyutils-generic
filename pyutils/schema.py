"""
Simple Schema Validator
=======================

efficient for basic straightforward usecases

This script shows an exerpt from a part of
process , where a incoming pub/sub message
is validated against a predefined schema.

* Class:JsonDictValidator - is developed as a reusable
  validator meta class for validating a python dict 
  against a schema .
  The schema can be defined declaratively in a sub class 
  that uses JsonDictValidator as a metaclass .
  
* Class:IngestionMessage - is the class that defines
  the schema for a pub/sub message dict . It uses
  `class:JsonDictValidator` as a metaclass for being able
  to define a schema .

"""
from typing import ClassVar, Optional, Callable
from abc import abstractmethod


class ValidatorMeta(type):
    """
    Abstract Base for Validator Classes

    * class must have `validate` method
    * `validate` method must be an instance method
    * class variables are READ ONLY

    Usage:
        class Xyz(metaclass=ValidtaorMeta):
            ...
    """
    def __new__(cls, name, bases, dct):
        # Enforce that the 'validate' method is in the class dictionary
        method_name='validate'
        if 'validate' not in dct or isinstance(dct["validate"], classmethod) or isinstance(dct["validate"], staticmethod):
            raise TypeError(
                f"Can't instantiate abstract class {name}"
                f"without an implementation for abstract class method {method_name}"
            )
        
        # Call the superclass's (ABCMeta's) __new__ method to create the class
        return super().__new__(cls, name, bases, dct)
    
    def __setattr__(cls, name, value):
        if name in cls.__dict__:
            raise AttributeError(f"Cannot modify constant '{name}' on ReadOnly Class {cls.__qualname__}")
        super().__setattr__(name, value)


class JsonDictValidator(metaclass=ValidatorMeta):
    """
    Validates the provided dict paylod against
        the provided validation specification
    
    - applies any additional formatting if specified
    """
    class SchemaViolation(Exception):
        """Indicates the violation of validation specification"""

    SCHEMA_VIOLATION_EXCEPTION: ClassVar[Exception] = SchemaViolation
    ALLOWED_EXTRA_KEYS: ClassVar[bool] = False
    FORMATTERS: ClassVar[dict] = {}

    @abstractmethod
    def validate(self, json_payload: dict, logger: Optional[Callable] = None, message_wrapper: Optional[Callable] = None) -> Optional[Exception]:
        """
        Default validation logic
        """

        def do_logging(msg: str, level: str = 'info'):
            msg = message_wrapper(msg) if message_wrapper else msg
            if logger:
                logger(msg, level=level)
            else:
                print(f'{level.upper()} : ', msg)
        
        self._check_specification(json_payload, self.VALIDATION_SPECIFICATION, allow_extra_keys=self.ALLOWED_EXTRA_KEYS, formatters=self.FORMATTERS, do_logging=do_logging)

    def _check_specification(self, json_payload: dict, specs: dict, allow_extra_keys: bool, formatters: dict, do_logging=lambda msg, level: print(f'{level.upper()} : ', msg)) -> bool:
        """
        Checks if the provided json_payload adheres to the validation specification
        without raising exceptions.
        Returns True if valid, False otherwise.
        """
        
        if not isinstance(json_payload, dict):
            log_msg = f'Payload is not a dictionary. Got {type(json_payload)}'
            do_logging(log_msg, 'error')
            raise self.SCHEMA_VIOLATION_EXCEPTION(log_msg)

        if len(json_payload) == 0:
            log_msg = f'Payload is empty'
            do_logging(log_msg, 'error')
            raise self.SCHEMA_VIOLATION_EXCEPTION(log_msg)

        for key, spec in specs.items():

            if len(spec) == 4:
                is_required, expected_type, default_value, nested_constraints = spec
            else:
                is_required, expected_type, default_value = spec
                nested_constraints = None

            if key not in json_payload:
                if is_required:
                    log_msg = f'{self.SCHEMA_VIOLATION_EXCEPTION.__name__}:`{key}` Key Required'
                    do_logging(log_msg, 'error')
                    raise self.SCHEMA_VIOLATION_EXCEPTION(log_msg)
                else:
                    json_payload[key]=default_value

            value = json_payload[key]

            if not isinstance(value, expected_type):
                log_msg = f'`{key=}` is expected of type {expected_type}, got {type(value)}'
                do_logging(log_msg, 'error')
                raise self.SCHEMA_VIOLATION_EXCEPTION(log_msg)
            
            if nested_constraints:
                if isinstance(nested_constraints, dict):
                    if not isinstance(json_payload[key], dict):  # pragma: no cover - unreachable, guarded by the expected_type check above
                        log_msg = f'`Nested Dict Exepected : {key=}` is expected of type {dict}, got {type(json_payload[key])}'
                        do_logging(log_msg, 'error')
                        raise self.SCHEMA_VIOLATION_EXCEPTION(log_msg)
                    if len(json_payload[key]) == 0:
                        log_msg = f'Nested ({key}) : Payload is empty'
                        do_logging(log_msg, 'error')
                        raise self.SCHEMA_VIOLATION_EXCEPTION(log_msg)
                    self._check_specification(json_payload[key], nested_constraints, do_logging=do_logging, allow_extra_keys=allow_extra_keys, formatters=formatters)
                if isinstance(nested_constraints, list) and len(nested_constraints) == 1 and isinstance(nested_constraints[0], dict):
                    if not all(isinstance(item, dict) for item in value):
                        log_msg = f'`Nested List of Dicts Exepected : {key=}` is expected of type {list} of {dict}, got {type(json_payload[key])}'
                        do_logging(log_msg, 'error')
                        raise self.SCHEMA_VIOLATION_EXCEPTION(log_msg)
                    for item in value:
                        self._check_specification(item, nested_constraints[0], do_logging=do_logging, allow_extra_keys=allow_extra_keys, formatters=formatters)

            json_payload[key] = formatters.get(key, lambda v:v)(value)

        if not allow_extra_keys:
            extra_keys = json_payload.keys() - specs.keys()
            if extra_keys:
                log_msg = f'Extra Key : {extra_keys} Not Allowed'
                do_logging(log_msg, 'error')
                raise self.SCHEMA_VIOLATION_EXCEPTION(log_msg)
