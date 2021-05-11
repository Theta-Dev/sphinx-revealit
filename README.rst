###############
sphinx-revealit
###############

Create beautifully animated presentations with the Sphinx documentation
builder.

Usage
#####

#. Create your sphinx documentation
#. Edit ``conf.py`` to use this extension

.. code:: python

    extensions = ['sphinx_revealit']
    pygments_style = 'monokai'

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
| revealjs\_static\_path      | List             | []        | Static file folder for RevealJS builder   |
+-----------------------------+------------------+-----------+-------------------------------------------+
| revealjs\_style\_theme      | RevealJS Theme   | black     | RevealJS theme (builtin or css file)      |
+-----------------------------+------------------+-----------+-------------------------------------------+
| revealjs\_script\_files     | List             | []        | Extra JS files to include                 |
+-----------------------------+------------------+-----------+-------------------------------------------+
| revealjs\_script\_conf      | dict             | {}        | RevealJS config                           |
+-----------------------------+------------------+-----------+-------------------------------------------+
| revealjs\_script\_plugins   | List             | []        | RevealJS plugins                          |
+-----------------------------+------------------+-----------+-------------------------------------------+
| revealjs\_css\_files        | List             | []        | Extra CSS files to include                |
+-----------------------------+------------------+-----------+-------------------------------------------+

