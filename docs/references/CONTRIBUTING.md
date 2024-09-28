# Contributing to pyfredapi

Thank you for your interest in contributing to pyfredapi! There are many ways you can help:

- Reporting a bug
- Submitting a fix
- Adding/Proposing new features

## Report bugs

Report a bug by [opening a new issue](https://github.com/gw-moore/pyfredapi/issues/new/choose).

## How to contribute to pyfredapi

Before contributing to `pyfredapi` it a good idea to create an issue to discuss the changes you would like to make. This will help ensure that your changes are accepted and merged into the project.

When you're ready contribute changes to `pyfredapi`, you will need to setup the project on your machine. The following steps will help you get started:

  1. Set your FRED API key as an environment variable. The `pyfredapi` tests require a FRED API key to run. You can set the API key as an environment variable by adding the following line to your `~/.zshrc`, `~/.bashrc` file:

```bash
export FRED_API_KEY="your_api_key"
```

  2. Fork the `pyfredapi` repo
  3. Clone your fork of the repo to your local machine
  4. Create a branch from `main`. Give your branch a descriptive name, e.g. `add-foo-feature`

Once you have completed the above steps, you need to setup your development environment. The `pyfredapi` project uses [hatch](https://github.com/pypa/hatch) to build and publish the `pyfredapi` package, so it a good idea to use `hatch` to setup your development environment.

  4. Follow the [hatch](https://hatch.pypa.io/latest/install/) install instructions.
  5. This step is a personal preference. Update the hatch config.toml to setup a python virtual environment in the project's directory. Follow the [hatch config docs](https://hatch.pypa.io/latest/config/hatch/)


  6. Create a virtual environment for the project and activate the environment

```bash
hatch env create
hatch shell
```

  7. Install the `pyfredapi` development dependencies

```bash
pip install '.[dev]'
```

  8. Setup pre-commit

```bash
pre-commit install
```

  9. Run the tests. Before making any changes it is a good to test that your environment is setup correctly. From the root of the project directory, run:

With pytest:

```bash
pytest tests/
```

With tox:

```bash
tox
```

  10. Make your changes. After making your changes:
      - Add or update tests
      - Add or update documentation

  11. Ensure the test and lint suites pass with tox. From the root of the project directory, run:

```bash
tox
```

  12. Ensure the documentation builds correctly. The documentation is built with sphinx. From the root of the project directory, run:

  ```bash
  make html -C docs/
  ```

  Then open the html docs with:

  ```bash
  open docs/_build/html/index.html
  ```

  13. Submit a pull request (PR)
