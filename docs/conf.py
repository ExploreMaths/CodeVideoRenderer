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
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'locales']

# -- Internationalization --------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-internationalization

# RTD normalizes language codes to ll-cc (e.g. zh-cn), but Sphinx uses ll_CC (e.g. zh_CN).
language = os.environ.get('READTHEDOCS_LANGUAGE', 'en')
if '-' in language:
    lang, country = language.split('-')
    language = f'{lang}_{country.upper()}'

locale_dirs = ['locales']
gettext_compact = False
autodoc_mock_imports = [
    "typing", 
    "manim",
    "numpy",
    "moviepy",
    "PIL",
]
autodoc_default_options = {
    'member-order': 'bysource',
    'show-inheritance': True,
}
autodoc_typehints_format = 'short'
python_use_unqualified_type_names = True
autodoc_type_aliases = {
    'PygmentsLanguage': 'CodeVideoRenderer.typing.PygmentsLanguage',
    'PygmentsFormatterStyle': 'CodeVideoRenderer.typing.PygmentsFormatterStyle',
    'StrPath': 'CodeVideoRenderer.typing.StrPath',
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
html_css_files = [
    'custom.css',
]

html_title = f'{project} v{release}'
html_logo = f'{html_static_path[0]}/logo.png'
html_favicon = f'{html_static_path[0]}/favicon.ico'
html_theme_options = {
    "light_css_variables": {
        "font-stack--headings": "Georgia, serif",
    },
}

# -- Setup connections ---------------------------------------------------

import re
from pathlib import Path

def replace_typealias_forwardrefs(app, what, name, obj, options, signature, return_annotation):
    """Replace TypeAliasForwardRef('module.path.AliasName') with AliasName in signatures."""
    pattern = r"TypeAliasForwardRef\(['\"]([\w.]+)['\"]\)"
    repl = lambda m: m.group(1).rsplit('.', 1)[-1]
    if signature:
        signature = re.sub(pattern, repl, signature)
    if return_annotation:
        return_annotation = re.sub(pattern, repl, return_annotation)
    return signature, return_annotation

def _link_type_aliases_in_html(app, exception):
    """Scan built HTML files and replace <em>Alias</em> with native <a><em> links.

    This runs after the HTML build finishes so that Sphinx's own
    PyTypedField.make_field logic (which wraps every type token in <em>)
    is left untouched; we only turn the bare <em> aliases into hyperlinks.
    """
    if exception is not None:
        return

    build_dir = Path(app.outdir)
    for html_path in build_dir.rglob('*.html'):
        content = html_path.read_text(encoding='utf-8')
        new_content = content
        for alias, full_path in autodoc_type_aliases.items():
            # Only replace <em>Alias</em> when it is NOT already inside an <a> tag.
            pattern = re.compile(
                rf'(?<!</a>)<em>{re.escape(alias)}</em>(?!</a>)'
            )
            repl = (
                f'<a class="reference internal" href="typing.html#{full_path}" '
                f'title="{full_path}"><em>{alias}</em></a>'
            )
            new_content = pattern.sub(repl, new_content)
        if new_content != content:
            html_path.write_text(new_content, encoding='utf-8')


def setup(app):
    app.connect('autodoc-process-signature', replace_typealias_forwardrefs)
    app.connect('build-finished', _link_type_aliases_in_html)