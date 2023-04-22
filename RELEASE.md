# Release Process

This document describes the process for preparing new version of the `pyfredapi` package.

## Pre-release PR Checklist

Preform these tasks before opening a PR for the `main` branch.

- [ ] Update the `CHANGELOG.md` file with the changes for the new release. Follow the [keepachangelog](https://keepachangelog.com/en/1.0.0/) guidelines.
- [ ] Check that no updates are needed in `CONTRIBUTING.md`
- [ ] Check that no updates are needed in `README.md`
- [ ] Update the requirements.txt
    ```bash
    pip-compile -o requirements.txt pyproject.toml  --resolver=backtracking
    ```
- [ ] Determine if this a major, minor, or patch release and use [hatch to bump the package version number](https://hatch.pypa.io/latest/version/#updating)
- [ ] Make sure the `pyfredapi` package builds locally
    ```bash
    hatch build
    ```

### Prepare the documentation

When the PR is merged, the Read The Docs build will be triggered and the documentation will be updated. It is important to be sure the documentation is correct before merging into the main branch.

- [ ] Update documentation dependencies for Read The Docs
    ```bash
    pip-compile --extra docs -o docs/requirements.txt pyproject.toml  --resolver=backtracking
    ```
- [ ] Test that the documentation builds locally
    ```bash
    make clean -C docs/
    make html -C docs/
    open docs/_build/html/index.html
    ```
- [ ] Review the documentation site

When a PR is opened for the main branch, the GitHub actions pipeline will the test suite and lint the code.

- [ ] Check that the CI/CD pipeline tasks have passed

# Post PR merge tasks

The package is published to PyPi via GitHub actions pipeline. The pipeline is triggered when a new version release is created in GitHub. Use the GitHub UI to create a new release.

- [ ] Title the tag `pyfredapi-v<version>`. The tag is used to trigger the GitHub actions pipeline to publish the package to PyPi.
- [ ] Title the release `pyfredapi v<version>`
- [ ] Add the changelog release notes to the release description
- [ ] Publish the release
