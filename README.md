<p align=center>
	<img alt="logo" src="https://github.com/user-attachments/assets/e28c0ce7-2962-4487-a347-029f3a7ed2ff" width="400" alt="CodeVideoRenderer" />
</p>

<h3><p align=center>A Python library for rendering dynamic code videos based on Manim</p></h3>

CodeVideoRenderer is a Python animation library specifically designed for creating dynamic code demonstration videos. It transforms static code into lively animations that simulate real programming processes.

[![Documentation Status](https://readthedocs.org/projects/CodeVideoRenderer/badge/?version=latest)](https://CodeVideoRenderer.readthedocs.io/)
[![Last Commit](https://img.shields.io/github/last-commit/ExploreMaths/CodeVideoRenderer.svg?style=flat-square)](https://github.com/ExploreMaths/CodeVideoRenderer/commits/main)
[![Repo Size](https://img.shields.io/github/repo-size/ExploreMaths/CodeVideoRenderer.svg?style=flat-square)](https://github.com/ExploreMaths/CodeVideoRenderer)
[![Python Versions](https://img.shields.io/pypi/pyversions/codevideorenderer.svg?style=flat-square)](https://pypi.org/project/codevideorenderer/)
[![PyPI Version](https://img.shields.io/pypi/v/codevideorenderer.svg?style=flat-square)](https://pypi.org/project/codevideorenderer/)
[![Python package](https://github.com/ExploreMaths/CodeVideoRenderer/actions/workflows/python-package.yml/badge.svg)](https://github.com/ExploreMaths/CodeVideoRenderer/actions/workflows/python-package.yml)
[![PyPI Downloads](https://img.shields.io/pypi/dm/codevideorenderer.svg?style=flat-square)](https://pypi.org/project/codevideorenderer/)

## ✨ Core Features

- **🎬 Professional animation effects**: Based on Manim engine, providing high-quality animation rendering
- **📝 Multi-language support**: Syntax highlighting for various programming languages including Python, JavaScript, Java, and more
- **⚙️ Highly customizable**: Adjustable typing speed, line spacing, camera behavior, and other parameters
- **🎨 Rich styling**: Multiple code highlighting styles, plus a built-in **VS Code Dark+** theme (`vscode-dark-plus`, the default)
- **🔧 Dual renderers**: Support for both Cairo and OpenGL rendering backends
- **🧹 Clear-code animation**: Delete the code backspace-style (speed-adjustable) or fade it out after typing finishes (`clear_code=True`)
- **💡 VS Code-style autocomplete**: IntelliSense-style popups with colored icons, labels, details and a selection highlight (`autocomplete=True`)
- **🇨🇳 Chinese IME simulation**: Pinyin (hyphen-separated) + candidate box pops up when Chinese characters are typed (`chinese_ime=True`)
- **🎨 Theme & layout**: Customisable background color and current-line highlight color
- **🎞️ Video post-processing**: Strip/add subtitles, mix background music, concatenate clips, set quality/resolution/fps, add watermarks, title cards and cover images

## 🚀 Quick Installation

### Prerequisites

* **Python 3.8+**
* **FFmpeg** (required for video rendering)

Install FFmpeg first if you haven't:

```bash
# Windows
winget install ffmpeg

# macOS
brew install ffmpeg

# Linux
sudo apt update && sudo apt install ffmpeg
```

### Install from PyPI

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
    formatter_style='vscode-dark-plus',
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

## 🎞️ Video Post-processing

After rendering, use the built-in helpers to finish your video. Every function accepts an
input path and an optional output path (a sensible name is derived if omitted), and returns
the output path.

```python
from CodeVideoRenderer import (
    remove_subtitles, add_subtitles, add_background_music, concat_videos,
    set_quality, add_watermark, add_title_card, extract_cover,
    extract_audio, remove_audio, trim_video, change_speed,
)

video = "FibonacciExample.mp4"

remove_subtitles(video)                       # strip subtitle streams  -> *_no_subs.mp4
add_subtitles(video, "captions.srt")          # burn subtitles in        -> *_subbed.mp4
add_subtitles(video, "captions.srt", soft=True)  # switchable soft subs
add_background_music(video, "bgm.mp3", volume=0.3)   # mix music        -> *_bgm.mp4
concat_videos(["part1.mp4", "part2.mp4"], "full.mp4")
set_quality(video, resolution="1080p", fps=60, crf=20)  # re-encode     -> *_quality.mp4
trim_video(video, start=1.0, duration=5.0)
change_speed(video, speed=2.0)
add_watermark(video, text="MyChannel", position="bottom-right")
add_watermark(video, image_path="logo.png", opacity=0.5)
add_title_card(video, title="Hello World", subtitle="A code demo", duration=3.0)
extract_cover(video, time=1.0, width=1280)    # thumbnail              -> *_cover.png
extract_audio(video, format="mp3")            # audio only             -> *.mp3
remove_audio(video)                           # silent video           -> *_mute.mp4
```

> **FFmpeg**: these helpers shell out to `ffmpeg`. It is located automatically via the
> `CODEVIDEORENDERER_FFMPEG` / `FFMPEG_BINARY` environment variables, `PATH`, common install
> locations, or the binary bundled with `imageio-ffmpeg`.

### Clear code after typing

Pass `clear_code=True` to delete the code once typing completes. Two modes are available:

```python
video = CameraFollowCursorCV(
    code=('string', code),
    language='python',
    video_name='FibonacciExample',

    clear_code=True,                 # delete the code after typing
    clear_code_mode='backspace',     # 'backspace' (逐字符删除) or 'fade' (整块淡出)
    clear_code_interval=0.03,        # 每个字符的删除间隔（控制删除速度）
    clear_code_run_time=1.0,         # fade 模式的时长 / backspace 模式下收尾的时长
)
```

### VS Code-style autocomplete

Enable `autocomplete=True` to pop up a completion box (just like IntelliSense) whenever
a keyword such as `def`, `import`, `class`, `for`, `return` … is typed. The popup mirrors
VS Code's suggest widget: **colored symbol icons** (method `ƒ`, class `▣`, keyword `⚿`,
snippet `➤`, …), labels, grey type details, and the blue selected-row highlight.

```python
video = CameraFollowCursorCV(
    code=('string', code),
    language='python',
    video_name='AutocompleteDemo',
    autocomplete=True,          # 触发关键词时弹出补全提示
    autocomplete_wait_time=0.6, # 提示框停留时长（秒）
)
```

### VS Code Dark+ syntax highlighting

The default `formatter_style` is `vscode-dark-plus`, a faithful port of the VS Code Dark+
theme (keywords `#569CD6` / `#C586C0`, strings `#CE9178`, functions `#DCDCAA`, classes
`#4EC9B0`, comments `#6A9955`, numbers `#B5CEA8`). Pass it explicitly, or use any other
Pygments style such as `github-dark` or `monokai`.

### Chinese IME simulation

Set `chinese_ime=True` to pop up a pinyin + candidate box (like Microsoft Pinyin) whenever
a Chinese character is typed — multi-character words are shown as **hyphen-separated
pinyin** (`世界` → `shi-jie`):

```python
video = CameraFollowCursorCV(
    code=('string', code),
    language='python',
    video_name='ChineseDemo',
    chinese_ime=True,       # 输入中文时弹出拼音候选框
    ime_wait_time=0.6,      # 候选框停留时长（秒）
)
```

### Theme & layout

```python
video = CameraFollowCursorCV(
    ...,
    background_color="#1E1E1E",       # 背景色
    line_highlight_color="#2D2D2D",   # 当前行高亮色
    end_wait_time=2.0,                # 结尾停留时长（秒）
)
```

## 🎯 Use Cases

- **Educational demonstrations**: Create code explanation videos for programming courses
- **Technical presentations**: Make code demonstration segments for conference talks
- **Algorithm visualization**: Dynamically showcase algorithm implementation processes and logic
- **Code review**: Visualize code modifications and refactoring processes

## 📚 Documentation

Full documentation and examples available at <https://codevideorenderer.readthedocs.io/>.

## 🤝 Contact Us

Found any issues? Please send them to my [163 email](mailto:zhuchongjing_pypi@163.com) or [Gmail email](mailto:github.exploremaths@gmail.com). We'll fix them as soon as possible.