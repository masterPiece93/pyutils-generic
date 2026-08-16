"""
Unit tests for `pyutils.typecheck`.

Covers:
    * strict decorator (argument / return type enforcement)
    * ArgumentTypeError / ReturnTypeError messages
    * TypeCheck field validators (default + custom exceptions)
    * TypeCheck custom `type_exception`
    * CoercedType coercion and its error branches
"""
import dataclasses
import unittest

from pyutils.typecheck import (
    strict,
    TypeCheck,
    CoercedType,
    ArgumentTypeError,
    ReturnTypeError,
)


class TestStrictDecorator(unittest.TestCase):
    """Tests for the `strict` decorator."""

    def test_valid_call_passes(self):
        @strict
        def add(a: int, b: int) -> int:
            return a + b

        self.assertEqual(add(2, 3), 5)

    def test_wrong_argument_type_raises(self):
        @strict
        def add(a: int, b: int) -> int:
            return a + b

        with self.assertRaises(ArgumentTypeError):
            add("2", 3)

    def test_wrong_return_type_raises(self):
        @strict
        def bad_return(a: int) -> int:
            return "not an int"

        with self.assertRaises(ReturnTypeError):
            bad_return(1)

    def test_unannotated_argument_is_skipped(self):
        # `b` has no annotation -> the KeyError branch is exercised.
        @strict
        def mixed(a: int, b) -> int:
            return a

        self.assertEqual(mixed(1, "anything"), 1)

    def test_missing_return_annotation_is_allowed(self):
        @strict
        def no_return_hint(a: int):
            return "whatever"

        self.assertEqual(no_return_hint(1), "whatever")

    def test_argument_type_error_message(self):
        err = ArgumentTypeError("fn", "a", int, str)
        self.assertIn("Argument `a`", str(err))
        self.assertIn("fn", str(err))

    def test_return_type_error_message(self):
        err = ReturnTypeError("fn", int, str)
        self.assertIn("Return Value", str(err))
        self.assertIn("fn", str(err))


class TestTypeCheckBuiltins(unittest.TestCase):
    """Tests for builtin-type checking in TypeCheck."""

    def test_valid_builtin_passes(self):
        @dataclasses.dataclass(frozen=True)
        class Person(TypeCheck):
            name: str
            age: int

        p = Person(name="alice", age=30)
        self.assertEqual(p.name, "alice")

    def test_wrong_builtin_type_raises(self):
        @dataclasses.dataclass(frozen=True)
        class Person(TypeCheck):
            name: str
            age: int

        with self.assertRaises(TypeError):
            Person(name="alice", age="thirty")


class TestTypeCheckValidators(unittest.TestCase):
    """Tests for the field `*_validator` mechanism."""

    def test_validator_failure_raises_value_error(self):
        @dataclasses.dataclass(frozen=True)
        class Person(TypeCheck):
            age: int

            def age_validator(value):
                return value >= 0

        with self.assertRaises(ValueError):
            Person(age=-1)

    def test_validator_success_passes(self):
        @dataclasses.dataclass(frozen=True)
        class Person(TypeCheck):
            age: int

            def age_validator(value):
                return value >= 0

        self.assertEqual(Person(age=10).age, 10)

    def test_custom_validator_exception_is_raised(self):
        class MyValidationError(Exception):
            def __init__(self, param, value, validator_name):
                super().__init__(f"{param}={value} failed {validator_name}")

        @dataclasses.dataclass(frozen=True)
        class Person(TypeCheck):
            age: int

            def age_validator(value):
                return value >= 0

            validator_exception = MyValidationError

        with self.assertRaises(MyValidationError):
            Person(age=-5)


class TestTypeCheckCustomTypeException(unittest.TestCase):
    """Tests for the custom `type_exception` mechanism."""

    def test_custom_type_exception_is_raised(self):
        class MyTypeError(TypeError):
            def __init__(self, name, current_type, field_type):
                super().__init__(f"{name}: {current_type} != {field_type}")

        @dataclasses.dataclass(frozen=True)
        class Person(TypeCheck):
            age: int

            type_exception = MyTypeError

        with self.assertRaises(MyTypeError):
            Person(age="not-an-int")


class TestCoercedType(unittest.TestCase):
    """Tests for CoercedType coercion and its error branches."""

    def test_successful_coercion(self):
        @dataclasses.dataclass(frozen=True)
        class ToInt(CoercedType):
            value: int
            coercion: dict

        result = ToInt(value="5", coercion={str: int})
        self.assertEqual(result.value, 5)
        self.assertEqual(str(result), "5")

    def test_missing_mandatory_key_raises(self):
        @dataclasses.dataclass(frozen=True)
        class MissingCoercion(CoercedType):
            value: int

        with self.assertRaises(CoercedType.MandatoryKeyMissingError):
            MissingCoercion(value=1)

    def test_extra_annotation_raises(self):
        @dataclasses.dataclass(frozen=True)
        class Extra(CoercedType):
            value: int
            coercion: dict
            extra: str

        with self.assertRaises(Exception):
            Extra(value="5", coercion={str: int}, extra="boom")

    def test_value_annotated_non_builtin_raises(self):
        class NotBuiltin:
            pass

        @dataclasses.dataclass(frozen=True)
        class BadValue(CoercedType):
            value: NotBuiltin
            coercion: dict

        with self.assertRaises(CoercedType.AnnotationTypeError):
            BadValue(value=NotBuiltin(), coercion={})

    def test_coercion_annotated_non_dict_raises(self):
        @dataclasses.dataclass(frozen=True)
        class BadCoercion(CoercedType):
            value: int
            coercion: list

        with self.assertRaises(CoercedType.AnnotationTypeError):
            BadCoercion(value="5", coercion=[])

    def test_value_type_not_coercible_raises(self):
        @dataclasses.dataclass(frozen=True)
        class ToInt(CoercedType):
            value: int
            coercion: dict

        # float is not a key in the coercion map -> CoersionError
        with self.assertRaises(CoercedType.CoersionError):
            ToInt(value=5.0, coercion={str: int})

    def test_coerced_to_wrong_type_raises(self):
        @dataclasses.dataclass(frozen=True)
        class ToInt(CoercedType):
            value: int
            coercion: dict

        # "5" coerces to float, but the annotation demands int -> CoersionError
        with self.assertRaises(CoercedType.CoersionError):
            ToInt(value="5", coercion={str: float})


if __name__ == "__main__":
    unittest.main(verbosity=2)
