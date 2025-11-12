# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import types

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)


# -- Project information -----------------------------------------------------

project = 'STAVAG'
copyright = '2025, Qunlun Shen'
author = 'Qunlun Shen'

# The full version, including alpha/beta/rc tags
release = '1.0.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'nbsphinx',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

html_theme_options = {
    "navigation_depth": 1,    
    "collapse_navigation": True,
    "titles_only": True
}

autosummary_generate = True
autosummary_imported_members = True
autodoc_mock_imports = MOCKS
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}
napoleon_google_docstring = True
napoleon_numpy_docstring = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

nbsphinx_execute = 'never'     
nbsphinx_allow_errors = True    

MOCKS = [
    "numpy", "pandas", "scanpy", "lightgbm",
    "matplotlib", "matplotlib.pyplot",
    "sklearn", "sklearn.metrics", "sklearn.multioutput",
    "scipy", "scipy.cluster", "scipy.cluster.hierarchy",
    "anndata",
]
for m in MOCKS:
    sys.modules.setdefault(m, types.ModuleType(m))

# 让 matplotlib 有个 pyplot 属性，避免属性访问报错
if hasattr(sys.modules["matplotlib"], "__dict__"):
    sys.modules["matplotlib"].pyplot = sys.modules.get(
        "matplotlib.pyplot", types.ModuleType("matplotlib.pyplot")
    )

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
#html_theme = 'alabaster'
html_theme = 'sphinx_rtd_theme'
html_sidebars = {
    '**': [
        'sphinx_rtd_theme/sidebar/brand.html',
        'sphinx_rtd_theme/sidebar/search.html',
        'sphinx_rtd_theme/sidebar/navigation.html',
    ]
}
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_css_files = [
    'hide_subsections.css',
    'fix_image_ratio.css', 
]

def setup(app):
    app.add_css_file('hide_subsections.css') 
try:
    import STAVAG as _S
    print("[docs] STAVAG imported from:", getattr(_S, "__file__", _S))
except Exception as e:
    print("[docs] STAVAG import failed:", e)
