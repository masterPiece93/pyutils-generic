"""
Scaling curves with perfplot.

Sweeps the list-of-dicts payload size `n` and plots time vs `n` for every
validator adapter. Writes a PNG next to this script.

Run:
    ./.venv/bin/python -m benchmarks.schema_json_dict_validator.bench_perfplot_size
    ./.venv/bin/python -m benchmarks.schema_json_dict_validator.bench_perfplot_size --show
"""
from __future__ import annotations

import argparse
import pathlib

import perfplot

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


# Adapters for the list-of-dicts schema are shape-invariant (the schema
# describes an item, not a fixed list length), so we build them ONCE and
# reuse them across every `n` sweep step.
_ADAPTERS = [
    JsonDictValidatorAdapter(p.list_jdv_spec()),
    FastJsonSchemaAdapter(p.list_json_schema()),
    JsonSchemaAdapter(p.list_json_schema()),
    CerberusAdapter(p.list_cerberus_schema()),
    VoluptuousAdapter(p.list_voluptuous_schema()),
    PydanticAdapter(p.list_pydantic_model()),
    MsgspecAdapter(p.list_msgspec_struct()),
]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--show", action="store_true", help="also open an interactive matplotlib window")
    parser.add_argument("--max-exp", type=int, default=12, help="sweep n = 2**1 .. 2**MAX_EXP (default 12)")
    args = parser.parse_args()

    out = pathlib.Path(__file__).with_name("perfplot_size.png")

    perfplot.save(
        str(out),
        setup=p.make_list_payload,
        kernels=[a.validate for a in _ADAPTERS],
        labels=[a.name for a in _ADAPTERS],
        n_range=[2 ** k for k in range(1, args.max_exp + 1)],
        xlabel="number of items in payload",
        equality_check=None,   # different libraries return different objects
        logx=True,
        logy=True,
        show_progress=True,
    )
    print(f"Wrote {out}")

    if args.show:
        import matplotlib.pyplot as plt  # noqa: WPS433
        plt.show()


if __name__ == "__main__":
    main()
