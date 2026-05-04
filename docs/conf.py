# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'CodeVideoRenderer'
copyright = '2026, Explore Maths'
author = 'Explore Maths'
release = '1.2.3'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

extensions = [
    "m2r2",
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    "sphinx_design",
    "sphinx_copybutton",
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
autodoc_mock_imports = [
    "typing", 
    "manim",
    "rich",
    "numpy",
    "proglog",
    "moviepy",
    "PIL"
]
autodoc_default_options = {
    'member-order': 'bysource'
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
html_css_files = [
    'custom.css',
    'https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@7.2.0/css/all.min.css',
]

html_title = f'{project} v{release}'
html_logo = f'{html_static_path[0]}/logo.png'
html_favicon = f'{html_static_path[0]}/favicon.ico'
html_theme_options = {
    "light_css_variables": {
        "font-stack--headings": "Georgia, serif",
    },
}