import inspect
import dataclasses
from typing import List, Union, get_args
from pyutils_generic import __all_builtin_types__
from abc import ABC, abstractmethod

__typing_SpecialGenericAlias__ = type(List)
__typing_GenericAlias__ = type(List[str])
__typing_UnionGenericAlias__ = type(Union[str, int])

# TODO : use typing.get_origin(...) method for determining the typing.* types

__all__ = [
    'ArgumentTypeError',
    'ReturnTypeError',
    'strict',
    'TypeCheck',
    'CoercedType',
    'registry',
    'CustomType'
]

registry : dict = {}


class ArgumentTypeError(TypeError):
    """Argument value Type mismatch againt function arg(*args) type-hint specification"""
    def __init__(self,fn_identifier, arg_name,arg_type,current_type) -> None:
        self.message = f"\nFunction - {fn_identifier} \n Argument `{arg_name}` is typed as {arg_type} , but value of type {current_type} is passed"
        super().__init__()
    def __str__(self) -> str:
        return self.message


class ReturnTypeError(TypeError):
    """Return value Type mismatch againt function return(->) type-hint specification"""
    def __init__(self, fn_identifier,return_type, current_return_type) -> None:
        super().__init__()
        self.message = f"\nFunction - {fn_identifier} \n Return Value is typed as {return_type} , but value of type {current_return_type} is returned"
    __str__ = lambda self: self.message


def strict(func):
    annotations = func.__annotations__
    
    code = func.__code__
    fn_arg_names :tuple = code.co_varnames
    fn_arg_count :int = code.co_argcount

    def _do_check(param, value, _type):
        if type(value) is not _type:
            raise ArgumentTypeError(f"{func.__name__} ({code.co_filename})",param, _type, type(value))
    def wrapper(*args,**kwargs):
        for index,param_name in enumerate(fn_arg_names[:fn_arg_count]):
            try:
                _type = annotations[param_name]
                value = args[index] if index < len(args) else kwargs[index]
            except KeyError: continue
            else: _do_check(param_name, value, _type)

        return_type = annotations.get('return',...)
        result = func(*args,**kwargs)
        if return_type is not ... and type(result) is not return_type:
            raise ReturnTypeError(f"{func.__name__} ({code.co_filename})",return_type,type(result))
        return result
    return wrapper


@dataclasses.dataclass(frozen=True)
class TypeCheck:
    def __post_init__(self):

        for (name, field_type) in self.__annotations__.items():

            self._typechecking(name, field_type)

        # TODO: add support for multiple validations for a particular field
        for (name, value) in self.__class__.__dict__.items():
            if name.endswith('_validator') and name.rstrip('_validator') in self.__dict__ and callable(value):
                if not value(getattr(self, name.rstrip('_validator'))):
                    parameter_name, parameter_value = name.rstrip('_validator'), getattr(self, name.rstrip('_validator'))
                    if not self.__class__.__dict__.get('validator_exception'):
                        raise ValueError(f"Schema Validation Fail : `{self.__class__.__name__}` Schema\nThe field validation `{name}` asserts False .")
                    else:
                        if callable(self.__class__.__dict__['validator_exception']):
                            raise self.__class__.__dict__['validator_exception'](parameter_name, parameter_value, name)
                        elif type(self.__class__.__dict__['validator_exception']) == type and issubclass(self.__class__.__dict__['validator_exception'], Exception): # TODO : isClass check missing
                            raise self.__class__.__dict__['validator_exception'](f"Schema Validation Fail : `{self.__class__.__name__}` Schema\nThe field validation `{name}` asserts False .")
    
    def _typechecking(self, name, field_type) -> None:
        """Main Typechecking logic"""
        if field_type in __all_builtin_types__:
            # This>Block> handling builtin types like - str, list, dict ...
            current_type = type(self.__dict__[name])
            _message: str = f"Schema Violation : `{self.__class__.__name__}` Schema"\
                            f"\nThe field `{name}` is typed as `{field_type}`,"\
                            f"but value of type `{current_type}` is assigned ."
            if not isinstance(self.__dict__[name], field_type):
                self._type_exception_handling(
                        name,
                        field_type,
                        exception_message=_message
                    )
        else:
            _message: str = f"Schema Violation : `{self.__class__.__name__}` Schema"\
                            f"\nThe field `{name}` is typed as `{field_type}`,"\
                            "but the value passed doesn't conform to this." # TODO: modify this to more meaningful message 
            if inspect.isclass(field_type) and issubclass(field_type, CustomType):
                if not field_type.guard(self.__dict__[name]):
                    self._type_exception_handling(
                        name,
                        field_type,
                        exception_message=_message
                    )
            elif isinstance(field_type, __typing_UnionGenericAlias__):
                # This>Block> handling Union types like - Union[T, ...], Optiobal[T]
                _internal_args = get_args(field_type)
                _last_internal_arg = _internal_args[-1]

                if _last_internal_arg == type(None):
                    # This>Block> Optional type detected
                    if isinstance(self.__dict__[name], type(None)):
                        ... # Do Nothing
                    else:
                        self._typechecking(name, _internal_args[0])

                # TODO :
                #       TODO > for a Union type , you can loop on all
                #       TODO > `_internal_args` , resolve their types and 
                #       TODO > do a recursive call to self._typechecking(...)


                
            elif isinstance(field_type, (__typing_SpecialGenericAlias__, __typing_GenericAlias__)):
                # handling Generic types like - List, List[T], Dict[T1, T2] etc ...
                # TODO : add support for recursive handling .
                
                if not registry[field_type](self.__dict__[name]):
                    self._type_exception_handling(
                        name,
                        field_type,
                        exception_message=_message
                    )
            
            else:
                raise Exception(f'The {field_type} is not a supported type.')

    def _type_exception_handling(self, name, field_type, exception_message):
        """
        Handles the exception raising logic
        raises TypeError(...) if custom `type_exception` variable
            is not specified by user .
        """
        current_type = type(self.__dict__[name])
        if not self.__class__.__dict__.get('type_exception'):
            raise TypeError(exception_message)
        else:
            if callable(self.__class__.__dict__['type_exception']):
                raise self.__class__.__dict__['type_exception'](name, current_type, field_type)
            elif type(self.__class__.__dict__['type_exception']) == type and inspect.isclass(self.__class__.__dict__['type_exception']) and issubclass(self.__class__.__dict__['type_exception'], Exception):
                raise self.__class__.__dict__['type_exception'](exception_message)


@dataclasses.dataclass(frozen=True)
class CoercedType:
    class AnnotationTypeError(TypeError):...
    class MandatoryKeyMissingError(Exception):...
    class CoersionError(ValueError):...
    def __post_init__(self):
        _error_ref: str = f"CoercedType ({self.__class__.__name__})"
        _mandatory_keys = ('value', 'coercion')
        key1, key2 = (*_mandatory_keys,)

        if not all(k in self.__annotations__ for k in _mandatory_keys):
            raise self.MandatoryKeyMissingError(f'{_error_ref}\nmissing any of mandatory keys : {_mandatory_keys}')
        if len(self.__annotations__) > 2:
            raise Exception(f"{_error_ref}\nIn a coerced-type , Cannot specify annotated fields other than the mandatory ones {_mandatory_keys}")
        if self.__annotations__[key1] not in __all_builtin_types__:
            raise self.AnnotationTypeError(f'{_error_ref}\n`{key1}` should be annotated to any one of python-builtin type')
        if self.__annotations__[key2] is not dict:
            raise self.AnnotationTypeError(f'{_error_ref}\n`{key2}` should be annotated as {dict}')
        value, its_annotattion = self.__dict__[key1], self.__annotations__[key1]
        if type(value) not in self.__dict__[key2]:
            raise self.CoersionError(f'{_error_ref}\nInput value `{value}<{type(value)}>` cannot be coerced.')
        coerced_value = self.__dict__[key2][type(value)](value)
        if not isinstance(coerced_value, its_annotattion):
            raise self.CoersionError(f'{_error_ref}\n`Input value `{value}<{type(value)}>` must coerce to annotated type -> {its_annotattion}. Instead, getting coerced to type<{type(coerced_value)}>')
        self.__dict__[key1] = coerced_value
    __str__ = lambda self: f"{self.value}"


class CustomType(ABC):
    """
    helps creating a custom type

    inherit this & set a static method for validating
        any value for that type ( i.e TypeGuard )
    """
    @staticmethod
    @abstractmethod
    def guard(self, ): ...
