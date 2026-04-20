Installation
============

CodeVideoRenderer can be installed using pip, the Python package manager.

Prerequisites
-------------

Before installing CodeVideoRenderer, ensure you have the following:

* **Python 3.8 or higher**
* **pip** (Python package installer)
* **FFmpeg** (for video rendering)

Installing FFmpeg
^^^^^^^^^^^^^^^^^

**Windows:**

1. Download FFmpeg from https://ffmpeg.org/download.html
2. Extract to a folder (e.g., ``C:\\ffmpeg``)
3. Add to PATH: ``System Properties > Environment Variables > Path > Edit > Add``

**macOS:**

.. code-block:: bash

   brew install ffmpeg

**Linux (Ubuntu/Debian):**

.. code-block:: bash

   sudo apt update
   sudo apt install ffmpeg

Basic Installation
------------------

Install CodeVideoRenderer using pip:

.. code-block:: bash

   pip install codevideorenderer

Installation with Extras
------------------------

For additional features, install with optional dependencies:

.. code-block:: bash

   # Install with OpenGL support
   pip install codevideorenderer[opengl]
   
   # Install with all extras
   pip install codevideorenderer[all]

Development Installation
------------------------

To install from source for development:

.. code-block:: bash

   git clone https://github.com/yourusername/CodeVideoRenderer.git
   cd CodeVideoRenderer
   pip install -e .

Verifying Installation
----------------------

Test your installation:

.. code-block:: python

   import CodeVideoRenderer
   print(CodeVideoRenderer.__version__)

Troubleshooting
---------------

Common installation issues:

* **ModuleNotFoundError**: Ensure you're using Python 3.8+
* **FFmpeg not found**: Verify FFmpeg is installed and in PATH
* **Permission errors**: Use ``pip install --user`` or virtual environment

Next Steps
----------

After installation, proceed to the :doc:`tutorials` section to start using CodeVideoRenderer.

.. seealso::
   :doc:`tutorials` for getting started guides
   :doc:`examples` for code examples
   :doc:`reference` for API documentation