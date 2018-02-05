======================
Documentation How-To's
======================

Build a template, using sphinx-quickstart::

  > sphinx-quickstart


Defaults from last run::

  > Root path for the documentation [.]: docs
  > Separate source and build directories (y/n) [n]:
  > Name prefix for templates and static dir [_]:
  > Project name: edafos
  > Author name(s): Nick Machairas
  > Project version []: 0.1.0
  > Project release [0.1.0]:
  > Project language [en]:
  > Source file suffix [.rst]:
  > Name of your master document (without suffix) [index]:
  > Do you want to use the epub builder (y/n) [n]: y
  > autodoc: automatically insert docstrings from modules (y/n) [n]: y
  > doctest: automatically test code snippets in doctest blocks (y/n) [n]: y
  > intersphinx: link between Sphinx documentation of different projects (y/n) [n]:
  > todo: write "todo" entries that can be shown or hidden on build (y/n) [n]: y
  > coverage: checks for documentation coverage (y/n) [n]:
  > imgmath: include math, rendered as PNG or SVG images (y/n) [n]:
  > mathjax: include math, rendered in the browser by MathJax (y/n) [n]: y
  > ifconfig: conditional inclusion of content based on config values (y/n) [n]:
  > viewcode: include links to the source code of documented Python objects (y/n) [n]: y
  > githubpages: create .nojekyll file to publish the document on GitHub pages (y/n) [n]: y
  > Create Makefile? (y/n) [y]:
  > Create Windows command file? (y/n) [y]:

Build html::
  > make html
