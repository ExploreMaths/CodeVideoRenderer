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
    "PIL",
    "typeguard",
]
autodoc_default_options = {
    'member-order': 'bysource',
    'show-inheritance': True,
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

# -- Fix mock signatures ---------------------------------------------------

import inspect
from sphinx.util.inspect import stringify_signature

def fix_mock_signatures(app, what, name, obj, options, signature, return_annotation):
    """Fix signatures for classes whose __new__ is inherited from mocked base classes.

    When a class inherits from a mocked object (e.g. via autodoc_mock_imports),
    Sphinx may pick up the mock's __new__ signature (*args, **kwargs) instead of
    the actual __init__ signature. This handler falls back to __init__ when it
    detects the generic mock signature.
    """
    if what == 'class' and signature == '(*args: Any, **kwargs: Any)':
        init = getattr(obj, '__init__', None)
        if init is not None:
            try:
                sig = inspect.signature(init)
                params = list(sig.parameters.values())[1:]  # remove self
                if params:
                    sig = sig.replace(parameters=params)
                    return stringify_signature(sig), None
            except ValueError:
                pass
    return signature, return_annotation

def setup(app):
    app.connect('autodoc-process-signature', fix_mock_signatures)