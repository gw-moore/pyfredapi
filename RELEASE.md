# Release Process

This document describes the process for preparing new version of the `pyfredapi` package.

## Pre-release PR Checklist

Preform these tasks before opening a PR for the `main` branch.

- [ ] Bump the version number. `pyfredapi` follow [semantic versioning](https://semver.org/spec/v2.0.0.html), and uses [hatch](https://hatch.pypa.io/latest/) to manage the version number.
    - Determine if this is a major, minor, or patch release based on the UNRELEASED section in changelog
    - Use [hatch to bump the package version number](https://hatch.pypa.io/latest/version/#updating)
- [ ] Update the `CHANGELOG.md` file with the changes for the new release. Follow the [keepachangelog](https://keepachangelog.com/en/1.0.0/) guidelines.
- [ ] Check that no updates are needed in `CONTRIBUTING.md`
- [ ] Check that no updates are needed in `README.md`
- [ ] Update the requirements.txt
    ```bash
    python -m piptools compile --upgrade -o requirements.txt pyproject.toml
    ```
- [ ] Run unit tests and make fresh vcr cassettes
    ```bash
    pytest tests/ --record-mode=all --runslow
    ```
- [ ] Make sure the `pyfredapi` package builds locally
    ```bash
    hatch build
    ```

### Prepare the documentation

When a commit is made to the `main` branch, the Read The Docs build will be triggered and the documentation will be updated. It is important to be sure the documentation is correct before merging into the main branch.

- [ ] Update documentation dependencies for Read The Docs
    ```bash
    python -m piptools compile --upgrade --extra docs -o docs/requirements.txt pyproject.toml
    ```
- [ ] Test that the documentation builds locally
    ```bash
    mkdocs build
    open site/index.html
    ```
- [ ] Review the documentation site

## Open a PR

When a PR is opened for the main branch, the GitHub actions pipeline will the test suite and lint the code.

- [ ] Check that the CI/CD pipeline tasks have passed
- [ ] Give the PR a descriptive title
- [ ] Add a description of the changes

## Post PR merge tasks

The package is published to PyPi via GitHub actions pipeline. The pipeline is triggered when a new version release is created in GitHub. Use the GitHub UI to create a new release.

- [ ] Title the tag `pyfredapi-v<version>`. The tag is used to trigger the GitHub actions pipeline to publish the package to PyPi.
- [ ] Title the release `pyfredapi v<version>`
- [ ] Add the changelog release notes to the release description
- [ ] Publish the release
