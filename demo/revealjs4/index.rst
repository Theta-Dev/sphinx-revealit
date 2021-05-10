===============
sphinx-revealit
===============

.. rjs-deck::
  :stylesheet: _static/style.css

.. rjs-section::
  :center:
  :class: abc def

.. rjs-title:: 4
  Create awesome presentations using Sphinx

.. rst-class:: testclass

``sphinx-revealit`` is an extenstion for the Sphinx documentation generator
that allows you to build HTML-based presentations using the RevealJS library.

First slide
===========

.. rjs-section::
  :background-color: #009900

Hello World, this is me, ThetaDev

.. rjs-fragments:: fade-right

  - want to be a software developer
  - doing web projects in my free time
  - likes arduino

.. rjs-fragments:: fade-right
  :stack:

  .. image:: /img/icon-attakei.jpg

  .. image:: /img/cat.jpeg
  
Second slide
============

.. rjs-section::
  :auto-animate:

.. rjs-id:: code1

.. code-block:: python
  :linenos:
  :emphasize-lines: 1
  
  def hello_world():
    print('Hello World')

Print some

  
Second slide
============

.. rjs-section::
  :auto-animate:

.. rjs-code:: python
  :linenos:
  :emphasize-lines: 2-3|6|1,5
  :data-id: code1
  
  def hello_world():
    print('Hello World')
    print('This is me')

  def __main__():
    hello_world()

Print some more

Unmatched paragraph


Third slide
===========

.. rjs-section::
  :notitle:

Grid table:

+------------+------------+-----------+
| Header 1   | Header 2   | Header 3  |
+============+============+===========+
| body row 1 | column 2   | column 3  |
+------------+------------+-----------+
| body row 2 | Cells may span columns.|
+------------+------------+-----------+

Jujubes pie chocolate brownie cake powder dragée gummies dragée. Jelly jujubes liquorice halvah gummies. Danish dessert donut. Jelly beans toffee ice cream muffin jujubes croissant cheesecake oat cake. Brownie lemon drops tootsie roll pie lollipop chocolate pie candy dragée. Fruitcake topping gummies jelly-o marzipan gingerbread. Ice cream liquorice cake gummi bears bear claw. Lemon drops chocolate cupcake sesame snaps ice cream chocolate bar. Chocolate oat cake donut fruitcake chocolate bar lemon drops muffin. Danish pastry chocolate liquorice macaroon macaroon donut toffee dessert. Gummies jelly jujubes topping carrot cake lemon drops muffin danish bear claw. Bear claw macaroon sugar plum bonbon chocolate cake cake chocolate candy canes lemon drops.

.. rjs-break::

Jujubes pie chocolate brownie cake powder dragée gummies dragée. Jelly jujubes liquorice halvah gummies. Danish dessert donut. Jelly beans toffee ice cream muffin jujubes croissant cheesecake oat cake. Brownie lemon drops tootsie roll pie lollipop chocolate pie candy dragée. Fruitcake topping gummies jelly-o marzipan gingerbread. Ice cream liquorice cake gummi bears bear claw. Lemon drops chocolate cupcake sesame snaps ice cream chocolate bar. Chocolate oat cake donut fruitcake chocolate bar lemon drops muffin. Danish pastry chocolate liquorice macaroon macaroon donut toffee dessert. Gummies jelly jujubes topping carrot cake lemon drops muffin danish bear claw. Bear claw macaroon sugar plum bonbon chocolate cake cake chocolate candy canes lemon drops.


Fourth slide
============

.. rjs-section::
  :background-image: /img/cat.jpeg


.. image:: /img/icon-attakei.jpg


Fourth#2 slide
==============

.. rjs-section::
  :background-image: /img/dir1/cat.jpeg

.. rjs-literalinclude:: run.py
  :emphasize-lines: 1-3|4-5


Animation time
==============

.. rjs-effect::
  :data-id: abc
  :index: 0

  First animation

.. rjs-effects::
  1.fade-in
  2.highlight-red
  4.strike
  6.fade-out

  Hello World

.. rjs-effects::
  1.fade-in
  3.highlight-red
  4.strike
  5.fade-out

  This is me


..
  YT video
  ========
  
  .. rjs-section::
    :background-iframe: https://www.youtube.com/embed/XaqR3G_NVoo
    :background-size: contain
    :notitle:


DIVs
====

Let's test some divs:

.. rjs-div:: grid grid-cols-3 gap-4

  .. rjs-div:: bg-purple-600 text-left
  
    Text in col1

  .. rjs-div:: bg-purple-700
  
    Text in col2

    .. rst-class:: text-red-500
    
    Some RED text

  .. rjs-div:: bg-purple-800 text-right
  
    Text in col3
