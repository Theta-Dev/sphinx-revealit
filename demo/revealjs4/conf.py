# -*- coding: utf-8 -*-

# -- Path setup --------------------------------------------------------------

# -- Project information -----------------------------------------------------
project = "sphinx-revealit"
copyright = "2021, Thetadev"
author = "ThetaDev"
version = '0.1.0'
release = version

# -- General configuration ---------------------------------------------------
extensions = ["sphinx_revealit"]
templates_path = ["_templates"]
source_suffix = ".rst"
master_doc = "index"
language = 'en'
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
pygments_style = 'vs'

# -- Options for HTML output -------------------------------------------------
html_theme = "alabaster"
html_static_path = ["_static"]

# -- Options for Reveal.js output ---------------------------------------------
revealjs_static_path = ["_static"]
revealjs_style_theme = "black"
revealjs_script_conf = {
    'controls': True,
    'progress': True,
    'history': True,
    'center': False,
    'transition': "slide",
    'autoPlayMedia': True,

    'width': 1920,
    'height': 1080,
    'margin': 0.04,
}

revealjs_script_plugins = [
    {
        "name": "RevealHighlight",
        "src": "revealjs4/plugin/highlight/highlight.js",
    },
]
revealjs_css_files = [
    "revealjs4/plugin/highlight/monokai.css",
]
