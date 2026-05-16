CameraFollowCursorCV
====================

``CameraFollowCursorCV`` is the primary class for creating code typing animation videos. It handles code parsing, syntax highlighting, camera movement, and the full rendering pipeline.

Quick Example
-------------

.. code-block:: python

   from CodeVideoRenderer import CameraFollowCursorCV

   video = CameraFollowCursorCV(
       code=('string', 'print("Hello, World!")'),
       language='python',
       video_name='HelloWorld'
   )
   video.render()

Constructor Parameters
----------------------

The following table summarizes the parameters accepted by the constructor. For the complete signature, see the API reference below.

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Parameter
     - Default
     - Description
   * - ``code``
     - *required*
     - A tuple ``('string', code_str)`` or ``('file', file_path)``.
   * - ``language``
     - *required*
     - Programming language for syntax highlighting (e.g. ``'python'``, ``'javascript'``).
   * - ``formatter_style``
     - ``"material"``
     - Pygments style name (e.g. ``"github-dark"``, ``"monokai"``).
   * - ``line_spacing``
     - ``0.8``
     - Vertical spacing between code lines.
   * - ``interval_range``
     - ``(0.15, 0.15)``
     - Min/max seconds between typed characters.
   * - ``camera_scale``
     - ``0.5``
     - Initial camera zoom level.
   * - ``video_name``
     - ``"CameraFollowCursorCV"``
     - Base name of the output MP4 file (without extension).
   * - ``renderer``
     - ``"cairo"``
     - Rendering backend: ``"cairo"`` (CPU) or ``"opengl"`` (GPU).

Output
------

After calling :meth:`~.render`, the final video is saved as an MP4 file. The default location follows Manim's output convention:

.. code-block:: text

   ./media/videos/1080p60/{video_name}.mp4

The exact sub-directory (e.g. ``1080p60``) depends on Manim's quality configuration. The file name is determined by the ``video_name`` parameter you passed to the constructor.

Full API Reference
------------------

.. autoclass:: CodeVideoRenderer.renderer.CameraFollowCursorCV
    :members:
    :undoc-members:
    :private-members:
    :special-members: __getattribute__
