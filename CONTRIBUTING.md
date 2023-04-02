# Contributing to pyfredapi

Thank you for your interest in contributing to pyfredapi! There are many ways you can help:

- Reporting a bug
- Submitting a fix
- Adding/Proposing new features

## Report bugs

Report a bug by [opening a new issue](https://github.com/gw-moore/pyfredapi/issues/new/choose).

## How to contribute code to pyfredapi

  1. Fork the repo
  2. Clone your fork of the repo
  3. Create a branch from `main`
  4. Follow the [poetry](https://python-poetry.org/) install instructions to install version 1.4.0
  5. Install the project's development dependencies with [poetry](https://python-poetry.org/)

```bash
poetry install --with docs,test,lint
```

  5. Setup pre-commit

```bash
poetry shell
pre-commit install
```

  6. If you changed the API...
      - Add or update tests
      - Add or update documentation
  7. Ensure the test and lint suites pass with tox. From the root of the project directory, run:

```bash
tox
```

  8. Ensure the documentation builds correctly. The documentation is built with sphinx.
  From the root of the project directory, run:

  ```bash
  make html -C docs/
  ```

  Then open the html docs with:

  ```bash
  open docs/_build/html/index.html
  ```

  9. Submit a pull request (PR)
