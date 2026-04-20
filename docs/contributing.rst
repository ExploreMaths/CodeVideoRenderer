Contributing
============

We welcome contributions from the community! This guide will help you get started with contributing to CodeVideoRenderer.

Ways to Contribute
------------------

There are many ways to contribute:

* **Bug Reports**: Report issues you encounter
* **Feature Requests**: Suggest new features or improvements
* **Code Contributions**: Submit pull requests with code changes
* **Documentation**: Improve documentation and examples
* **Testing**: Help test new features and report bugs
* **Community Support**: Help other users in discussions

Getting Started
---------------

Development Environment Setup
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. **Fork the repository** on GitHub
2. **Clone your fork**:

   .. code-block:: bash

      git clone https://github.com/yourusername/CodeVideoRenderer.git
      cd CodeVideoRenderer

3. **Set up development environment**:

   .. code-block:: bash

      python -m venv venv
      source venv/bin/activate  # On Windows: venv\\Scripts\\activate
      pip install -e .[dev]

4. **Install pre-commit hooks**:

   .. code-block:: bash

      pre-commit install

Code Style Guidelines
---------------------

Python Code Style
^^^^^^^^^^^^^^^^^

* Follow **PEP 8** conventions
* Use **type hints** for all function signatures
* Write **docstrings** for all public functions and classes
* Keep functions focused and modular

Example:

.. code-block:: python

   def calculate_line_height(font_size: int, line_spacing: float) -> float:
       """Calculate line height based on font size and spacing.
       
       Args:
           font_size: The font size in points
           line_spacing: The line spacing multiplier
           
       Returns:
           The calculated line height
       """
       return font_size * line_spacing

Documentation Standards
^^^^^^^^^^^^^^^^^^^^^^^

* Use **reStructuredText** for documentation
* Include examples for all public APIs
* Keep documentation up to date with code changes
* Use meaningful commit messages

Testing
-------

Writing Tests
^^^^^^^^^^^^^

* Write tests for new features and bug fixes
* Use **pytest** for testing framework
* Aim for good test coverage
* Include both unit tests and integration tests

Example test:

.. code-block:: python

   def test_camera_follow_cursor():
       """Test camera follows cursor correctly."""
       renderer = CameraFollowCursorCV(('string', 'print("test")'), 'python')
       # Test implementation
       assert renderer.camera_behavior is not None

Running Tests
^^^^^^^^^^^^^

.. code-block:: bash

   # Run all tests
   pytest
   
   # Run with coverage
   pytest --cov=CodeVideoRenderer
   
   # Run specific test file
   pytest tests/test_renderer.py

Submitting Changes
------------------

Pull Request Process
^^^^^^^^^^^^^^^^^^^^

1. **Create a feature branch**:

   .. code-block:: bash

      git checkout -b feature/your-feature-name

2. **Make your changes** and commit them:

   .. code-block:: bash

      git add .
      git commit -m "Add feature: your feature description"

3. **Push to your fork**:

   .. code-block:: bash

      git push origin feature/your-feature-name

4. **Create a Pull Request** on GitHub

Pull Request Guidelines
^^^^^^^^^^^^^^^^^^^^^^^

* **One feature per PR**: Keep pull requests focused
* **Descriptive title**: Clearly describe what the PR does
* **Detailed description**: Explain the changes and why they're needed
* **Reference issues**: Link to related issues
* **Update documentation**: Include documentation changes if needed

Issue Reporting
---------------

When reporting issues, please include:

* **CodeVideoRenderer version**
* **Python version**
* **Operating system**
* **Error message** and stack trace
* **Steps to reproduce** the issue
* **Expected behavior** vs actual behavior

Example issue template:

.. code-block:: markdown

   ## Description
   Brief description of the issue
   
   ## Steps to Reproduce
   1. Step one
   2. Step two
   3. Step three
   
   ## Expected Behavior
   What you expected to happen
   
   ## Actual Behavior
   What actually happened
   
   ## Environment
   - CodeVideoRenderer version: X.X.X
   - Python version: X.X.X
   - OS: Windows/macOS/Linux

Feature Requests
----------------

When suggesting new features:

* **Explain the problem** you're trying to solve
* **Describe your proposed solution**
* **Provide use cases** and examples
* **Consider alternatives** you've explored

Community Guidelines
--------------------

* Be respectful and inclusive
* Help others when you can
* Provide constructive feedback
* Follow the :doc:`code_of_conduct`

Recognition
-----------

Contributors will be recognized in:

* **GitHub contributors list**
* **Release notes**
* **Documentation credits**

Getting Help
------------

If you need help with contributing:

* **Check existing documentation** and issues
* **Ask in GitHub discussions**
* **Join the community chat** (if available)
* **Contact maintainers** for guidance

.. seealso::
   :doc:`code_of_conduct` for community guidelines
   :doc:`installation` for development setup
   GitHub repository for current issues and discussions