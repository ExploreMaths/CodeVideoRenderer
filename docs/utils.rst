Utilities
=========

This module provides internal helper functions, video post-processing effects, and progress-bar utilities. Most users do not need to interact with these directly, but the public items are documented here for completeness.

String processing
-----------------

* :func:`~.stripEmptyLines` — Remove leading and trailing empty lines from a string.
* :func:`~.findSpacePositions` — Locate non-leading, non-trailing spaces in a multi-line string.
* :func:`~.replaceMiddleSpacesWithOccupyCharacter` — Replace middle spaces with a placeholder character used by Manim.

Video effects
-------------

* :func:`~.addGlowEffect` — Apply a soft-glow filter to a rendered video.

Progress bars
-------------

* :class:`~.DefaultProgressBar` — A ``rich`` progress bar used during rendering.
* :class:`~.RichProgressBarLogger` — A ``proglog`` logger that bridges to Rich progress bars.

Context managers
----------------

* :func:`~.noManimOutput` — Suppress Manim console output within a ``with`` block.

.. automodule:: CodeVideoRenderer.utils
    :members:
    :undoc-members: