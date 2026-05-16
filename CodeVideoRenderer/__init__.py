"""
CodeVideoRenderer – A Python animation library for creating dynamic code demonstration videos.

This package provides tools to transform static code into lively animations that simulate
real programming processes, built on top of the Manim engine.

Quick start
-----------

>>> from CodeVideoRenderer import CameraFollowCursorCV
>>> video = CameraFollowCursorCV(
...     code=('string', 'print("Hello, World!")'),
...     language='python',
...     video_name='HelloWorld'
... )
>>> video.render()

Modules
-------

* :mod:`~.renderer` — Core rendering engine (:class:`~.CameraFollowCursorCV`).
* :mod:`~.config` — Default constants and configuration values.
* :mod:`~.typing` — Type aliases used across the library.
* :mod:`~.utils` — Internal utility functions and helpers.
* :mod:`~.version` — Package version string.
"""
from .renderer import *
from .config import *
from .typing import *
from .utils import *
from .version import __version__