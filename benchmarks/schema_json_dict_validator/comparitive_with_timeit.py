"""
Comparative Benchmarking
=========================
"""
import subprocess
import sys
import timeit
from pyutils.schema import JsonDictValidator

SAMPLE_JSON_PAYLOAD = {
    "eventId": "123",
    "username": "test_user",
    "sampleField": {
        "NestedField": {
            "max_length": 50,
            "min_length": 5,
            "pattern": "^[a-zA-Z0-9_]+$"
        },
        "NestedList": [
            {"first_name": "John", "age": 30, "email": "john@example.com"},
            {"first_name": "Jane", "age": 25, "email": "jane@example.com"},
            *[{"first_name": f"User {v}", "age": 30, "email": f"user{v}@example.com"} for v in range(1000)],
        ]
    },
    "NestedList": [
        {"first_name": "John", "age": 30, "email": "john@example.com"},
        {"first_name": "Jane", "age": 25, "email": "jane@example.com"},
        *[{"first_name": f"User {v}", "age": 30, "email": f"user{v}@example.com"} for v in range(1000)]
    ]
}

class TestSchemaForJsonDictValidator(JsonDictValidator):
    """
    Example schema for validating a JSON payload using JsonDictValidator.
    """
    VALIDATION_SPECIFICATION: dict = {
        "eventId":  (True, str, None),
        "username": (True, str, None),
        "sampleField": (False, dict, {}, {
            "NestedField": (True, dict, None, {
                "max_length":   (False, int, 100),
                "min_length":   (False, int, 0),
                "pattern":      (False, str, r"^[a-zA-Z0-9_]+$")
            }),
            "NestedList": (False, list, [], [{
                "first_name":   (True, str, None),
                "age":          (True, int, None),
                "email":        (False, str, ''),
            }])
        }),
        "NestedList": (False, list, [], [{
            "first_name":   (True, str, None),
            "age":          (True, int, None),
            "email":        (False, str, ''),
        }]),
    }


    def validate(self, json_payload: dict) -> bool:
        """
        Validate the input data against the TestSchema1
        """
        return super().validate(json_payload)


test_schema_for_jsonschema: dict = {
  "$schema": "https://json-schema.org",
  "title": "EventPayloadSchema",
  "type": "object",
  "required": [
    "eventId",
    "username",
    "sampleField",
    "NestedList"
  ],
  "properties": {
    "eventId": {
      "type": "string"
    },
    "username": {
      "type": "string"
    },
    "sampleField": {
      "type": "object",
      "required": [
        "NestedField",
        "NestedList"
      ],
      "properties": {
        "NestedField": {
          "type": "object",
          "required": [
            "max_length",
            "min_length",
            "pattern"
          ],
          "properties": {
            "max_length": {
              "type": "integer"
            },
            "min_length": {
              "type": "integer"
            },
            "pattern": {
              "type": "string"
            }
          },
          "additionalProperties": False
        },
        "NestedList": {
          "type": "array",
          "items": {
            "$ref": "#/$defs/userItem"
          }
        }
      },
      "additionalProperties": False
    },
    "NestedList": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/userItem"
      }
    }
  },
  "additionalProperties": False,
  "$defs": {
    "userItem": {
      "type": "object",
      "required": [
        "first_name",
        "age",
        "email"
      ],
      "properties": {
        "first_name": {
          "type": "string"
        },
        "age": {
          "type": "integer"
        },
        "email": {
          "type": "string",
          "format": "email"
        }
      },
      "additionalProperties": False
    }
  }
}


def benchmark_approach_1():

    try:
        # Attempt to import the package
        import jsonschema
    except ModuleNotFoundError:
        # Package is missing, install it using pip
        print("Package not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "jsonschema"])

        # Import the package again after successful installation
        import jsonschema

    print("Benchmarking JsonDictValidator:")
    execution_time = timeit.timeit(
        stmt="validator.validate(SAMPLE_JSON_PAYLOAD)",
        number=1000,
        globals={"validator": TestSchemaForJsonDictValidator(), "SAMPLE_JSON_PAYLOAD": SAMPLE_JSON_PAYLOAD}
    )

    print(f"\t - Time taken for validation (1000 runs): {execution_time:.6f} seconds")

    # Benchmarking jsonschema
    print("Benchmarking jsonschema:")
    
    validator = jsonschema.Draft7Validator(test_schema_for_jsonschema)
    execution_time = timeit.timeit(
        stmt="validator.validate(SAMPLE_JSON_PAYLOAD)",
        number=1000,
        globals={"validator": validator, "SAMPLE_JSON_PAYLOAD": SAMPLE_JSON_PAYLOAD}
    )
    print(f"\t - Time taken for validation (1000 runs): {execution_time:.6f} seconds")

def benchmark_approach_2():

    import tracemalloc

    try:
        # Attempt to import the package
        import jsonschema
    except ModuleNotFoundError:
        # Package is missing, install it using pip
        print("Package not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "jsonschema"])

        # Import the package again after successful installation
        import jsonschema

    def validation_with_json_dict_validator(data):
        validator = TestSchemaForJsonDictValidator()
        validator.validate(data)

    def validation_with_jsonschema(data):
        validator = jsonschema.Draft7Validator(test_schema_for_jsonschema)
        validator.validate(data)

    # evaluation function to benchmark and compare the two approaches
    def evaluate_functions(function_list, test_input, iterations=1000):
        print(f"--- Benchmarking Report (Input: {test_input} | Iterations: {iterations:,}) ---")
        print(f"{'Function Name':<25} | {'Status':<8} | {'Avg Time (ms)':<15} | {'Peak Memory (KB)':<16}")
        print("-" * 75)
        
        # Store the result of the first function to serve as the baseline ground-truth
        baseline_result = None
        
        for index, func in enumerate(function_list):
            func_name = func.__name__
            
            # 1. Functional Correctness Check
            try:
                current_result = func(test_input)
                if index == 0:
                    baseline_result = current_result
                    status = "PASS"
                else:
                    status = "PASS" if current_result == baseline_result else "FAIL"
            except Exception as e:
                print(f"{func_name:<25} | ERROR    | Code execution failed: {e}")
                continue

            # 2. Memory Footprint Tracking
            tracemalloc.start()
            func(test_input)
            _, peak_memory = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            peak_memory_kb = peak_memory / 1024

            # 3. Execution Time Benchmarking
            execution_time = timeit.timeit(
                stmt=f"{func_name}(test_input)",
                number=iterations,
                globals={func_name: func, "test_input": test_input}
            )

            print(f"{func_name:<25} | {status:<8} | {execution_time:<15.6f} | {peak_memory_kb:<16.4f}")

    # Target workload configurations
    functions_to_compare = [validation_with_json_dict_validator, validation_with_jsonschema]
    sample_input = SAMPLE_JSON_PAYLOAD
    total_runs = 1000

    # Execute the analysis
    evaluate_functions(functions_to_compare, sample_input, iterations=total_runs)


if __name__ == "__main__":
    # Benchmarking JsonDictValidator

    import argparse

    parser = argparse.ArgumentParser(description="Executes the comparative benchmarking.")
    parser.add_argument("-a1", "--approach_1", action="store_true", help="Run Benchmarking Approach 1")
    parser.add_argument("-a2", "--approach_2", action="store_true", help="Run Benchmarking Approach 2")
    args = parser.parse_args()

    if args.approach_1:
        benchmark_approach_1()  # Run the first benchmarking approach
    if args.approach_2:
        benchmark_approach_2()  # Run the second benchmarking approach

    print("\nBenchmarking completed.")
    ...
    # Script Run : python3 comparative_with_timeit.py
    