Reference Manual
================

This reference manual details modules, functions, and variables included in CodeVideoRenderer, describing what they are and what they do. For learning how to use CodeVideoRenderer, see :doc:`tutorials`. For a list of changes since the last release, see the :doc:`changelog`.

.. seealso::
    
    * :doc:`tutorials` for practical usage guides
    * :doc:`examples` for code examples
    * :doc:`installation` for setup instructions

Module Overview
---------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Module
     - Description
   * - :doc:`mainclass`
     - ``CameraFollowCursorCV`` – the main class for creating code animation videos.
   * - :doc:`config`
     - Default constants and configuration values (spacing, timing, fonts, offsets, etc.).
   * - :doc:`typing`
     - Type aliases and custom types used across the library (``PygmentsLanguage``, ``StrPath``, etc.).
   * - :doc:`utils`
     - Internal utility functions and helper classes for text processing, progress bars, and video post-processing.
   * - :doc:`version`
     - Package version string (``__version__``).

Index
-----

.. toctree::
   :maxdepth: 1

   mainclass
   config
   typing
   utils
   version