Configuration and constants
=====================================

This module contains all default constants and configuration values used by CodeVideoRenderer. You can import these constants to customize the rendering behavior, or pass your own values directly to :class:`~.CameraFollowCursorCV`.

Commonly customized constants
------------------------------

* :data:`~.DEFAULT_TAB_WIDTH` — Number of spaces used to expand tab characters (default: ``4``).
* :data:`~.DEFAULT_TYPE_INTERVAL` — Seconds between typed characters (default: ``0.15``).
* :data:`~.DEFAULT_LINE_SPACING` — Vertical spacing between code lines (default: ``0.8``).
* :data:`~.DEFAULT_CURSOR_BLINK_RUN_TIME` — Duration of the cursor blink animation (default: ``0.5``).
* :data:`~.CODE_OFFSET` — Vertical offset applied to code positioning (default: ``0.08``).
* :data:`~.NOT_AVAILABLE_CHARACTERS` — Characters that are rejected during rendering (``'\r\v\f'``).

.. automodule:: CodeVideoRenderer.config
    :members:
    :undoc-members: