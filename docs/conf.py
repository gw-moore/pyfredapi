"""Sphinx configuration."""
import plotly.io as pio
import sphinx_material

from pyfredapi import __version__

pio.renderers.default = "browser"

# -- Project information -----------------------------------------------------

project = "pyfredapi"
html_title = "pyfredapi"

copyright = "2023, Greg Moore"
author = "Greg Moore"

# The full version, including alpha/beta/rc tags
release = __version__

# The master toctree document.
master_doc = "index"

# -- General configuration ---------------------------------------------------

extensions = [
    "nbsphinx",
    "myst_parser",
    "sphinx_copybutton",
    "sphinxcontrib.autodoc_pydantic",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

nbsphinx_execute = "never"
autosummary_generate = True
autodoc_pydantic_model_show_config_summary = False
autodoc_pydantic_model_show_config_member = False
autodoc_pydantic_model_show_field_summary = True
autodoc_pydantic_model_undoc_members = False
napoleon_numpy_docstring = True
napoleon_preprocess_types = True

# Setup auto-doc options for all documented modules in references/api.rst
autodoc_default_options = {
    "members": True,
    "show-inheritance": True,
}

# Make function signatures readable
autodoc_typehints = "description"

# -- HTML theme settings ------------------------------------------------

# Sphinx-Immaterial theme options
extensions.append("sphinx_immaterial")
html_theme = "sphinx_immaterial"
html_theme_options = {
    "icon": {
        "repo": "fontawesome/brands/github",
        "edit": "material/file-edit-outline",
    },
    "site_url": "https://pyfredapi.readthedocs.io",
    "repo_url": "https://github.com/gw-moore/pyfredapi/",
    "repo_name": "pyfredapi",
    "edit_uri": "blob/main/docs",
    "globaltoc_collapse": True,
    "features": [
        "navigation.expand",
        # "navigation.tabs",
        # "toc.integrate",
        "navigation.sections",
        # "navigation.instant",
        # "header.autohide",
        "navigation.top",
        # "navigation.tracking",
        # "search.highlight",
        "search.share",
        "toc.follow",
        "toc.sticky",
        "content.tabs.link",
        "announce.dismiss",
    ],
    "palette": [
        {
            "media": "(prefers-color-scheme: light)",
            "scheme": "default",
            "primary": "indigo",
            "accent": "light-blue",
            "toggle": {
                "icon": "material/lightbulb-outline",
                "name": "Switch to dark mode",
            },
        },
        {
            "media": "(prefers-color-scheme: dark)",
            "scheme": "slate",
            "primary": "indigo",
            "accent": "light-blue",
            "toggle": {
                "icon": "material/lightbulb",
                "name": "Switch to light mode",
            },
        },
    ],
    "toc_title_is_page_title": True,
    # BEGIN: social icons
    "social": [
        {
            "icon": "fontawesome/brands/github",
            "link": "https://github.com/gw-moore/pyfredapi",
            "name": "Source on github.com",
        },
        {
            "icon": "fontawesome/brands/python",
            "link": "https://pypi.org/project/pyfredapi/",
        },
    ],
    # END: social icons
}

html_static_path = ["_static"]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
