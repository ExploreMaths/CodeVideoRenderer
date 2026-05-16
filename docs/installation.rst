Installation
============

CodeVideoRenderer can be installed using pip, the Python package manager.

Prerequisites
-------------

Before installing CodeVideoRenderer, ensure you have the following:

* **Python 3.8 or higher**
* **pip** (Python package installer)
* **FFmpeg** (for video rendering)

We strongly recommend installing inside a virtual environment because Manim (a heavy dependency) may conflict with other packages in your global Python environment.

.. code-block:: bash

   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

Installing FFmpeg
^^^^^^^^^^^^^^^^^

.. tab-set::

   .. tab-item:: Windows

      .. code-block:: bash

         winget install ffmpeg

   .. tab-item:: macOS

      .. code-block:: bash

         brew install ffmpeg

   .. tab-item:: Linux

      .. code-block:: bash

         sudo apt update
         sudo apt install ffmpeg

Verifying FFmpeg
^^^^^^^^^^^^^^^^

After installation, confirm FFmpeg is available in your ``PATH``:

.. code-block:: bash

   ffmpeg -version

You should see version information printed. If you get a "command not found" error, restart your terminal or add FFmpeg to your system ``PATH`` before continuing.

Basic Installation
------------------

Install CodeVideoRenderer using pip:

.. code-block:: bash

   pip install codevideorenderer

Development Installation
------------------------

To install from source for development:

.. code-block:: bash

   git clone https://github.com/ExploreMaths/CodeVideoRenderer.git
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