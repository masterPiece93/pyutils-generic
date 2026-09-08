import unittest
import dataclasses
import datetime
from pyutils_generic.typecheck import TypeCheck, registry, CustomType
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

# ========

class Json(CustomType):
    """
    Custom type for JSON

    add arrangement for error placement.
    """

    @staticmethod
    def guard(value: Any) -> bool:
        """TypeGuard

        - checks for JSON
        """

        if not isinstance(value, dict):
            return False

        # recursive check for a single JSON value
        def is_valid_value(value: Any) -> bool:
            # scalar (leaf) values are always valid
            if isinstance(value, (str, int, float, bool)):
                return True
            # a list may only contain scalars or dicts (no nested lists)
            elif isinstance(value, list):
                return all(
                    isinstance(item, (str, int, float, bool, dict))
                    and is_valid_value(item)
                    for item in value
                )
            # every key must be a str and every value a valid JSON value
            elif isinstance(value, dict):
                return all(
                    isinstance(k, str) and is_valid_value(v)
                    for k, v in value.items()
                )
            # anything else (e.g. a nested list, set, object) is invalid
            else:
                return False

        # a top-level dict is valid when all keys are str and all values valid
        return all(
            isinstance(key, str) and is_valid_value(val)
            for key, val in value.items()
        )



class CummulativeTestCase(unittest.TestCase):
    """
    Cummulative test cases around the custom type
    """

    def setUp(self):

        def is_json_list(value: Any) -> bool:
            """TypeGuard

            - checks for List[Json]
            """
            if isinstance(value, list) and all([isinstance(element, dict) for element in value]):
                for element in value:
                    # check for the JSON
                    if not Json.guard(element):
                        return False
                return True

            return False
        registry[List[Json]] = is_json_list # typing.List[Json] registered
        registry[List[str]] = is_str_list
        registry[List[int]] = is_int_list

    def test_cummulative(self):
        
        # creating a test schema
        @dataclasses.dataclass(frozen=True)
        class _TestSchema(TypeCheck):
            data1: List[str]
            data2: list
            value1: Optional[List[int]]
            value2: str
            json_data: List[Json]
            # json_data: List[Json] = field(default_factory=list)

        # subTest 1 -
        with self.subTest(f"-- SubTest-1 : Test with correct data", number=1):
            # correct data :
            correct_data: dict = {
                "data1": ["1", "s"],
                "data2": [1, 2, "3", "four", 5.0],
                "value1": [2],
                "value2": "2",
                "json_data": [
                    {"key1": 1},
                    {"key2": [1, 2, 3]},
                    {"key3": {"key4": 1, "key5": 2}},
                    {"key6": "value"},
                ]
            }
            # test
            _TestSchema(**correct_data)

        # subTest 2 -
        with self.subTest("-- SubTest-2.1 : Test with incorrect data ( a datetime object )", number=2):
            # in-correct data :
            INCORRECT_VALUE = datetime.datetime.now()
            incorrect_data: dict = {
                "data1": ["1", "s"],
                "data2": [1, 2, "3", "four", 5.0],
                "value1": [2],
                "value2": "2",
                "json_data": [
                    {"key0": INCORRECT_VALUE},
                    {"key1": 1},
                    {"key2": [1, 2, 3]},
                    {"key3": {"key4": 1, "key5": 2}},
                    {"key6": "value"},
                ]
            }
            # test
            with self.assertRaises(TypeError) as e:
                _TestSchema(**incorrect_data)

        # subTest 3 -
        with self.subTest("-- SubTest-2.2 : Test with incorrect data ( a list of lists )", number=3):
            # in-correct data :
            INCORRECT_VALUE = [1, [2, 3]] # a list of list
            incorrect_data: dict = {
                "data1": ["1", "s"],
                "data2": [1, 2, "3", "four", 5.0],
                "value1": [2],
                "value2": "2",
                "json_data": [
                    {"key0": INCORRECT_VALUE},
                    {"key1": 1},
                    {"key2": [1, 2, 3]},
                    {"key3": {"key4": 1, "key5": 2}},
                    {"key6": "value"},
                ]
            }
            # test
            with self.assertRaises(TypeError) as e:
                _TestSchema(**incorrect_data)

        # subTest 4 -
        with self.subTest("-- SubTest-2.3 : Test with incorrect data ( a list of lists at nested level )", number=4):
            # in-correct data :
            INCORRECT_VALUE = [1, [2, 3]] # a list of list
            incorrect_data: dict = {
                "data1": ["1", "s"],
                "data2": [1, 2, "3", "four", 5.0],
                "value1": [2],
                "value2": "2",
                "json_data": [
                    {"key0": {
                        "nested_key1": 2.3,
                        "nested_key2": INCORRECT_VALUE,
                    }},
                    {"key1": 1},
                    {"key2": [1, 2, 3]},
                    {"key3": {"key4": 1, "key5": 2}},
                    {"key6": "value"},
                ]
            }
            # test
            with self.assertRaises(TypeError) as e:
                _TestSchema(**incorrect_data)

    def tearDown(self):

        del registry[List[str]]
        del registry[List[int]]
        del registry[List[Json]]

if __name__ == '__main__':
    unittest.main(
        
    )