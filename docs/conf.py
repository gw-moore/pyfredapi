import pkg_resources

project = "pyfreadpi"
copyright = "2022"
author = "Greg Moore"
release = pkg_resources.get_distribution("pyfredapi").version

extensions = [
    "myst_parser",
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "sphinx.ext.autosectionlabel",
    "nbsphinx",
    "sphinxcontrib.autodoc_pydantic",
    "sphinx_copybutton",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# HTML Configuration
import plotly.io as pio

pio.renderers.default = "browser"

import sphinx_material

html_context = sphinx_material.get_html_context()
html_theme_path = sphinx_material.html_theme_path()
html_theme = "sphinx_material"
# Set link name generated in the top bar.
html_title = f"pyfredapi version {release}"
# Material theme options (see theme.conf for more information)
html_theme_options = {
    # Set the name of the project to appear in the navigation.
    "nav_title": "pyfredapi",
    # Set the color and the accent color
    # "color_primary": "blue",
    # "color_accent": "light-blue",
    # Set the repo location to get a badge with stats
    "repo_url": "https://github.com/gw-moore/pyfredapi/",
    "repo_name": "pyfredapi",
    "repo_type": "github",
    "master_doc": True,
    # Visible levels of the global TOC; -1 means unlimited
    "globaltoc_depth": 3,
    # If False, expand all TOC entries
    "globaltoc_collapse": True,
    # If True, show hidden TOC entries
    "globaltoc_includehidden": True,
}
html_show_sourcelink = True
html_sidebars = {
    "**": [
        "globaltoc.html",
        #'localtoc.html',
    ]
}

html_static_path = ["_static"]

# Make function signatures readable
autodoc_typehints = "description"
