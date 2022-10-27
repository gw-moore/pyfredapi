# Contributing to pyfredapi

Thank you for your interest in contributing to pyfredapi! There are many ways you can help:

- Reporting a bug
- Submitting a fix
- Adding/Proposing new features

## Report bugs

Report a bug by [opening a new issue](https://github.com/gw-moore/pyfredapi/issues/new/choose).

## How to Contribute code to pyfredapi

  1. Fork the repo
  2. Clone your fork of the repo
  3. Create a branch from `main`
  4. Install the project dependency with [poetry](https://python-poetry.org/)

```bash
poetry install --with docs,test,lint
```

  5. If you've added changed the API...
      - Add or update tests
      - Add or update documentation
  6. Ensure the test and lint suites pass with tox. From the root of the project directory, run:

```bash
tox
```

  7. Submit a pull request (PR)
