sphinx-revealit
===============

Sphinx extension with theme to generate Reveal.js presentations.

Overview
--------

This extension generates Reveal.js presentations
from **standard** reStructuredText.

It includes these features.

* Custom builder to translate from reST to reveal.js style HTML
* Template to be enable to render presentation local independent


Usage
-----

1. Create your sphinx documentation
2. Edit `conf.py` to use this extension

.. code-block:: python

  extensions = [
    'sphinx_revealit',
  ]

3. Write source for standard document style

4. Build sources as Reveal.js presentation

.. code-block:: bash

  $ make revealjs

Contributings
-------------

GitHub repository does not have reveal.js library.

If you use from GitHub and editable mode, Run ``tools/fetch_revealjs.py`` after install.


Copyright
---------

Apache-2.0 license. Please see `LICENSE <./LICENSE>`_.
