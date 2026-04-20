Plugins
=======

CodeVideoRenderer supports a plugin system that allows extending its functionality with custom components and integrations.

Overview
--------

The plugin system enables:

* **Custom syntax highlighters** for additional languages
* **Alternative camera behaviors** and movement patterns
* **Export formats** beyond standard video output
* **Integration with other tools** and frameworks

Built-in Plugins
----------------

Currently Available Plugins
^^^^^^^^^^^^^^^^^^^^^^^^^^^

CodeVideoRenderer comes with the following built-in plugins:

Syntax Highlighting Plugins
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Pygments Integration**: Default syntax highlighting engine
* **Language Support**: Python, JavaScript, Java, C++, and more
* **Style Themes**: Multiple color schemes (github-dark, monokai, etc.)

Camera Plugins
~~~~~~~~~~~~~~

* **FollowCursorCamera**: Default cursor-following behavior
* **AutoZoomCamera**: Automatic zoom adjustment based on content
* **SmoothPanCamera**: Smooth panning transitions

Creating Custom Plugins
-----------------------

Plugin Structure
^^^^^^^^^^^^^^^^

A basic plugin consists of:

.. code-block:: python

   from CodeVideoRenderer.plugins import BasePlugin

   class MyCustomPlugin(BasePlugin):
       """Example custom plugin."""
       
       def __init__(self, config=None):
           super().__init__(config)
           
       def setup(self, renderer):
           """Initialize plugin with renderer instance."""
           self.renderer = renderer
           
       def process_code(self, code):
           """Process code before animation."""
           return code
           
       def before_render(self):
           """Hook called before rendering starts."""
           pass
           
       def after_render(self):
           """Hook called after rendering completes."""
           pass

Syntax Highlighter Plugin
^^^^^^^^^^^^^^^^^^^^^^^^^

Create custom syntax highlighting for new languages:

.. code-block:: python

   from pygments.lexers import get_lexer_by_name
   from pygments.formatters import HtmlFormatter

   class CustomLanguagePlugin(BasePlugin):
       def __init__(self, language_name):
           self.language_name = language_name
           
       def setup(self, renderer):
           # Register custom language
           renderer.register_language(self.language_name, self.highlight_code)
           
       def highlight_code(self, code):
           lexer = get_lexer_by_name(self.language_name)
           formatter = HtmlFormatter(style='monokai')
           return highlight(code, lexer, formatter)

Camera Behavior Plugin
^^^^^^^^^^^^^^^^^^^^^^

Implement custom camera movement patterns:

.. code-block:: python

   class SmoothScrollCameraPlugin(BasePlugin):
       def __init__(self, scroll_speed=0.1):
           self.scroll_speed = scroll_speed
           
       def setup(self, renderer):
           renderer.camera_behavior = self.custom_camera_behavior
           
       def custom_camera_behavior(self, cursor_position, code_lines):
           # Implement custom camera logic
           return smooth_scroll_to(cursor_position, self.scroll_speed)

Using Plugins
-------------

Loading Plugins
^^^^^^^^^^^^^^^

Plugins can be loaded in several ways:

Programmatic Loading
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from CodeVideoRenderer import CameraFollowCursorCV
   from my_plugins import CustomLanguagePlugin

   renderer = CameraFollowCursorCV(
       code=('string', 'code'),
       language='python'
   )
   
   # Load plugin
   plugin = CustomLanguagePlugin('my_language')
   renderer.load_plugin(plugin)

Configuration File
~~~~~~~~~~~~~~~~~~

Create a configuration file (e.g., ``config.yaml``):

.. code-block:: yaml

   plugins:
     - my_plugins.CustomLanguagePlugin:
         language_name: "custom_lang"
     - my_plugins.SmoothScrollCameraPlugin:
         scroll_speed: 0.15

Then load from configuration:

.. code-block:: python

   renderer.load_plugins_from_config('config.yaml')

Plugin Development Tips
-----------------------

Best Practices
^^^^^^^^^^^^^^

* **Keep plugins focused**: Each plugin should handle one specific task
* **Use configuration**: Make plugins configurable for flexibility
* **Handle errors gracefully**: Implement proper error handling
* **Document thoroughly**: Provide clear documentation for your plugin

Testing Plugins
^^^^^^^^^^^^^^^

.. code-block:: python

   import unittest
   from CodeVideoRenderer.plugins import BasePlugin
   from CodeVideoRenderer import CameraFollowCursorCV

   class TestMyPlugin(unittest.TestCase):
       def test_plugin_initialization(self):
           plugin = MyCustomPlugin()
           renderer = CameraFollowCursorCV(...)
           plugin.setup(renderer)
           # Test plugin functionality

Community Plugins
-----------------

We welcome community contributions! Share your plugins:

* **GitHub Repository**: Submit pull requests with your plugins
* **Documentation**: Add your plugin to the community plugins list
* **Examples**: Provide usage examples and demos

Available Community Plugins
^^^^^^^^^^^^^^^^^^^^^^^^^^^

*Check the GitHub repository for community-contributed plugins.*

.. seealso::
   :doc:`contributing` for guidelines on plugin development
   :doc:`examples` for plugin usage examples
   GitHub repository for community plugins