.. CodeVideoRenderer documentation master file, created by
   sphinx-quickstart on Mon Apr 20 19:33:36 2026.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

CodeVideoRenderer
=================

**CodeVideoRenderer** is a Python animation library based on Manim, specifically designed for creating dynamic code demonstration videos. It transforms static code into lively animations that simulate real programming processes.

Core Concepts
-------------

Code Animation
^^^^^^^^^^^^^^

CodeVideoRenderer's core functionality is to animate code character by character and line by line. Unlike traditional static code displays, it can:

* **Simulate typing process**: Display code character by character, simulating real programming experience
* **Intelligent cursor tracking**: Camera automatically follows the cursor movement, ensuring the currently edited code stays in the center of view
* **Syntax highlighting support**: Integrates Pygments syntax highlighting engine, supporting multiple programming languages

Camera System
^^^^^^^^^^^^^

The library includes an intelligent camera system that can:

* **Auto-scaling**: Automatically adjust camera zoom based on code content
* **Smooth movement**: Camera smoothly follows cursor movement, avoiding abrupt jumps
* **Focus management**: Intelligently recognizes code structure to ensure important parts remain visible

Key Features
------------

* **🎬 Professional animation effects**: Based on Manim engine, providing high-quality animation rendering
* **📝 Multi-language support**: Syntax highlighting for various programming languages including Python, JavaScript, Java, and more
* **⚙️ Highly customizable**: Adjustable typing speed, line spacing, camera behavior, and other parameters
* **🎨 Rich styling**: Multiple code highlighting styles (such as github-dark, monokai, etc.)
* **🔧 Dual renderers**: Support for both Cairo and OpenGL rendering backends

Use Cases
---------

CodeVideoRenderer is particularly suitable for the following application scenarios:

* **Educational demonstrations**: Create code explanation videos for programming courses
* **Technical presentations**: Make code demonstration segments for conference talks
* **Algorithm visualization**: Dynamically showcase algorithm implementation processes and logic
* **Code review**: Visualize code modifications and refactoring processes

Design Philosophy
-----------------

CodeVideoRenderer's design philosophy is "making code come alive," aiming to better convey programming ideas and code logic through animation. It's not just a code rendering tool, but a code storytelling tool.

Index
-----

.. toctree::
   :maxdepth: 2
   :caption: Documentation

   examples
   installation
   tutorials
   reference
   faq
   migration
   changelog
   contributing
   code_of_conduct

.. toctree::
   :maxdepth: 1
   :caption: External Links
   
   GitHub Repository <https://github.com/ExploreMaths/CodeVideoRenderer>
   PyPI Package <https://pypi.org/project/codevideorenderer/>