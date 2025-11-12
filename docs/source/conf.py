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

os.environ.setdefault("READTHEDOCS", "1")

# 一个可调用 可取属性 的 Dummy 对象
class _Dummy:
    def __init__(self, *a, **k): pass
    def __call__(self, *a, **k): return _Dummy()
    def __getattr__(self, name): return _Dummy()
    def __iter__(self): return iter([])
    def __repr__(self): return "<Dummy>"

# 生成带有 __getattr__ 的桩模块 任何属性访问都返回 Dummy
def _stub_module(fullname, attrs=None, as_package=False):
    mod = types.ModuleType(fullname)
    # PEP 562 模块级 __getattr__ 支持 from m import X 这类访问
    def __getattr__(attr):
        return _Dummy()
    mod.__getattr__ = __getattr__
    if as_package:
        mod.__path__ = []  # 标成包 允许有子模块
    if attrs:
        for k, v in attrs.items():
            setattr(mod, k, v)
    sys.modules[fullname] = mod
    return mod

# 先把顶层包占住
for pkg in ["sklearn", "matplotlib", "scipy"]:
    if pkg not in sys.modules:
        _stub_module(pkg, as_package=True)

# 针对会被显式 from-import 的符号 提供命名桩
_stub_module("sklearn.metrics", {
    "mean_squared_error": lambda *a, **k: 0.0,
    "r2_score": lambda *a, **k: 0.0,
}, as_package=False)

class _DummyEstimator:
    def __init__(self, *a, **k): pass
    def fit(self, *a, **k): return self
    def predict(self, *a, **k): return []

_stub_module("sklearn.multioutput", {
    "MultiOutputRegressor": _DummyEstimator,
}, as_package=False)

# 其他常见依赖做通用桩 足够支撑导入与注释提取
for name in [
    "numpy", "pandas", "scanpy", "lightgbm",
    "matplotlib.pyplot",
    "scipy", "scipy.cluster", "scipy.cluster.hierarchy",
    "anndata",
]:
    if name not in sys.modules:
        _stub_module(name)

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
