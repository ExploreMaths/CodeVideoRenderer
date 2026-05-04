Changelog
=========

This document records all notable changes to CodeVideoRenderer.

.. seealso::

   * :doc:`installation` for upgrade instructions
   * `GitHub releases <https://github.com/ExploreMaths/CodeVideoRenderer/releases>`_ for detailed change information
   * :doc:`contributing` for information on reporting issues

CodeVideoRenderer 1.2.3 :bdg-success-line:`Latest`
------------------------------------------------------------------------

**Date**: May 4, 2026

See details at https://pypi.org/project/codevideorenderer/1.2.3/.

.. admonition:: What's Changed
   :class: tip

   **Additions 🚀**

   * Added ``moviepy`` version requirement ``<2.0.0`` for Python 3.8
   * Added ``typing-extensions`` dependency with a minimum required version of ``4.0.0``
   * Added ``imageio-ffmpeg`` dependency with a minimum required version of ``0.4.0``
   * Added ``typeguard`` dependency with a minimum required version of ``3.0``
   * Added import of ``annotations`` (from ``__future__``) in ``typing.py`` and ``utils.py`` for compatibility with Python 3.8, 3.9

   **Changes 🧹**
   
   * Downgraded the minimum required version of the ``manim`` dependency from ``0.20.1`` to ``0.18.0``
   * Downgraded the minimum required version of the ``numpy`` dependency from ``2.4.2`` to ``1.24.4``
   * Downgraded the minimum required version of the ``pillow`` dependency from ``11.2.1`` to ``9.1``
   * Downgraded the minimum required Python version from ``3.9`` to ``3.8``
   * Modified the import methods of ``TypeAlias``, ``UnionType`` and ``VideoFileClip`` for compatibility with Python 3.8, 3.9
   * Replaced all type annotations in the format of ``type | type`` with ``Union[type, type]`` for compatibility with Python 3.8, 3.9
   * Changed all ``PathLike[str]`` to ``PathLike`` (as ``PathLike`` in Python 3.8 does not support generics)
   * Replaced all type annotations in the formats of ``tuple[...]``, ``list[...]`` and ``dict[...]`` with ``Tuple[...]``, ``List[...]`` and ``Dict[...]`` respectively for compatibility with Python 3.8
   * Switched the type checker from :func:`typeChecker` to :func:`typeguard.typechecked`

   **Deletions 🗑️**

   * Removed :func:`checkType` and :func:`typeChecker` from ``utils.py``

CodeVideoRenderer 1.2.2
------------------------------------------------------------------------

**Date**: Apr 27, 2026

See details at https://pypi.org/project/codevideorenderer/1.2.2/.

.. admonition:: What's Changed
   :class: tip

   **Changes 🧹**
   
   * Convert all documents (functions, classes, constants) to the reStructuredText format for better compatibility with Sphinx documentation.

   * Change the default value of the ```formatter_style``` parameter in the :class:`~.CameraFollowCursorCV` class to ```"material"```.

CodeVideoRenderer 1.2.1
----------------------------

**Date**: Mar 22, 2026

See details at https://pypi.org/project/codevideorenderer/1.2.1/.

.. admonition:: What's Changed
   :class: tip

   **Additions 🚀**

   * Add the :data:`~.__version__` variable to ```__init__.py```
   
   * Add the :data:`~.__all__` variable to ```config.py```, ```renderer.py```, ```typing.py```, and ```utils.py```
   
   * Add the :attr:`~.formatter_style` parameter to the :class:`~.CameraFollowCursorCV` class
   
   * Add beautification for terminal error messages
   
   * Add parameter descriptions and type annotations for all functions and classes
   
   * Add the :meth:`~.__getattribute__` function to the :class:`~.CameraFollowCursorCV` class to prevent data modification by changing attributes
   
   * Add the CodeVideoRendererFont font to support Chinese characters
   
   * Add the :data:`~.NOT_AVAILABLE_CHARACTERS` variable to ```config.py```
   
   * Add the :class:`~.Parameters` class to the :class:`~.CameraFollowCursorCV` class for managing and retrieving parameters

   * Add ```version.py``` to manage package version


   **Changes 🧹**

   * Change the function name format from ```aaa_bbb``` (snake_case) to ```aaaBbb``` (camelCase)
   
   * Change the :data:`~.PygmentsLanguage` class to a ```Literal``` type
   
   * Refactor the ```default_progress_bar``` function into the :class:`~.DefaultProgressBar` class
   
   * Split ```CameraFollowCursorCVR.py``` into ```renderer.py```, ```typing.py```, and ```utils.py```
   
   * Modify the whitespace handling logic to improve rendering speed
   
   * Make partial modifications to the parameters and descriptions of the :class:`~.CameraFollowCursorCV` class
   
   * Modify some terminal output content
   
   * Update the value of :data:`~.CODE_OFFSET` in ```config.py```


   **Fixes 🐛**

   * Fix the code offset issue caused by `@gaojj2000 <https://github.com/gaojj2000>`_ in `#5 <https://github.com/ExploreMaths/CodeVideoRenderer/pull/5>`_
   * Fix the ```code_line_rectangle``` offset issue that occurs when code offset happens


   **Deletions 🗑️**

   * Remove the :data:`~.DEFAULT_CODE_FORMATTER_STYLE`, :data:`~.AVAILABLE_CHARACTERS`, and :data:`~.EMPTY_CHARACTER` variables from ```config.py```

CodeVideoRenderer 1.1.2
----------------------------

**Date**: Feb 11, 2026

See details at https://pypi.org/project/codevideorenderer/1.1.2/.

.. admonition:: What's Changed
   :class: tip

   * Fixed the cursor position error caused by manim uniformly removing leading spaces on each line (see `#5 <https://github.com/ExploreMaths/CodeVideoRenderer/pull/5>`_ for details).

CodeVideoRenderer 1.1.1
----------------------------

**Date**: Feb 11, 2026

See details at https://pypi.org/project/codevideorenderer/1.1.1/.

.. admonition:: What's Changed
   :class: tip

   * Added compatibility updates for ```manim==0.19.1``` (see `#3 <https://github.com/ExploreMaths/CodeVideoRenderer/pull/3>`_ for details).

   * Modified :func:`~.type_checker` to adapt to ```Literal``` and :data:`~.PygmentsLanguage`.

   * Optimized terminal display.

   * Added glow effects.

   * Integrated ```functions.py``` into ```CameraFollowCursorCVR.py```.

   * Adapted to OpenGL rendering and resolved related issues when switching to OpenGL rendering (see `#4 <https://github.com/ExploreMaths/CodeVideoRenderer/pull/4>`_ for details).

   * Added the ```renderer``` parameter to :class:`~.CameraFollowCursorCV` to configure the renderer.

   * Adopted the ```timeit``` module to calculate rendering time and eliminate redundant variables.

   * Removed summary output before rendering the ```Scene```.

   * Deleted unused constants in ```config.py```.

   * Changed the type of the ```language``` parameter in :class:`~.CameraFollowCursorCV` from ```str``` to :data:`~.PygmentsLanguage`.

   * Refactored the file structure.

CodeVideoRenderer 1.1.0
----------------------------

**Date**: Dec 25, 2025

See details at https://pypi.org/project/codevideorenderer/1.1.0/.

.. admonition:: What's Changed
   :class: tip

   * Revised camera movement logic.

   * Added opening animation.

   * Fixed the issue where output could not be terminated when ```output=False``` was used in :meth:`~.render`.

CodeVideoRenderer 1.0.9.post2
------------------------------

**Date**: Nov 24, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.9.post2/.

.. admonition:: What's Changed
   :class: tip

   * Adjusted the spacing between the cursor and characters.

CodeVideoRenderer 1.0.9.post1
------------------------------

**Date**: Nov 17, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.9.post1/.

.. admonition:: What's Changed
   :class: tip

   * Fixed partial issues with the :func:`~.type_checker` decorator.

   * Redesigned progress bar style and added a ```{task.completed}/{task.total}``` field.

CodeVideoRenderer 1.0.9
----------------------------

**Date**: Nov 16, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.9/.

.. admonition:: What's Changed
   :class: tip

   * Overhauled and rewrote camera movement logic, and added automatic camera scaling.

   * Used ```rich``` to print initial data at the start of rendering.

   * Rewrote the rendering progress bar with ```rich.progress```.

   * Refactored type checking and adopted ```rich.traceback``` for cleaner error output.

CodeVideoRenderer 1.0.8.post1
--------------------------------

**Date**: Nov 8, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.8.post1/.

.. admonition:: What's Changed
   :class: tip

   * Fixed issues in ```__init__.py```.

CodeVideoRenderer 1.0.8
----------------------------

**Date**: Nov 8, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.8/.

.. admonition:: What's Changed
   :class: tip

   * Fixed code offset errors.

   * Reverted the default font to Consolas, as Cascadia Code converts ```>=``` to ```≥``` and triggers internal Manim errors.

   * Removed unused constants in ```/renderer/config.py```.

CodeVideoRenderer 1.0.7.post3
--------------------------------

**Date**: Nov 6, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.7.post3/.

.. admonition:: What's Changed
   :class: tip

   * Re-uploaded complete source code due to incomplete package upload on pip.

CodeVideoRenderer 1.0.7.post2
---------------------------------

**Date**: Nov 6, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.7.post2/.

.. admonition:: What's Changed
   :class: tip

   * Fixed rendering errors triggered by blank lines at the start of code content.

   * Disabled Manim caching to improve rendering speed.

CodeVideoRenderer 1.0.7.post1
--------------------------------

**Date**: Oct 3, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.7.post1/.

.. admonition:: What's Changed
   :class: tip

   * Resolved bugs occurring when using the ```code_file``` parameter.

CodeVideoRenderer 1.0.7
----------------------------

**Date**: Oct 3, 2025
   
See details at https://pypi.org/project/codevideorenderer/1.0.7/.

.. admonition:: What's Changed
   :class: tip

   * Updated pip dependency configuration.

   * Changed parameter ```camera_floating_maximum_value``` to ```camera_floating_max_value```, ```screen_scale``` to ```camera_scale```.

   * Improved error message presentation.

CodeVideoRenderer 1.0.6
----------------------------

**Date**: Sep 27, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.6/.

.. admonition:: What's Changed
   :class: tip

   * Fixed progress bar formatting errors caused by overly long code lines.

   * Refactored the renderer module: optimized the structure and error handling of CodeVideoRenderer (see `#1 <https://github.com/ExploreMaths/CodeVideoRenderer/pull/1>`_ for details).

CodeVideoRenderer 1.0.5.post2
---------------------------------

**Date**: Sep 25, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.5.post2/.

.. admonition:: What's Changed
   :class: tip

   * Fixed version compatibility issues of pip dependencies to ensure full compliance with project requirements.

   * Resolved inconsistent color display of ANSI escape sequences in rendering outputs across different terminals/compilers.

CodeVideoRenderer 1.0.5.post1
-------------------------------

**Date**: Sep 23, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.5.post1/.

.. admonition:: What's Changed
   :class: tip

   * Fixed pip installation failures.

CodeVideoRenderer 1.0.5
----------------------------

**Date**: Sep 20, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.5/.

.. admonition:: What's Changed
   :class: tip

   * Added the new ```output``` parameter to the :meth:`~.render` method to control rendering output behavior.

   * Refactored ```CodeVideo``` from a function to a class for better code maintainability and scalability.

CodeVideoRenderer 1.0.4
----------------------------

**Date**: Sep 6, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.4/.

.. admonition:: What's Changed
   :class: tip

   * Fixed calculation errors of rendering duration.

   * Removed the deprecated ```font``` parameter.

   * Optimized terminal rendering logs.

   * Improved overall code execution efficiency.

CodeVideoRenderer 1.0.3
----------------------------

**Date**: Aug 29, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.3/.

.. admonition:: What's Changed
   :class: tip

   * Fixed the issue where the cursor failed to pause at the start of new lines.

   * Excluded leading and trailing whitespace of each code line from animation playback to reduce redundant animation duration.

   * Adjusted the background width of the currently highlighted code line.

   * Added the new ```line_spacing``` parameter to customize line spacing.

   * Optimized terminal rendering information output.

   * Fine-tuned camera movement logic.

CodeVideoRenderer 1.0.2
----------------------------

**Date**: Aug 26, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.2/.

CodeVideoRenderer 1.0.1.2
----------------------------

**Date**: Aug 23, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.1.2/.

CodeVideoRenderer 1.0.1.1
----------------------------

**Date**: Aug 22, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.1.1/.

CodeVideoRenderer 1.0.1.0
----------------------------

**Date**: Aug 19, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.1.0/.

CodeVideoRenderer 1.0.0.5
----------------------------

**Date**: Aug 18, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.0.5/.

CodeVideoRenderer 1.0.0.4
----------------------------

**Date**: Aug 17, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.0.4/.

CodeVideoRenderer 1.0.0.3
----------------------------

**Date**: Aug 16, 2025

No information available.

CodeVideoRenderer 1.0.0.2
----------------------------

**Date**: Aug 16, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.0.2/.

CodeVideoRenderer 1.0.0.1
----------------------------

**Date**: Aug 16, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.0.1/.

CodeVideoRenderer 1.0.0.0
----------------------------

**Date**: Aug 15, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.0.0/.
