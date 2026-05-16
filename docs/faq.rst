FAQ & Troubleshooting
=====================

Frequently asked questions and common issues.

General Questions
-----------------

Where is the output video saved?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After calling ``render()``, the final MP4 is placed next to Manim's internal render output, using the name you provided via ``video_name``:

.. code-block:: text

   ./media/videos/1080p60/{video_name}.mp4

The exact sub-directory (e.g. ``1080p60``) depends on Manim's current quality configuration.

Cairo vs. OpenGL – which should I use?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* **Cairo** (default, ``renderer='cairo'``) – CPU-based, works on virtually all systems.
* **OpenGL** (``renderer='opengl'``) – GPU-based, can be faster but requires compatible graphics drivers.

If you encounter rendering errors with OpenGL, switch back to Cairo:

.. code-block:: python

   video = CameraFollowCursorCV(
       code=('string', 'code'),
       language='python',
       renderer='cairo'
   )

Does it support Chinese characters?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Yes. CodeVideoRenderer bundles ``CodeVideoRendererFont`` to support CJK characters. If you see garbled text, ensure your input code is valid UTF-8.

Common Issues
-------------

FFmpeg not found
^^^^^^^^^^^^^^^^

If rendering fails with an FFmpeg-related error, verify FFmpeg is installed and available in your ``PATH``:

.. code-block:: bash

   ffmpeg -version

If the command is not found, reinstall FFmpeg (see :doc:`installation`) and restart your terminal.

Invalid characters error
^^^^^^^^^^^^^^^^^^^^^^^^

CodeVideoRenderer rejects the following characters because they can break Manim's text layout:

* ``\r`` (carriage return)
* ``\v`` (vertical tab)
* ``\f`` (form feed)

If your code contains these (often copied from certain editors), replace them with regular spaces or newlines before passing the string to ``CameraFollowCursorCV``.

Code is cut off or too large
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If your code block overflows the visible area or the camera zoom feels wrong, adjust ``camera_scale``:

.. code-block:: python

   # Zoom out for large files
   video = CameraFollowCursorCV(
       code=('file', 'large_script.py'),
       language='python',
       camera_scale=0.3
   )

Values smaller than the default ``0.5`` zoom the camera out; larger values zoom in.

How do I suppress console output during rendering?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pass ``output=False`` to :meth:`~.render`:

.. code-block:: python

   video.render(output=False)

This disables progress bars and timing logs while still producing the video file.

Why does Manim caching not work?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

CodeVideoRenderer internally sets ``config.disable_caching = True`` to prevent stale cache files from interfering with the code-typing animation. This is intentional and not a bug.

Why is my code slightly misaligned vertically?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Certain characters (``acegmnopqrsuvwxyz+,-.:;<=>_~``) trigger a known Manim text-layout alignment bug. CodeVideoRenderer automatically applies a workaround offset (:data:`~.CODE_OFFSET`) for these characters. If you still see issues, try adjusting ``camera_scale`` or avoid those characters in critical positions.

Are tabs expanded? Can I change the tab size?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Yes — tabs are always expanded to spaces using a tab size of ``4`` (the :data:`~.DEFAULT_TAB_WIDTH` constant). Currently this value cannot be changed at runtime; if you need a different tab size, preprocess your code string before passing it to :class:`~.CameraFollowCursorCV`.

What happens if ``video_name`` is empty?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The constructor raises ``ValueError("video_name must be provided")`` if ``video_name`` is empty or falsy. Always provide a non-empty string.

Rendering is slow
^^^^^^^^^^^^^^^^^

* Try ``renderer='opengl'`` if you have a compatible GPU.
* Reduce the code length or split it into multiple shorter videos.
* Ensure you are not running inside a very slow virtual machine without GPU passthrough.
