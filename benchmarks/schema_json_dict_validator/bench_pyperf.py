"""
Steady-state comparison with pyperf.

Compares JsonDictValidator against fastjsonschema, jsonschema, cerberus,
voluptuous, pydantic v2, and msgspec on three payload shapes at fixed sizes.

Run:
    ./.venv/bin/python -m benchmarks.schema_json_dict_validator.bench_pyperf \\
        -o benchmarks/schema_json_dict_validator/results.json

    # Quick smoke check:
    ./.venv/bin/python -m benchmarks.schema_json_dict_validator.bench_pyperf \\
        --fast --worker

    # Compare two runs:
    ./.venv/bin/python -m pyperf compare_to baseline.json results.json
"""
from __future__ import annotations

import sys

import pyperf

from benchmarks.schema_json_dict_validator import payloads as p
from benchmarks.schema_json_dict_validator.adapters import (
    JsonDictValidatorAdapter,
    FastJsonSchemaAdapter,
    JsonSchemaAdapter,
    CerberusAdapter,
    VoluptuousAdapter,
    PydanticAdapter,
    MsgspecAdapter,
)


# Fixed sizes for steady-state comparison.
FLAT_N = 10
NESTED_N = 10
LIST_N = 100


def _build_flat_adapters():
    return [
        JsonDictValidatorAdapter(p.flat_jdv_spec(FLAT_N)),
        FastJsonSchemaAdapter(p.flat_json_schema(FLAT_N)),
        JsonSchemaAdapter(p.flat_json_schema(FLAT_N)),
        CerberusAdapter(p.flat_cerberus_schema(FLAT_N)),
        VoluptuousAdapter(p.flat_voluptuous_schema(FLAT_N)),
        PydanticAdapter(p.flat_pydantic_model(FLAT_N)),
        MsgspecAdapter(p.flat_msgspec_struct(FLAT_N)),
    ]


def _build_nested_adapters():
    return [
        JsonDictValidatorAdapter(p.nested_jdv_spec(NESTED_N)),
        FastJsonSchemaAdapter(p.nested_json_schema(NESTED_N)),
        JsonSchemaAdapter(p.nested_json_schema(NESTED_N)),
        CerberusAdapter(p.nested_cerberus_schema(NESTED_N)),
        VoluptuousAdapter(p.nested_voluptuous_schema(NESTED_N)),
        PydanticAdapter(p.nested_pydantic_model(NESTED_N)),
        MsgspecAdapter(p.nested_msgspec_struct(NESTED_N)),
    ]


def _build_list_adapters():
    return [
        JsonDictValidatorAdapter(p.list_jdv_spec()),
        FastJsonSchemaAdapter(p.list_json_schema()),
        JsonSchemaAdapter(p.list_json_schema()),
        CerberusAdapter(p.list_cerberus_schema()),
        VoluptuousAdapter(p.list_voluptuous_schema()),
        PydanticAdapter(p.list_pydantic_model()),
        MsgspecAdapter(p.list_msgspec_struct()),
    ]


def main() -> None:
    # Default to `--quiet` so the "unstable result" warnings don't drown out
    # the numbers. Users can still opt-in to the verbose pyperf output with
    # `-v` / `--verbose`.
    _flags = set(sys.argv[1:])
    if not (_flags & {"-q", "--quiet", "-v", "--verbose"}):
        sys.argv.insert(1, "--quiet")

    runner = pyperf.Runner()

    # ---- flat ----
    flat_payload = p.make_flat_payload(FLAT_N)
    for adapter in _build_flat_adapters():
        runner.bench_func(f"flat[{FLAT_N}]/{adapter.name}", adapter.validate, flat_payload)

    # ---- nested ----
    nested_payload = p.make_nested_payload(NESTED_N)
    for adapter in _build_nested_adapters():
        runner.bench_func(f"nested[{NESTED_N}]/{adapter.name}", adapter.validate, nested_payload)

    # ---- list of dicts ----
    list_payload = p.make_list_payload(LIST_N)
    for adapter in _build_list_adapters():
        runner.bench_func(f"list[{LIST_N}]/{adapter.name}", adapter.validate, list_payload)


if __name__ == "__main__":
    main()
