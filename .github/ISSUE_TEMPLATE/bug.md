name: Bug Report
description: File a bug report
title: "[Bug]: "
labels: ["bug", "triage"]

body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to fill out this bug report!
  - type: textarea
    id: what-happened
    attributes:
      label: What happened?
      description: Also tell us, what did you expect to happen?
      placeholder: Tell us what you see!
      value: "A bug happened!"
    validations:
      required: true
  - type: textarea
    id: version
    attributes:
      label: Version
      description: Which version of Python & Pyfredapi are you using, and which Operating System?
    validations:
      required: true
