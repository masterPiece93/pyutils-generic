from pyutils.typecheck import CustomType, registry, TypeCheck
from dataclasses import dataclass
from typing import Any, List

class IntList(CustomType): ...

def is_str_list(value: Any) -> bool:

    if isinstance(value, list) and all([isinstance(element, str) for element in value]):
        return True

    return False 

def is_int_list(value: Any) -> bool:

    if isinstance(value, list) and all([isinstance(element, int) for element in value]):
        return True

    return False 

setattr(IntList, "guard", staticmethod(is_int_list))

registry[List[str]]=is_str_list

@dataclass(frozen=True)
class TestSchema(TypeCheck):
    data1: List[str]
    data2: IntList

if __name__ == '__main__':

    TestSchema(**{"data1": ["1","s"], "data2": [1,2,"3"]})
