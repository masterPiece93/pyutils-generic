# Benchmarks

Performance benchmarks for `pyutils` modules, comparing them against popular
peer libraries.

## Layout

```
benchmarks/
├── requirements-compare.txt   # peer libraries being compared against
├── requirements-bench.txt     # measurement / plotting harness only
└── schema_json_dict_validator/
    ├── payloads.py            # payload + schema factories (flat / nested / list)
    ├── adapters.py            # uniform validate(payload) wrappers per library
    ├── bench_pyperf.py        # steady-state comparison at fixed sizes
    ├── bench_perfplot_size.py # scaling curves (time vs payload size)
    └── perfplot_size.png      # output of bench_perfplot_size
```

Requirements are intentionally split so it's obvious which dependencies exist
for *what is being measured* vs *how it is measured*.

## Setup

Install both requirement sets into the project's virtualenv:

```bash
./.venv/bin/pip install -r benchmarks/requirements-compare.txt \
                       -r benchmarks/requirements-bench.txt
```

You can install just one set if you only need part of the pipeline:

| File | Contains | Needed for |
|---|---|---|
| `requirements-compare.txt` | `fastjsonschema`, `jsonschema`, `cerberus`, `voluptuous`, `pydantic`, `msgspec` | building the adapters |
| `requirements-bench.txt` | `pyperf`, `perfplot`, `matplotlib`, `numpy` | running the benchmark scripts |

---

## `schema_json_dict_validator`

Benchmarks `pyutils.schema.JsonDictValidator` against six peers on three
payload shapes:

- **flat** — dict of `n` string fields
- **nested** — dict wrapping one nested dict of `n` int fields
- **list of dicts** — dict wrapping a list of `n` `{id, name}` items

All adapters build their schema/model **once** in `__init__`; only
`validate(payload)` is timed. `JsonDictValidatorAdapter` `deepcopy`s the
payload inside `validate` because `JsonDictValidator.validate` mutates its
input (fills defaults, applies formatters).

### 1. Steady-state comparison — `bench_pyperf.py`

Runs 7 validators × 3 shapes = **21 benchmarks** at fixed sizes.
Defaults to `--quiet`; pass `-v` for verbose pyperf output.

#### Quick smoke check (seconds)

```bash
./.venv/bin/python -m benchmarks.schema_json_dict_validator.bench_pyperf --fast
```

#### Full run (minutes; publishable numbers)

```bash
./.venv/bin/python -m benchmarks.schema_json_dict_validator.bench_pyperf \
    -o benchmarks/schema_json_dict_validator/results.json
```

#### Reduce jitter (recommended for the full run)

```bash
sudo ./.venv/bin/python -m pyperf system tune           # enable perf tuning
# ... run the benchmark ...
sudo ./.venv/bin/python -m pyperf system reset          # undo tuning
```

#### Inspect saved results

```bash
./.venv/bin/python -m pyperf stats results.json         # summary statistics
./.venv/bin/python -m pyperf dump  results.json         # raw runs / values
./.venv/bin/python -m pyperf hist  results.json         # ASCII histogram
```

#### Compare two runs (regression detection across commits)

```bash
./.venv/bin/python -m pyperf compare_to baseline.json results.json
```

#### Useful pyperf flags

| Flag | Effect |
|---|---|
| `--fast` | fewer runs / values — smoke test only |
| `--rigorous` | more runs — for the most stable numbers |
| `-p N` `-n N` `-l N` | processes / values-per-process / loops-per-value |
| `-o FILE` | write results as JSON |
| `--append FILE` | append to an existing results file |
| `-v` / `--verbose` | re-enable the "unstable result" warnings |

### 2. Scaling curves — `bench_perfplot_size.py`

Log-log plot of validation time vs list size. Writes
`perfplot_size.png` next to the script and, with `--show`, opens an
interactive matplotlib window.

```bash
./.venv/bin/python -m benchmarks.schema_json_dict_validator.bench_perfplot_size
./.venv/bin/python -m benchmarks.schema_json_dict_validator.bench_perfplot_size --show
./.venv/bin/python -m benchmarks.schema_json_dict_validator.bench_perfplot_size --max-exp 8
```

`--max-exp K` sweeps `n = 2**1 .. 2**K` (default 12).

---

## Tips

- Close other CPU-heavy apps (browser, IDE indexers) before a real run.
- Prefer `pyperf` for single-point numbers, `perfplot` for scaling curves.
- If you get the "not enough samples" warning, either pass `--rigorous`
  or increase `-p` / `-n` / `-l`. The default `bench_pyperf.py` output
  hides that warning; use `-v` to see it again.
- Fair comparisons require **building schemas once** — always keep
  compilation outside the timed function.
