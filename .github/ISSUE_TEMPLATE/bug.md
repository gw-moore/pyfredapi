name: 🐛 Bug
description: Report a bug or unexpected behavior in pyfredapi
labels: [bug, unconfirmed]

body:
  - type: markdown
    attributes:
      value:  Thank you for contributing to pyfredapi!

  - type: textarea
    id: description
    attributes:
      label: Description
      description: |
        Please explain what you're seeing and what you would expect to see.

        Please provide as much detail as possible to make understanding and solving your problem as quick as possible. 🙏
    validations:
      required: true

  - type: textarea
    id: example
    attributes:
      label: Example Code
      description: >
        If applicable, please add a self-contained,
        [minimal, reproducible, example](https://stackoverflow.com/help/minimal-reproducible-example)
        demonstrating the bug.

      placeholder: |
        import pyfredapi

        ...
      render: Python

  - type: textarea
    id: version
    attributes:
      label: Python, pyfredapi & OS Version
      description: |
        Which version of Python & pyfredapi are you using, and which Operating System?

      render: Text
    validations:
      required: true
