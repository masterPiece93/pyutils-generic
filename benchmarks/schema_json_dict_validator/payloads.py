"""
Payload / schema factories for benchmarking.

Every factory is parameterised by `n` so that harnesses like `perfplot`
can sweep it. Three shapes are provided:

* `flat`         - a flat dict of `n` string fields
* `nested`       - a dict wrapping a single nested dict of `n` int fields
* `list_of_dicts`- a dict wrapping a list of `n` small item dicts

For every shape we expose:

* a JsonDictValidator VALIDATION_SPECIFICATION
* a JSON Schema (Draft 2020-12) - shared by jsonschema / fastjsonschema
* a Cerberus schema
* a Voluptuous schema
* a pydantic v2 model
* a msgspec.Struct
* a payload factory `make_<shape>_payload(n)`
"""
from __future__ import annotations

from typing import Any, List

from pydantic import BaseModel, ConfigDict
from voluptuous import Schema, Required, ALLOW_EXTRA, PREVENT_EXTRA
import msgspec


# ---------------------------------------------------------------------------
# 1. Flat payload : {"f0": "v0", "f1": "v1", ...}
# ---------------------------------------------------------------------------

def make_flat_payload(n: int) -> dict:
    return {f"f{i}": f"v{i}" for i in range(n)}


def flat_jdv_spec(n: int) -> dict:
    return {f"f{i}": (True, str, None) for i in range(n)}


def flat_json_schema(n: int) -> dict:
    return {
        "type": "object",
        "properties": {f"f{i}": {"type": "string"} for i in range(n)},
        "required": [f"f{i}" for i in range(n)],
        "additionalProperties": False,
    }


def flat_cerberus_schema(n: int) -> dict:
    return {f"f{i}": {"type": "string", "required": True} for i in range(n)}


def flat_voluptuous_schema(n: int) -> Schema:
    return Schema(
        {Required(f"f{i}"): str for i in range(n)},
        extra=PREVENT_EXTRA,
    )


def flat_pydantic_model(n: int) -> type[BaseModel]:
    fields = {f"f{i}": (str, ...) for i in range(n)}
    from pydantic import create_model
    return create_model(
        f"FlatModel_{n}",
        __config__=ConfigDict(extra="forbid"),
        **fields,
    )


def flat_msgspec_struct(n: int) -> type[msgspec.Struct]:
    # msgspec.defstruct builds a Struct at runtime.
    return msgspec.defstruct(
        f"FlatStruct_{n}",
        [(f"f{i}", str) for i in range(n)],
        forbid_unknown_fields=True,
    )


# ---------------------------------------------------------------------------
# 2. Nested payload : {"meta": {"k0": 0, "k1": 1, ...}}
# ---------------------------------------------------------------------------

def make_nested_payload(n: int) -> dict:
    return {"meta": {f"k{i}": i for i in range(n)}}


def nested_jdv_spec(n: int) -> dict:
    return {
        "meta": (
            True,
            dict,
            None,
            {f"k{i}": (True, int, None) for i in range(n)},
        )
    }


def nested_json_schema(n: int) -> dict:
    return {
        "type": "object",
        "properties": {
            "meta": {
                "type": "object",
                "properties": {f"k{i}": {"type": "integer"} for i in range(n)},
                "required": [f"k{i}" for i in range(n)],
                "additionalProperties": False,
            }
        },
        "required": ["meta"],
        "additionalProperties": False,
    }


def nested_cerberus_schema(n: int) -> dict:
    return {
        "meta": {
            "type": "dict",
            "required": True,
            "schema": {f"k{i}": {"type": "integer", "required": True} for i in range(n)},
        }
    }


def nested_voluptuous_schema(n: int) -> Schema:
    return Schema(
        {Required("meta"): Schema(
            {Required(f"k{i}"): int for i in range(n)},
            extra=PREVENT_EXTRA,
        )},
        extra=PREVENT_EXTRA,
    )


def nested_pydantic_model(n: int) -> type[BaseModel]:
    from pydantic import create_model
    Meta = create_model(
        f"Meta_{n}",
        __config__=ConfigDict(extra="forbid"),
        **{f"k{i}": (int, ...) for i in range(n)},
    )
    return create_model(
        f"NestedModel_{n}",
        __config__=ConfigDict(extra="forbid"),
        meta=(Meta, ...),
    )


def nested_msgspec_struct(n: int) -> type[msgspec.Struct]:
    Meta = msgspec.defstruct(
        f"NestedMeta_{n}",
        [(f"k{i}", int) for i in range(n)],
        forbid_unknown_fields=True,
    )
    return msgspec.defstruct(
        f"NestedStruct_{n}",
        [("meta", Meta)],
        forbid_unknown_fields=True,
    )


# ---------------------------------------------------------------------------
# 3. List-of-dicts payload : {"items": [{"id": .., "name": ..}, ...]}
# ---------------------------------------------------------------------------

def make_list_payload(n: int) -> dict:
    return {"items": [{"id": i, "name": f"n{i}"} for i in range(n)]}


def list_jdv_spec() -> dict:
    return {
        "items": (
            True,
            list,
            None,
            [{
                "id":   (True, int, None),
                "name": (True, str, None),
            }],
        )
    }


def list_json_schema() -> dict:
    return {
        "type": "object",
        "properties": {
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id":   {"type": "integer"},
                        "name": {"type": "string"},
                    },
                    "required": ["id", "name"],
                    "additionalProperties": False,
                },
            }
        },
        "required": ["items"],
        "additionalProperties": False,
    }


def list_cerberus_schema() -> dict:
    return {
        "items": {
            "type": "list",
            "required": True,
            "schema": {
                "type": "dict",
                "schema": {
                    "id":   {"type": "integer", "required": True},
                    "name": {"type": "string", "required": True},
                },
            },
        }
    }


def list_voluptuous_schema() -> Schema:
    return Schema(
        {Required("items"): [Schema(
            {Required("id"): int, Required("name"): str},
            extra=PREVENT_EXTRA,
        )]},
        extra=PREVENT_EXTRA,
    )


def list_pydantic_model() -> type[BaseModel]:
    class Item(BaseModel):
        model_config = ConfigDict(extra="forbid")
        id: int
        name: str

    class ListModel(BaseModel):
        model_config = ConfigDict(extra="forbid")
        items: List[Item]

    return ListModel


def list_msgspec_struct() -> type[msgspec.Struct]:
    # Use defstruct so the item class is materialised in a stable module and
    # can be referenced directly (avoids forward-ref resolution issues that
    # trip on classes defined inside a function scope).
    Item = msgspec.defstruct(
        "ListItem",
        [("id", int), ("name", str)],
        forbid_unknown_fields=True,
    )
    return msgspec.defstruct(
        "ListStruct",
        [("items", List[Item])],
        forbid_unknown_fields=True,
    )
