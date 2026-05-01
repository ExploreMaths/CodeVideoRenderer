<p align=center>
	<img alt="logo" src="https://github.com/user-attachments/assets/e28c0ce7-2962-4487-a347-029f3a7ed2ff" width="400" alt="CodeVideoRenderer" />
</p>

<h3><p align=center>A Python library for rendering dynamic code videos based on Manim</p></h3>

CodeVideoRenderer is a Python animation library specifically designed for creating dynamic code demonstration videos. It transforms static code into lively animations that simulate real programming processes.

## ✨ Core Features

- **🎬 Professional animation effects**: Based on Manim engine, providing high-quality animation rendering
- **📝 Multi-language support**: Syntax highlighting for various programming languages including Python, JavaScript, Java, and more
- **⚙️ Highly customizable**: Adjustable typing speed, line spacing, camera behavior, and other parameters
- **🎨 Rich styling**: Multiple code highlighting styles (such as github-dark, monokai, etc.)
- **🔧 Dual renderers**: Support for both Cairo and OpenGL rendering backends

## 🚀 Quick Installation

```bash
pip install codevideorenderer
```

## 💡 Quick Start

```python
from CodeVideoRenderer import CameraFollowCursorCV

code = '''
def fibonacci(n):
    """Calculate the nth Fibonacci number"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Example usage
result = fibonacci(10)
print(f"Fibonacci(10) = {result}")
'''

video = CameraFollowCursorCV(
    code=('string', code),
    language='python',
    formatter_style='github-dark',
    video_name='FibonacciExample'
)
video.render()
```

## 📋 Main Features

### Code Animation
- **Simulate typing process**: Display code character by character, line by line
- **Intelligent cursor tracking**: Camera automatically follows cursor movement
- **Syntax highlighting support**: Integrates Pygments syntax highlighting engine

### Camera System
- **Auto-scaling**: Automatically adjust camera zoom based on code content
- **Smooth movement**: Camera smoothly follows cursor movement
- **Focus management**: Intelligently recognizes code structure to ensure important parts remain visible

## 🎯 Use Cases

- **Educational demonstrations**: Create code explanation videos for programming courses
- **Technical presentations**: Make code demonstration segments for conference talks
- **Algorithm visualization**: Dynamically showcase algorithm implementation processes and logic
- **Code review**: Visualize code modifications and refactoring processes

## 📚 Documentation

Full documentation and examples available at <https://codevideorenderer.readthedocs.io/>.

## 🤝 Contact Us

Found any issues? Please send them to [my email](mailto:zhuchongjing_pypi@163.com). We'll fix them as soon as possible.
