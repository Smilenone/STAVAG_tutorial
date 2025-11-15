# Configuration file for the Sphinx documentation builder.
# This file contains only commonly used options.
# For the full list, see:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

import os
import sys
import types

# Insert repository root so that "import STAVAG" resolves on RTD
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)

# Mark we are on Read the Docs
os.environ.setdefault("READTHEDOCS", "1")

# --------------------------- Robust lightweight stubs ---------------------------
# We do not want generic "Dummy" objects for third party libs because Sphinx
# would print "<Dummy>" in type hints. Instead we create minimal modules and
# minimal classes with proper __name__ and __module__ so that type rendering
# shows nice names like "anndata.AnnData" and "numpy.ndarray".

def _ensure_module(fullname: str) -> types.ModuleType:
    """Create and register an empty module if it does not exist."""
    if fullname in sys.modules:
        return sys.modules[fullname]
    mod = types.ModuleType(fullname)
    sys.modules[fullname] = mod
    return mod

def _make_class(name: str, module: str):
    """Make a lightweight class with correct __name__ and __module__."""
    return type(name, (), {"__module__": module})

# anndata and AnnData
_anndata = _ensure_module("anndata")
if not hasattr(_anndata, "AnnData"):
    _anndata.AnnData = _make_class("AnnData", "anndata")

# numpy and ndarray
_numpy = _ensure_module("numpy")
if not hasattr(_numpy, "ndarray"):
    _numpy.ndarray = _make_class("ndarray", "numpy")

# pandas and DataFrame
_pandas = _ensure_module("pandas")
if not hasattr(_pandas, "DataFrame"):
    _pandas.DataFrame = _make_class("DataFrame", "pandas")

# scanpy with AnnData alias
_scanpy = _ensure_module("scanpy")
if not hasattr(_scanpy, "AnnData"):
    _scanpy.AnnData = _anndata.AnnData
    
# tqdm placeholder so "import tqdm" / "from tqdm.auto import tqdm" work
_tqdm = _ensure_module("tqdm")
_tqdm_auto = _ensure_module("tqdm.auto")
_tqdm_nb = _ensure_module("tqdm.notebook")

def _noop_tqdm(iterable=None, *args, **kwargs):
    """Lightweight stand-in for tqdm that simply returns the iterable."""
    return iterable if iterable is not None else []

# tqdm.tqdm
if not hasattr(_tqdm, "tqdm"):
    _tqdm.tqdm = _noop_tqdm

# tqdm.tqdm_notebook (legacy import style)
if not hasattr(_tqdm, "tqdm_notebook"):
    _tqdm.tqdm_notebook = _noop_tqdm

# from tqdm.auto import tqdm
if not hasattr(_tqdm_auto, "tqdm"):
    _tqdm_auto.tqdm = _noop_tqdm

# from tqdm.notebook import tqdm
if not hasattr(_tqdm_nb, "tqdm"):
    _tqdm_nb.tqdm = _noop_tqdm
    
# matplotlib and pyplot
_matplotlib = _ensure_module("matplotlib")
_ensure_module("matplotlib.pyplot")  # enough for "import matplotlib.pyplot as plt"

# sklearn metrics and multioutput
_sklearn = _ensure_module("sklearn")
_metrics = _ensure_module("sklearn.metrics")
if not hasattr(_metrics, "mean_squared_error"):
    _metrics.mean_squared_error = lambda *a, **k: 0.0
if not hasattr(_metrics, "r2_score"):
    _metrics.r2_score = lambda *a, **k: 0.0
_multioutput = _ensure_module("sklearn.multioutput")
if not hasattr(_multioutput, "MultiOutputRegressor"):
    class _MultiOutputRegressor:
        def __init__(self, *a, **k): pass
        def fit(self, *a, **k): return self
        def predict(self, *a, **k): return []
    _multioutput.MultiOutputRegressor = _MultiOutputRegressor

# scipy bits that may be imported at module import time
_scipy = _ensure_module("scipy")
_scipy_cluster = _ensure_module("scipy.cluster")
_scipy_hier = _ensure_module("scipy.cluster.hierarchy")
for _fname in ("linkage", "fcluster", "dendrogram"):
    if not hasattr(_scipy_hier, _fname):
        setattr(_scipy_hier, _fname, lambda *a, **k: None)

# lightgbm placeholder so "import lightgbm as lgb" works
_ensure_module("lightgbm")

# Important note:
# We deliberately do NOT set autodoc_mock_imports because Sphinx would replace
# our carefully crafted stubs with MagicMocks and the rendered type hints
# would degrade again. Our manual stubs are already in sys.modules.


# -- Project information -----------------------------------------------------

project = "STAVAG"
copyright = "2025, Qunlun Shen"
author = "Qunlun Shen"
release = "1.0.0"


# -- General configuration ---------------------------------------------------

extensions = [
    "nbsphinx",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

html_theme_options = {
    "navigation_depth": 1,
    "collapse_navigation": True,
    "titles_only": True,
}

# Let autosummary actually generate the stub pages
autosummary_generate = True
autosummary_imported_members = True

# Autodoc options
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}
# Put annotations into the description so import-time resolution is not required
autodoc_typehints = "description"

# Napoleon for Google and NumPy style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = True

# Templates and patterns
templates_path = ["_templates"]
exclude_patterns = []

# Jupyter notebooks
nbsphinx_execute = "never"
nbsphinx_allow_errors = True

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_sidebars = {
    "**": [
        "sphinx_rtd_theme/sidebar/brand.html",
        "sphinx_rtd_theme/sidebar/search.html",
        "sphinx_rtd_theme/sidebar/navigation.html",
    ]
}
html_static_path = ["_static"]
html_css_files = [
    "hide_subsections.css",
    "fix_image_ratio.css",
]

def setup(app):
    app.add_css_file("hide_subsections.css")

# Do not import STAVAG here for debugging prints.
# Importing it here may happen before all stubs are in place and can fail.
