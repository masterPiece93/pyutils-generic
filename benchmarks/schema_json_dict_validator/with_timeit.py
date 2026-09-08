"""
Benchmarking
============
"""
import timeit
from pyutils_generic.schema import JsonDictValidator

from typing import Optional, ClassVar


class InputSchema1(JsonDictValidator):
    """
    Example schema 1
    """
    VALIDATION_SPECIFICATION: dict = {
        "eventId":  (True, str, None),
        "username": (True, str, None),
    }

    def validate(self, json_payload: dict, logger: Optional[callable] = None, message_wrapper: Optional[callable] = None) -> Optional[Exception]:
        """
        Validate the input data against the InputSchema1
        """
        return super().validate(json_payload, logger=logger, message_wrapper=message_wrapper)


class InputSchema2(JsonDictValidator):
    """
    Example schema 2
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

    def validate(self, json_payload: dict, logger: Optional[callable] = None, message_wrapper: Optional[callable] = None) -> Optional[Exception]:
        """
        Validate the input data against the InputSchema2
        """
        return super().validate(json_payload, logger=logger, message_wrapper=message_wrapper)


# Entrypoint for benchmarking
if __name__ == "__main__":

    # Measure the time taken for validation
    
    # Test 1
    # ------
    print("Test with InputSchema1:")
    # Test data for InputSchema1
    input_data = {"eventId": "123", "username": "test_user"}
    # Measure the time taken for validation using timeit
    execution_time = timeit.timeit(
        stmt="""validator.validate(input_data)
        """,
        number=1000,
        globals={"validator": InputSchema1(), "input_data": input_data}
    )
    print(f"\t - Time taken for validation (1000 runs): {execution_time:.6f} seconds")
    
    # --- x ---

    # Test 2
    # ------
    print("Test with InputSchema2:")
    # Test data for InputSchema2
    input_data = {
        "eventId": "123",
        "username": "test_user",
        "url": "/test/url",
        "orgId": "org_456",
        "tenancy": "tenant_789",
        "orgName": {"max_length": 50, "min_length": 5, "pattern": "^[a-zA-Z0-9_]+$"},
        "user": [
            {"first_name": "John", "age": 30, "email": "john@example.com"},
            {"first_name": "Jane", "age": 25},
            {"first_name": "Alice", "age": 28, "email": "alice@example.com"}
        ]
    }
    # Measure the time taken for validation using timeit
    execution_time = timeit.timeit(
        stmt="""validator.validate(input_data)
        """,
        number=1000,
        globals={"validator": InputSchema2(), "input_data": input_data}
    )
    print(f"\t - Time taken for validation (1000 runs): {execution_time:.6f} seconds")

    # --- x ---

    # Test 3
    # ------
    print("Test with InputSchema2 (type 2):")
    # Test data for InputSchema2
    input_data = {
        "eventId": "123",
        "username": "test_user",
        "url": "/test/url",
        "orgId": "org_456",
        "tenancy": "tenant_789",
        "orgName": {"max_length": 50, "min_length": 5, "pattern": "^[a-zA-Z0-9_]+$"},
        "user": [{"first_name": f"User {v}", "age": 30, "email": f"user{v}@example.com"} for v in range(1000)]
    }
    # Measure the time taken for validation using timeit
    execution_time = timeit.timeit(
        stmt="""validator.validate(input_data)
        """,
        number=1000,
        globals={"validator": InputSchema2(), "input_data": input_data}
    )
    print(f"\t - Time taken for validation (1000 runs): {execution_time:.6f} seconds")

    # --- x ---

    # Script Run : python3 with_timeit.py
