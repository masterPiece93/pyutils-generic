import unittest
import dataclasses
from pyutils.typecheck import TypeCheck, registry, CustomType
from typing import Any, List, Optional



# creating a custom type of our own
class IntList(CustomType): ...

# Schema
@dataclasses.dataclass(frozen=True)
class SampleSchema(TypeCheck):
    """Sample Schema - for the testing purpose
    """
    data1: List[str]
    data2: IntList
    value1: Optional[IntList]
    value2: str


def is_str_list(value: Any) -> bool:
    """TypeGurad

    - checks for List[str]
    """
    if isinstance(value, list) and all([isinstance(element, str) for element in value]):
        return True

    return False 

def is_int_list(value: Any) -> bool:
    """TypeGurad

    - checks for List[int]
    """
    if isinstance(value, list) and all([isinstance(element, int) for element in value]):
        return True

    return False 

# =======
# Testing
# ======= 

class PositiveTestCase(unittest.TestCase):
    """
    Positive test cases around the custom type
    """

    def setUp(self):
        # This is How we need to register our typeguards 
        setattr(IntList, "guard", staticmethod(is_int_list))    # A custom type
        registry[List[str]]=is_str_list                         # typing.List[str]

    def test_positive(self):

        correct_data: dict = {
            "data1": ["1","s"],
            "data2": [1,2,3],
            "value1": [2],
            "value2": "2"
        }
        SampleSchema(**correct_data)

    def tearDown(self):
        delattr(IntList, "guard")
        del registry[List[str]]


class NegetiveTestCase(unittest.TestCase):
    """
    Negative test cases around the custom type
    """

    def setUp(self):
        # This is How we need to register our typeguards 
        setattr(IntList, "guard", staticmethod(is_int_list))    # A custom type
        registry[List[str]]=is_str_list                         # typing.List[str]

    def test_negetive_1(self):
        
        with self.assertRaises(TypeError) as e:
            INCORRECT_VALUE = "3"
            incorrect_data: dict = {
                "data1": ["1","s"],
                "data2": [1,2,3],
                "value1": [2, INCORRECT_VALUE], # a string value is added to the list
                "value2": "2"
            }
            SampleSchema(**incorrect_data)

    def tearDown(self):
        delattr(IntList, "guard")
        del registry[List[str]]


if __name__ == '__main__':
    unittest.main()