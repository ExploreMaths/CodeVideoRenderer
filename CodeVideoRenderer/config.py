from manim import config
from rich.console import Console
import sys

# 原始标准输出和标准错误流
ORIGINAL_STDOUT = sys.stdout
"""Original standard output stream, used for console output."""
ORIGINAL_STDERR = sys.stderr
"""Original standard error stream, used for console error output."""
ORIGINAL_PROGRESS_BAR = config.progress_bar
"""Original progress bar, used for progress tracking."""

# 默认设置
DEFAULT_OUTPUT_VALUE = True
"""Default output value."""
DEFAULT_LINE_SPACING = 0.8
"""Default line spacing."""
DEFAULT_CURSOR_HEIGHT = 0.35
"""Default cursor height."""
DEFAULT_CURSOR_WIDTH = 1e-4
"""Default cursor width."""
DEFAULT_CODE_FONT = 'Consolas'
"""Default code font."""
DEFAULT_CURSOR_TO_CHAR_BUFFER = 0.07
"""Default buffer time between cursor movement and character rendering."""
DEFAULT_TYPE_INTERVAL = 0.15
"""Default typing interval."""
DEFAULT_LINE_BREAK_RUN_TIME = 0.4
"""Default line break animation run time."""
DEFAULT_TAB_WIDTH = 4
"""Default tab width."""
DEFAULT_OUTPUT_CONSOLE = Console(file=ORIGINAL_STDOUT)
"""Default output console."""
DEFAULT_CURSOR_BLINK_RUN_TIME = 0.5
"""Default cursor blink animation run time."""

# 其他设置
CODE_OFFSET = 0.08
"""Default offset for code rendering."""
NOT_AVAILABLE_CHARACTERS = '\r\v\f'
"""Characters that are not available for rendering."""
OCCUPY_CHARACTER = '('
"""Character that is used to occupy a position in the code."""

__all__ = [
    "ORIGINAL_STDOUT",
    "ORIGINAL_STDERR",
    "ORIGINAL_PROGRESS_BAR",
    "DEFAULT_OUTPUT_VALUE",
    "DEFAULT_LINE_SPACING",
    "DEFAULT_CURSOR_HEIGHT",
    "DEFAULT_CURSOR_WIDTH",
    "DEFAULT_CODE_FONT",
    "DEFAULT_CURSOR_TO_CHAR_BUFFER",
    "DEFAULT_TYPE_INTERVAL",
    "DEFAULT_LINE_BREAK_RUN_TIME",
    "DEFAULT_TAB_WIDTH",
    "DEFAULT_OUTPUT_CONSOLE",
    "DEFAULT_CURSOR_BLINK_RUN_TIME",
    "CODE_OFFSET",
    "NOT_AVAILABLE_CHARACTERS",
    "OCCUPY_CHARACTER"
]