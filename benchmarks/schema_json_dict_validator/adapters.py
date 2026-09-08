"""
Adapters that wrap each validator behind a uniform interface:

    adapter = SomeAdapter(schema_or_spec)
    adapter.validate(payload)   # called in the hot loop

The schema / model / struct is built ONCE in __init__ so the timed call
represents steady-state validation only (mirroring real-world usage where
schemas are compiled at startup).
"""
from __future__ import annotations

import copy
from typing import Any, Callable

import fastjsonschema
import jsonschema
import msgspec
from cerberus import Validator as _CerberusValidator
from pydantic import BaseModel

from pyutils_generic.schema import JsonDictValidator, ValidatorMeta


# ---------------------------------------------------------------------------
# JsonDictValidator (this project)
# ---------------------------------------------------------------------------
class JsonDictValidatorAdapter:
    """Adapter around pyutils.schema.JsonDictValidator.

    NB: JsonDictValidator.validate MUTATES the payload (fills defaults,
    applies formatters, sets extras). To keep every timed call doing the
    same work we deepcopy the payload inside `validate`. This charges our
    validator with copy cost that the other libraries don't pay - it is
    the honest apples-to-apples baseline for a validator with in-place
    mutation semantics.
    """

    name = "JsonDictValidator"

    def __init__(self, spec: dict, allow_extra: bool = False, formatters: dict | None = None):
        _noop_logger: Callable[[str, str], None] = lambda m, level: None

        def _validate(self, json_payload: dict) -> None:
            JsonDictValidator.validate(self, json_payload, logger=_noop_logger)

        cls = ValidatorMeta(
            "BenchJsonDictValidator",
            (JsonDictValidator,),
            {
                "VALIDATION_SPECIFICATION": spec,
                "ALLOWED_EXTRA_KEYS": allow_extra,
                "FORMATTERS": formatters or {},
                "validate": _validate,
            },
        )
        self._instance = cls()

    def validate(self, payload: dict) -> Any:
        return self._instance.validate(copy.deepcopy(payload))


# ---------------------------------------------------------------------------
# fastjsonschema (compiles schema -> Python function)
# ---------------------------------------------------------------------------
class FastJsonSchemaAdapter:
    name = "fastjsonschema"

    def __init__(self, json_schema: dict):
        self._validate = fastjsonschema.compile(json_schema)

    def validate(self, payload: dict) -> Any:
        return self._validate(payload)


# ---------------------------------------------------------------------------
# jsonschema (reference implementation)
# ---------------------------------------------------------------------------
class JsonSchemaAdapter:
    name = "jsonschema"

    def __init__(self, json_schema: dict):
        self._validator = jsonschema.Draft202012Validator(json_schema)

    def validate(self, payload: dict) -> Any:
        return self._validator.validate(payload)


# ---------------------------------------------------------------------------
# cerberus
# ---------------------------------------------------------------------------
class CerberusAdapter:
    name = "cerberus"

    def __init__(self, cerberus_schema: dict):
        self._validator = _CerberusValidator(cerberus_schema, require_all=True)

    def validate(self, payload: dict) -> Any:
        # Cerberus returns False on failure rather than raising; convert to
        # a raise so the failure path is comparable across adapters.
        if not self._validator.validate(payload):
            raise ValueError(self._validator.errors)


# ---------------------------------------------------------------------------
# voluptuous
# ---------------------------------------------------------------------------
class VoluptuousAdapter:
    name = "voluptuous"

    def __init__(self, voluptuous_schema):
        self._schema = voluptuous_schema

    def validate(self, payload: dict) -> Any:
        return self._schema(payload)


# ---------------------------------------------------------------------------
# pydantic v2
# ---------------------------------------------------------------------------
class PydanticAdapter:
    name = "pydantic_v2"

    def __init__(self, model: type[BaseModel]):
        self._model = model

    def validate(self, payload: dict) -> Any:
        return self._model.model_validate(payload)


# ---------------------------------------------------------------------------
# msgspec
# ---------------------------------------------------------------------------
class MsgspecAdapter:
    name = "msgspec"

    def __init__(self, struct: type[msgspec.Struct]):
        self._struct = struct

    def validate(self, payload: dict) -> Any:
        return msgspec.convert(payload, self._struct)
