sphinx-revealit
===============

Sphinx extension with theme to generate Reveal.js presentations.

Overview
--------

This extension generate Reveal.js presentation
from **standard** reStructuredText.

It include theses features.

* Custom builder to translate from reST to reveal.js style HTML
* Template to be enable to render presentation local independent

Installation
------------

.. code-block:: bash

    $ pip install sphinx-revealjs


Usage
-----

1. Create your sphinx documentation
2. Edit `conf.py` to use this extension

    .. code-block:: python

        extensions = [
            'sphinx_revealjs',
        ]

3. Write source for standard document style

4. Build sources as Reveal.js presentation

    .. code-block:: bash

        $ make revealjs

Change logs
-----------

See `it <./CHANGES.rst>`_

Policy for following to Reveal.js version
-----------------------------------------

This is implemented based Reveal.js.
I plan to update it at patch-version for catch up when  new Reveal.js version released.

* If Reveal.js updated minor or patch version, sphinx-revealjs update patch version.
* If Reveal.js updated major version, sphinx-revealjs update minor version with compatible for two versions.

Futures
-------

* Index template as none presentation
* CDN support

Contributings
-------------

GitHub repository does not have reveal.js library.

If you use from GitHub and editable mode, Run ``tools/fetch_revealjs.py`` after install.

.. code-block:: bash

    $ git clone https://github.com/attakei/sphinx-revealjs
    $ cd sphinx-revealjs
    $ poetry install
    $ poetry run python tools/fetch_revealjs.py

Copyright
---------

Apache-2.0 license. Please see `LICENSE <./LICENSE>`_.
