# All packaging metadata now lives in `pyproject.toml`.
# This shim is kept only to support legacy `pip install -e .` workflows on very
# old pip versions. Modern builds use `python -m build` with the PEP 517
# backend declared in pyproject.toml.
from setuptools import setup

setup()