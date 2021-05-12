###############
Sphinx-RevealIT
###############

Create beautifully animated presentations with the Sphinx documentation builder.

Reveal.js is a javascript-based presentation library created by Hakim El Hattab.
It transforms HTML documents into interactive presentations which can be viewed
in any browser.

Sphinx-RevealIT is an extension for the popular Sphinx documentation builder
that can generate these presentations from simple ReStructured text.

It includes various directives that allow you to use most of Reveal's functionality
like animated fragments and code blocks or custom background and animations.

Sphinx-RevealIT comes with the tailwind.css framework out of the box, which makes
custom formatting and layouting super easy.

Note that Sphinx-RevealIT is not compatible with old browsers that don't support
CSS variables (like IE11).


Usage
#####

#. Create your sphinx documentation
#. Edit ``conf.py`` to use this extension

.. code:: python

    extensions = ['sphinx_revealit']
    pygments_style = 'monokai'

    revealjs_static_path = ["_static"]
    revealjs_style_theme = "black"
    revealjs_use_tailwind = True

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
        'RevealZoom', 'RevealSearch'
    ]

#. Write your presentation in ReStructured text

#. Build sources as Reveal.js presentation

::

    $ make revealjs

Directives
##########

rjs-deck
========

Set attributes for a RevealJS deck (presentation).

+--------------+----------+--------------------------+
| Attribute    | Value    | Description              |
+==============+==========+==========================+
| theme        | String   | RevealJS theme           |
+--------------+----------+--------------------------+
| conf         | JSON     | RevealJS config          |
+--------------+----------+--------------------------+
| stylesheet   | Path     | Path to CSS stylesheet   |
+--------------+----------+--------------------------+

rjs-section, rjs-break
======================

Set attributes for a RevealJS slide. Place the ``rjs-section`` directive
after the title. The ``rjs-break`` directive splits a document section
into multiple slides.

+-----------------------------+---------------------------+-----------------------------------------------------------------------------------+
| Attribute                   | Value                     | Description                                                                       |
+=============================+===========================+===================================================================================+
| background-color            | CSS color                 | Background color                                                                  |
+-----------------------------+---------------------------+-----------------------------------------------------------------------------------+
| background-image            | Image file/URL            | Background image                                                                  |
+-----------------------------+---------------------------+-----------------------------------------------------------------------------------+
| background-position         | CSS background-position   | Position of background image                                                      |
+-----------------------------+---------------------------+-----------------------------------------------------------------------------------+
| background-repeat           | CSS background-repeat     | Should background image repeat                                                    |
+-----------------------------+---------------------------+-----------------------------------------------------------------------------------+
| background-size             | cover / contain           | Cropping / Letterboxing                                                           |
+-----------------------------+---------------------------+-----------------------------------------------------------------------------------+
| background-video            | Video file/URL            | Background video                                                                  |
+-----------------------------+---------------------------+-----------------------------------------------------------------------------------+
| background-video-loop       | Flag                      | Should video play repeatedly                                                      |
+-----------------------------+---------------------------+-----------------------------------------------------------------------------------+
| background-video-muted      | Flag                      | Should audio be muted                                                             |
+-----------------------------+---------------------------+-----------------------------------------------------------------------------------+
| background-opacity          | 0 - 1                     | Background image/video opacity (0: transparent, 1: opaque)                        |
+-----------------------------+---------------------------+-----------------------------------------------------------------------------------+
| background-iframe           | iframe URL                | Show a website as slide background                                                |
+-----------------------------+---------------------------+-----------------------------------------------------------------------------------+
| background-interactive      | Flag                      | Make iframe interactive                                                           |
+-----------------------------+---------------------------+-----------------------------------------------------------------------------------+
| transition                  | RevealJS Transition       | Slide transition                                                                  |
+-----------------------------+---------------------------+-----------------------------------------------------------------------------------+
| background-transition       | RevealJS Transition       | Background transition                                                             |
+-----------------------------+---------------------------+-----------------------------------------------------------------------------------+
| auto-animate                | Flag                      | Auto-An                                                                           |
+-----------------------------+---------------------------+-----------------------------------------------------------------------------------+
| auto-animate-easing         | CSS easing                | CSS easing function                                                               |
+-----------------------------+---------------------------+-----------------------------------------------------------------------------------+
| auto-animate-no-unmatched   | Flag                      | Determines whether elements with no matching auto-animate target should fade in   |
+-----------------------------+---------------------------+-----------------------------------------------------------------------------------+
| auto-animate-duration       | decimal number            | Animation duration in seconds                                                     |
+-----------------------------+---------------------------+-----------------------------------------------------------------------------------+
| auto-animate-delay          | decimal number            | Animation delay in seconds                                                        |
+-----------------------------+---------------------------+-----------------------------------------------------------------------------------+
| notitle                     | Flag                      | Dont show title                                                                   |
+-----------------------------+---------------------------+-----------------------------------------------------------------------------------+
| visibility                  | hidden / uncounted        | Hide slides or remove them from count and progress                                |
+-----------------------------+---------------------------+-----------------------------------------------------------------------------------+
| center                      | Flag                      | Center slide content                                                              |
+-----------------------------+---------------------------+-----------------------------------------------------------------------------------+
| light                       | Flag                      | Mark background image/iframe as light (dark text)                                 |
+-----------------------------+---------------------------+-----------------------------------------------------------------------------------+
| dark                        | Flag                      | Mark background image/iframe as dark (light text)                                 |
+-----------------------------+---------------------------+-----------------------------------------------------------------------------------+
| class                       | String                    | CSS classes                                                                       |
+-----------------------------+---------------------------+-----------------------------------------------------------------------------------+

rjs-fragments
=============

Block of RevealJS fragments. Applies effects to all children of the
following types: paragraph, list item, image, rjs-box, rjs-title

+-------------+----------+---------------------------------------+
| Attribute   | Value    | Description                           |
+=============+==========+=======================================+
| VALUE       | String   | RevealJS effect                       |
+-------------+----------+---------------------------------------+
| class       | String   | CSS classes                           |
+-------------+----------+---------------------------------------+
| stack       | Flag     | Stack fragments on top of eachother   |
+-------------+----------+---------------------------------------+

rjs-effect
==========

Single RevealJS fragment. Can be used in a ``revealjs_fragments`` block
to override properties of a single fragment, too.

+-------------+----------+--------------------+
| Attribute   | Value    | Description        |
+=============+==========+====================+
| VALUE       | String   | RevealJS effect    |
+-------------+----------+--------------------+
| data-id     | String   | RevealJS data id   |
+-------------+----------+--------------------+
| index       | Number   | Index number       |
+-------------+----------+--------------------+

rjs-effects
===========

Nested RevealJS fragments

+-------------+---------------------------------------------------------------------------------------------------------------------+----------------------------+
| Attribute   | Value                                                                                                               | Description                |
+=============+=====================================================================================================================+============================+
| VALUE       | String, separated by whitespace\ ``fade-in highlight-ff0000 fade-out``\ \ ``1.fade-in highlight-blue 5.fade-out``   | Effect sequence to apply   |
+-------------+---------------------------------------------------------------------------------------------------------------------+----------------------------+
| data-id     | String                                                                                                              | RevealJS data id           |
+-------------+---------------------------------------------------------------------------------------------------------------------+----------------------------+

rjs-code, rjs-literalinclude
============================

Code block with added RevealJS functionality. Backwards compatible to
the vanilla Sphinx code block.

+-------------------+--------------------------------------------------------------+--------------------------------------------------------------------------------+
| Attribute         | Value                                                        | Description                                                                    |
+===================+==============================================================+================================================================================+
| emphasize-lines   | Line number ranges (``1, 3``, ``4-7``), separated by ``|``   | Code lines to highlight. Separate with ``|`` to highlight them step-by-step.   |
+-------------------+--------------------------------------------------------------+--------------------------------------------------------------------------------+
| index             | Number                                                       | Effect index                                                                   |
+-------------------+--------------------------------------------------------------+--------------------------------------------------------------------------------+
| data-id           | String                                                       | RevealJS data id                                                               |
+-------------------+--------------------------------------------------------------+--------------------------------------------------------------------------------+

rjs-id
======

Set RevealJS ``data-id`` property of the following node. Supported nodes
are ``paragraph`` and ``literal_block``.

rjs-div, rjs-box
================

+-------------+----------+--------------------+
| Attribute   | Value    | Description        |
+=============+==========+====================+
| VALUE       | String   | CSS classes        |
+-------------+----------+--------------------+
| data-id     | String   | RevealJS data id   |
+-------------+----------+--------------------+
| style       | String   | CSS styling        |
+-------------+----------+--------------------+

rjs-title
=========

Turns the following paragraph into a title. Value determines header
level (default: 3).

+-------------+-----------------------+-----------------------+
| Attribute   | Value                 | Description           |
+=============+=======================+=======================+
| VALUE       | [Number (1-6)] Text   | Header level, Title   |
+-------------+-----------------------+-----------------------+
| data-id     | String                | RevealJS data id      |
+-------------+-----------------------+-----------------------+
| style       | String                | CSS styling           |
+-------------+-----------------------+-----------------------+
| class       | String                | CSS classes           |
+-------------+-----------------------+-----------------------+

Config values
#############

+-----------------------------+------------------+-----------+-------------------------------------------+
| Attribute                   | Value            | Default   | Description                               |
+=============================+==================+===========+===========================================+
| revealjs_static_path        | List             | []        | Static file folder for RevealJS builder   |
+-----------------------------+------------------+-----------+-------------------------------------------+
| revealjs_style_theme        | RevealJS Theme   | black     | RevealJS theme (builtin or css file)      |
+-----------------------------+------------------+-----------+-------------------------------------------+
| revealjs_use_tailwind       | bool             | False     | Use tailwind.css framework                |
+-----------------------------+------------------+-----------+-------------------------------------------+
| revealjs_purge_tailwind     | bool             | True      | Remove unused classes from tailwind.css   |
+-----------------------------+------------------+-----------+-------------------------------------------+
| revealjs_script_files       | List             | []        | Extra JS files to include                 |
+-----------------------------+------------------+-----------+-------------------------------------------+
| revealjs_script_conf        | dict             | {}        | RevealJS config                           |
+-----------------------------+------------------+-----------+-------------------------------------------+
| revealjs_script_plugins     | List             | []        | RevealJS plugins                          |
+-----------------------------+------------------+-----------+-------------------------------------------+
| revealjs_css_files          | List             | []        | Extra CSS files to include                |
+-----------------------------+------------------+-----------+-------------------------------------------+


Thank you
#########

goes to Kazuya Takei who created the original sphinx-revealjs project from which this is a fork of.
Also thanks tho Hakim El Hattab, creator of the Reveal.js presentation framework. 
