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

    # Create a simple code animation
    renderer = CameraFollowCursorCV(
        code=('string', '''def hello_world():
        print("Hello, World!")
        return True'''),
        language='python',
        formatter_style='github-dark'
    )

    renderer.render()

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

   renderer = CameraFollowCursorCV(
       code=('string', 'your_code_here'),
       language='python',
       interval_range=(0.05, 0.1),  # Fast typing
       # interval_range=(0.2, 0.5),  # Slow, deliberate typing
   )

Working with Files
^^^^^^^^^^^^^^^^^^

Animate code from existing files:

.. code-block:: python

   renderer = CameraFollowCursorCV(
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
   renderer = CameraFollowCursorCV(
       code=('string', 'code'),
       language='python',
       formatter_style='monokai'
   )

Camera Configuration
^^^^^^^^^^^^^^^^^^^^

Adjust camera behavior for different code sizes:

.. code-block:: python

   renderer = CameraFollowCursorCV(
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

Performance Optimization
^^^^^^^^^^^^^^^^^^^^^^^^

* **Use OpenGL**: For faster rendering on supported systems
* **Batch Processing**: Render multiple videos in sequence
* **Resolution**: Choose appropriate resolution for your needs

Troubleshooting Common Issues
------------------------------

See the :doc:`reference` section for detailed API documentation and troubleshooting tips.
