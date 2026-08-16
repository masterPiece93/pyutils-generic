"""
Unit tests for `schema.py`.

Covers:
    * ValidatorMeta metaclass rules (abstract `validate`, read-only class vars)
    * DictValidator._check_specification for every validation branch
    * Required / optional keys, defaults, type checks
    * Nested dict and nested list-of-dicts constraints
    * Extra key handling (allowed / not allowed)
    * Formatter application
    * The end-to-end IngestionMessage example flow

Run with the project virtual environment:
    ./.venv/bin/python -m unittest -v pyutils.tests.test_dict_validator
"""
import unittest
from typing import ClassVar

from pyutils.schema import DictValidator, ValidatorMeta


def make_validator(spec, allow_extra=False, formatters=None):
    """Helper to build a concrete DictValidator subclass on the fly."""
    namespace = {
        "VALIDATION_SPECIFICATION": spec,
        "ALLOWED_EXTRA_KEYS": allow_extra,
        "FORMATTERS": formatters or {},
        "validate": lambda self, json_payload: DictValidator.validate(
            self, json_payload, logger=lambda m, level: None, message_wrapper=lambda m: m
        ),
    }
    cls = ValidatorMeta("TmpValidator", (DictValidator,), namespace)
    return cls


class TestValidatorMeta(unittest.TestCase):
    """Tests for the metaclass rules."""

    def test_missing_validate_raises(self):
        with self.assertRaises(TypeError):
            ValidatorMeta("NoValidate", (), {})

    def test_classmethod_validate_raises(self):
        with self.assertRaises(TypeError):
            ValidatorMeta("Cm", (), {"validate": classmethod(lambda cls: None)})

    def test_staticmethod_validate_raises(self):
        with self.assertRaises(TypeError):
            ValidatorMeta("Sm", (), {"validate": staticmethod(lambda: None)})

    def test_instance_method_validate_ok(self):
        cls = ValidatorMeta("Ok", (), {"validate": lambda self: None})
        self.assertTrue(hasattr(cls, "validate"))

    def test_class_variables_are_read_only(self):
        cls = make_validator({"a": (True, str, None)})
        with self.assertRaises(AttributeError):
            cls.ALLOWED_EXTRA_KEYS = True

    def test_read_only_error_message(self):
        cls = make_validator({"a": (True, str, None)})
        try:
            cls.ALLOWED_EXTRA_KEYS = True
        except AttributeError as e:
            self.assertIn("Cannot modify constant 'ALLOWED_EXTRA_KEYS'", str(e))

    def test_setting_new_class_attribute_is_allowed(self):
        cls = make_validator({"a": (True, str, None)})
        cls.SOME_NEW_ATTR = 123
        self.assertEqual(cls.SOME_NEW_ATTR, 123)


class TestLoggingBranches(unittest.TestCase):
    """Tests exercising the print-based logging fallback."""

    def test_validate_without_logger_uses_print(self):
        Validator = ValidatorMeta("PrintValidator", (DictValidator,), {
            "VALIDATION_SPECIFICATION": {"name": (True, str, None)},
            "ALLOWED_EXTRA_KEYS": False,
            "FORMATTERS": {},
            "validate": lambda self, json_payload: DictValidator.validate(self, json_payload),
        })
        import io
        from contextlib import redirect_stdout
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            with self.assertRaises(DictValidator.SchemaViolation):
                Validator().validate({"name": 123})
        self.assertIn("ERROR", buffer.getvalue())


class TestBasicValidation(unittest.TestCase):
    """Tests for the top-level payload validation."""

    def setUp(self):
        self.Validator = make_validator({
            "name": (True, str, None),
            "age": (True, int, None),
        })

    def test_valid_payload_passes(self):
        payload = {"name": "alice", "age": 30}
        self.Validator().validate(payload)

    def test_non_dict_payload_raises(self):
        with self.assertRaises(DictValidator.SchemaViolation):
            self.Validator().validate(["not", "a", "dict"])

    def test_empty_payload_raises(self):
        with self.assertRaises(DictValidator.SchemaViolation):
            self.Validator().validate({})

    def test_missing_required_key_raises(self):
        with self.assertRaises(DictValidator.SchemaViolation):
            self.Validator().validate({"name": "alice"})

    def test_wrong_type_raises(self):
        with self.assertRaises(DictValidator.SchemaViolation):
            self.Validator().validate({"name": "alice", "age": "thirty"})


class TestOptionalKeysAndDefaults(unittest.TestCase):
    """Tests for optional keys and default value population."""

    def test_optional_key_gets_default(self):
        Validator = make_validator({
            "name": (True, str, None),
            "nickname": (False, str, "n/a"),
        })
        payload = {"name": "alice"}
        Validator().validate(payload)
        self.assertEqual(payload["nickname"], "n/a")

    def test_provided_optional_key_is_kept(self):
        Validator = make_validator({
            "name": (True, str, None),
            "nickname": (False, str, "n/a"),
        })
        payload = {"name": "alice", "nickname": "ally"}
        Validator().validate(payload)
        self.assertEqual(payload["nickname"], "ally")


class TestExtraKeys(unittest.TestCase):
    """Tests for extra key handling."""

    def test_extra_key_not_allowed_raises(self):
        Validator = make_validator({"name": (True, str, None)}, allow_extra=False)
        with self.assertRaises(DictValidator.SchemaViolation):
            Validator().validate({"name": "alice", "extra": "boom"})

    def test_extra_key_allowed_passes(self):
        Validator = make_validator({"name": (True, str, None)}, allow_extra=True)
        payload = {"name": "alice", "extra": "ok"}
        Validator().validate(payload)
        self.assertEqual(payload["extra"], "ok")


class TestNestedDict(unittest.TestCase):
    """Tests for nested dict constraints."""

    def setUp(self):
        self.Validator = make_validator({
            "meta": (True, dict, None, {
                "count": (True, int, None),
                "label": (False, str, "default_label"),
            }),
        })

    def test_valid_nested_dict_passes(self):
        payload = {"meta": {"count": 5}}
        self.Validator().validate(payload)
        self.assertEqual(payload["meta"]["label"], "default_label")

    def test_empty_nested_dict_raises(self):
        with self.assertRaises(DictValidator.SchemaViolation):
            self.Validator().validate({"meta": {}})

    def test_nested_required_key_missing_raises(self):
        with self.assertRaises(DictValidator.SchemaViolation):
            self.Validator().validate({"meta": {"label": "x"}})

    def test_nested_wrong_type_raises(self):
        with self.assertRaises(DictValidator.SchemaViolation):
            self.Validator().validate({"meta": {"count": "five"}})


class TestNestedListOfDicts(unittest.TestCase):
    """Tests for nested list-of-dicts constraints."""

    def setUp(self):
        self.Validator = make_validator({
            "users": (True, list, None, [{
                "first_name": (True, str, None),
                "age": (True, int, None),
                "email": (False, str, ""),
            }]),
        })

    def test_valid_list_of_dicts_passes(self):
        payload = {"users": [
            {"first_name": "ann", "age": 20},
            {"first_name": "bob", "age": 25, "email": "bob@x.com"},
        ]}
        self.Validator().validate(payload)
        self.assertEqual(payload["users"][0]["email"], "")

    def test_list_item_not_dict_raises(self):
        with self.assertRaises(DictValidator.SchemaViolation):
            self.Validator().validate({"users": ["not_a_dict"]})

    def test_list_item_missing_required_raises(self):
        with self.assertRaises(DictValidator.SchemaViolation):
            self.Validator().validate({"users": [{"first_name": "ann"}]})

    def test_list_item_wrong_type_raises(self):
        with self.assertRaises(DictValidator.SchemaViolation):
            self.Validator().validate({"users": [{"first_name": "ann", "age": "old"}]})


class TestFormatters(unittest.TestCase):
    """Tests for formatter application on the last processed key."""

    def test_formatter_applied_on_last_key(self):
        Validator = make_validator(
            {"url": (True, str, None)},
            formatters={"url": lambda v: v.lstrip("/")},
        )
        payload = {"url": "/path/"}
        Validator().validate(payload)
        self.assertEqual(payload["url"], "path/")


class TestIngestionMessageExample(unittest.TestCase):
    """End-to-end test mirroring the documented example."""

    def _build_message_class(self):
        class IngestionMessage(DictValidator):
            VALIDATION_SPECIFICATION: ClassVar[dict] = {
                "eventId": (True, str, None),
                "username": (True, str, None),
                "url": (True, str, None),
                "orgId": (True, str, None),
                "tenancy": (True, str, None),
                "orgName": (True, dict, None, {
                    "max_length": (False, int, 100),
                    "min_length": (False, int, 0),
                    "pattern": (False, str, r"^[a-zA-Z0-9_]+$"),
                }),
                "user": (True, list, None, [{
                    "first_name": (True, str, None),
                    "age": (True, int, None),
                    "email": (False, str, ""),
                }]),
            }
            ALLOWED_EXTRA_KEYS: ClassVar[bool] = False
            FORMATTERS: ClassVar[dict] = {"url": lambda value: value.lstrip("/")}

            def validate(self, json_payload: dict, message_id: str) -> None:
                _logger = lambda m, level: None
                _message_wrapper = lambda log_msg: f"[{message_id}] {log_msg}"
                super().validate(json_payload, logger=_logger, message_wrapper=_message_wrapper)

        return IngestionMessage

    def _valid_payload(self):
        return {
            "eventId": "e1",
            "username": "u1",
            "url": "/path/",
            "orgId": "o1",
            "tenancy": "t1",
            "orgName": {"max_length": 100},
            "user": [
                {"first_name": "ankit", "age": 33},
                {"first_name": "john_doe", "age": 28, "email": "john@example.com"},
            ],
        }

    def test_valid_message_passes_and_populates_defaults(self):
        IngestionMessage = self._build_message_class()
        data = self._valid_payload()
        IngestionMessage().validate(data, "187129034567124876")
        self.assertEqual(data["orgName"]["min_length"], 0)
        self.assertEqual(data["orgName"]["pattern"], r"^[a-zA-Z0-9_]+$")
        self.assertEqual(data["user"][0]["email"], "")

    def test_read_only_class_var_on_subclass(self):
        IngestionMessage = self._build_message_class()
        with self.assertRaises(AttributeError):
            IngestionMessage.ALLOWED_EXTRA_KEYS = True

    def test_extra_top_level_key_raises(self):
        IngestionMessage = self._build_message_class()
        data = self._valid_payload()
        data["channel"] = "extra"
        with self.assertRaises(DictValidator.SchemaViolation):
            IngestionMessage().validate(data, "187129034567124876")

    def test_missing_required_top_level_key_raises(self):
        IngestionMessage = self._build_message_class()
        data = self._valid_payload()
        del data["eventId"]
        with self.assertRaises(DictValidator.SchemaViolation):
            IngestionMessage().validate(data, "187129034567124876")


if __name__ == "__main__":
    unittest.main(verbosity=2)
