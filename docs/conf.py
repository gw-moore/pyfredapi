import sphinx_material
from pyfredapi import __version__
import plotly.io as pio

pio.renderers.default = "browser"

# -- Project information -----------------------------------------------------

project = "pyfredapi"
html_title = "pyfredapi"

copyright = "2022, Greg Moore"
author = "Greg Moore"

# The full version, including alpha/beta/rc tags
release = __version__

# The master toctree document.
master_doc = "index"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "myst_parser",
    "nbsphinx",
    "sphinx_copybutton",
]

nbsphinx_execute = "never"

# Setup auto-doc options for all documented modules in references/api.rst
autodoc_default_options = {
    "members": True,
    "show-inheritance": True,
}

# Make function signatures readable
autodoc_typehints = "description"

# -- HTML theme settings ------------------------------------------------

# Material theme options
extensions.append("sphinx_material")
html_theme_path = sphinx_material.html_theme_path()
html_context = sphinx_material.get_html_context()
html_theme = "sphinx_material"
html_show_sourcelink = False
html_sidebars = {
    "**": ["logo-text.html", "globaltoc.html", "localtoc.html", "searchbox.html"]
}
html_theme_options = {
    "base_url": "https://pyfredapi.readthedocs.io/en/latest/",
    "repo_url": "https://github.com/gw-moore/pyfredapi/",
    "repo_name": project,
    "repo_type": "github",
    "nav_title": f"{project} v{release}",
    # "nav_links": [
    #     {
    #         "href": "index",
    #         "title": project,
    #         "internal": True,
    #     }
    # ],
    "color_primary": "indigo",
    "color_accent": "blue",
    "globaltoc_depth": 2,
    "master_doc": True,
    "heroes": {
        "index": "Python library to make retrieving data from FRED easy",
    },
    # setting the logo icon so as to not have broken element on the page
    # considering adding a custom svg to the project and assigning it to 'html_logo'
    "logo_icon": "&#xE1AF",
}

html_static_path = ["_static"]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
