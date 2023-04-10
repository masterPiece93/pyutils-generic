import dataclasses


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
class User(TypeCheck):
    name: str
    age: int
    contacts: tuple = (...,)

    name_validator = lambda value: value.islower()
    contacts_validator = lambda value: all([v.isdigit() and len(v) == 10 for v in value])

    def max_contacts_validation(self) -> None:
        if len(self.contacts) > 3:
            raise ValueError('user contact must have 10 digits')
