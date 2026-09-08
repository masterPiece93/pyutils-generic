# Contributing to `pyutils_generic`

Thanks for your interest in contributing! 🙏

## Development setup

```bash
git clone https://github.com/masterPiece93/pyutils-generic.git
cd pyutils-generic

python3 -m venv .venv
source .venv/bin/activate

pip install -e ".[dev]"
```

## Running tests

```bash
python -m unittest discover -s pyutils_generic/tests -p 'test_*.py' -v
```

With coverage:

```bash
python -m coverage run -m unittest discover -s pyutils_generic/tests -p 'test_*.py'
python -m coverage report
```

## Linting

```bash
pylint pyutils_generic --fail-under=9.0
```

## Building the package

```bash
python -m build
check-wheel-contents dist/*.whl
```

## Pull requests

- Keep each PR focused on a single logical change.
- Add/update tests covering your change.
- Update `CHANGELOG.md` under `[Unreleased]` for user-facing changes.
- Update documentation under `docs/` and the relevant sections of `README.md`.
- Ensure `pylint` and the test suite pass locally.

## Release process (maintainers)

1. Bump `version` in `pyproject.toml` and `pyutils_generic/__init__.py`.
2. Move `[Unreleased]` entries in `CHANGELOG.md` under the new version heading.
3. Commit, tag `vX.Y.Z`, and push.
4. Create a GitHub Release from the tag — this triggers the
   [`release.yml`](.github/workflows/release.yml) workflow which builds and
   publishes to PyPI via trusted publishing.
