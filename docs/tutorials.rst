Tutorials & Guides
==================

This section contains step-by-step tutorials and comprehensive guides for using CodeVideoRenderer.

Getting Started
---------------

Quick Start Guide
^^^^^^^^^^^^^^^^^

Create your first code animation video:

.. code-block:: python

    from CodeVideoRenderer import CameraFollowCursorCV

    code = '''
    def hello_world():
        print("Hello, World!")
        return True
    '''

    # Create a simple code animation
    video = CameraFollowCursorCV(
        code=('string', code),
        language='python',
        formatter_style='github-dark'
    )

    video.render()

Basic Concepts
--------------

Understanding CodeVideoRenderer
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

CodeVideoRenderer works by:

1. **Parsing Code**: Reads and processes your code
2. **Syntax Highlighting**: Applies language-specific coloring
3. **Animation**: Creates typing animations character by character
4. **Camera Movement**: Smoothly follows the cursor

Core Components
^^^^^^^^^^^^^^^

* **CameraFollowCursorCV**: Main class for creating animations
* **Code Input**: Support for strings and files
* **Renderer Types**: Cairo (software) and OpenGL (hardware accelerated)

Intermediate Tutorials
----------------------

Customizing Animation Speed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Control the typing speed with interval ranges:

.. code-block:: python

   video = CameraFollowCursorCV(
       code=('string', 'your_code_here'),
       language='python',
       interval_range=(0.05, 0.1),  # Fast typing
       # interval_range=(0.2, 0.5),  # Slow, deliberate typing
   )

Working with Files
^^^^^^^^^^^^^^^^^^

Animate code from existing files:

.. code-block:: python

   video = CameraFollowCursorCV(
       code=('file', 'path/to/your/script.py'),
       language='python',
       video_name='MyScriptAnimation'
   )

Advanced Tutorials
------------------

Custom Styling
^^^^^^^^^^^^^^

Use different syntax highlighting styles:

.. code-block:: python

   # Available styles: github-dark, monokai, solarized-dark, etc.
   video = CameraFollowCursorCV(
       code=('string', 'code'),
       language='python',
       formatter_style='monokai'
   )

Camera Configuration
^^^^^^^^^^^^^^^^^^^^

Adjust camera behavior for different code sizes:

.. code-block:: python

   video = CameraFollowCursorCV(
       code=('string', 'large_code_block'),
       language='python',
       camera_scale=0.3,  # Zoom out for large files
       line_spacing=1.2   # Increase spacing for readability
   )

Best Practices
--------------

Code Preparation
^^^^^^^^^^^^^^^^

* **Clean Code**: Remove unnecessary comments and whitespace
* **Consistent Formatting**: Use consistent indentation
* **Reasonable Length**: Keep code blocks under 100 lines for optimal viewing

Switching to OpenGL
^^^^^^^^^^^^^^^^^^^

By default CodeVideoRenderer uses the Cairo (CPU) backend. If you have a compatible GPU, you can switch to OpenGL for faster rendering:

.. code-block:: python

   video = CameraFollowCursorCV(
       code=('string', 'your_code_here'),
       language='python',
       renderer='opengl'  # Use GPU acceleration
   )
   video.render()

.. note::

   OpenGL support depends on your graphics drivers and operating system. If rendering fails with OpenGL, fall back to ``renderer='cairo'`` (the default).

Controlling Console Output
^^^^^^^^^^^^^^^^^^^^^^^^^^

By default :meth:`~.render` prints progress bars and timing logs. To run silently:

.. code-block:: python

   video.render(output=False)

This is useful when rendering in CI/CD pipelines or batch scripts where console noise should be minimized.

Performance Optimization
^^^^^^^^^^^^^^^^^^^^^^^^

* **Use OpenGL**: For faster rendering on supported systems (see example above)
* **Batch Processing**: Render multiple videos in sequence
* **Resolution**: Choose appropriate resolution for your needs

Troubleshooting Common Issues
------------------------------

See the :doc:`faq` section for solutions to common problems (FFmpeg errors, invalid characters, slow rendering, etc.).
