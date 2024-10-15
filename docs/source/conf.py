# Configuration file for the Sphinx documentation builder.  # noqa: D100
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path("../..", "ia").resolve()))

import ia

# The short X.Y version (including .devXXXX, rcX, b1 suffixes if present)
version = re.sub(r"(\d+\.\d+)\.\d+(.*)", r"\1\2", ia.__version__)
version = re.sub(r"(\.dev\d+).*?$", r"\1", version)

project = "IA - Search Algorithms"
copyright = "2024, Pablo Hernández Jiménez"
author = "Pablo Hernández Jiménez"
release = ia.__version__
print(f"{version} {release}")

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "numpydoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.autosummary",
    "sphinx.ext.graphviz",
    "sphinx.ext.ifconfig",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "IPython.sphinxext.ipython_console_highlighting",
    "IPython.sphinxext.ipython_directive",
    "sphinx_copybutton",
    "sphinx_design",
]

templates_path = ["_templates"]
exclude_patterns = ["_autosummary/ia.graph.parser.generated_parser*"]

default_role = "autolink"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_title = "IA - Search Algorithms"
html_last_updated_fmt = "%b %d, %Y"
html_use_modindex = True
html_copy_source = False
html_domain_indices = False
html_file_suffix = ".html"
html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]

html_theme_options = {
    # "logo": {
    #     "image_light": "_static/numpylogo.svg",
    #     "image_dark": "_static/numpylogo_dark.svg",
    # },
    "github_url": "https://github.com/hadronomy/PR1y2-IA-2425",
    "collapse_navigation": True,
    "header_links_before_dropdown": 6,
    # Add light/dark mode and documentation version switcher:
    "navbar_end": [
        "search-button",
        "theme-switcher",
        # "version-switcher",
        "navbar-icon-links",
    ],
    "navbar_persistent": [],
}

add_function_parentheses = False
coverage_show_missing_items = True
numpydoc_show_class_members = False

autosummary_generate = True
autosummary_imported_members = True

rst_epilog = """
.. |repo_url| replace:: https://github.com/hadronomy/PR1y2-IA-2425
"""
