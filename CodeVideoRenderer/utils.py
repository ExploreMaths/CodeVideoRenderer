from __future__ import annotations
from manim import config
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, TransferSpeedColumn
from copy import copy
from contextlib import contextmanager
from io import StringIO
from typing import get_args, get_origin, Generator, Any, Union, List
from moviepy.video.io.VideoFileClip import VideoFileClip
from PIL import Image, ImageFilter, ImageEnhance
from proglog import ProgressBarLogger
from collections import OrderedDict
import numpy as np
import time, sys

try:
    from types import UnionType
except ImportError:
    UnionType = type(Union[int, str])

from .config import *
from .typing import StrPath

@contextmanager
def noManimOutput() -> Generator[None, Any, None]:
    """
    Context manager used to execute code without outputting Manim logs.
    """
    sys.stdout = StringIO()
    stderr_buffer = StringIO()
    sys.stderr = stderr_buffer
    config.progress_bar = "none"

    try:
        yield
    finally:
        sys.stdout = ORIGINAL_STDOUT
        sys.stderr = ORIGINAL_STDERR
        config.progress_bar = ORIGINAL_PROGRESS_BAR
        stderr_content = stderr_buffer.getvalue()
        if stderr_content:
            print(stderr_content, file=ORIGINAL_STDERR)

def stripEmptyLines(text: str) -> str:
    """
    Remove empty lines from the beginning and end of a string.

    Args:
        text (str): The input string to process.
        
    Returns:
        str: The string with empty lines removed from the beginning and end.
    """
    lines = text.split("\n")
    
    start = 0
    while start < len(lines) and lines[start].strip() == '':
        start += 1
    
    end = len(lines)
    while end > start and lines[end - 1].strip() == '':
        end -= 1
    
    return '\n'.join(lines[start:end])

def typeName(item_type: Any) -> str:
    """
    Get the name of a type, handling union types and generic types.

    Args:
        item_type: The type or value to get the name of.
        
    Returns:
        str: The name of the type.
    """
    # Handle UnionType
    if isinstance(item_type, UnionType):
        return str(item_type).replace(" | ", "' or '")
    
    # Handle non-type objects (like Literal values)
    if not isinstance(item_type, type):
        if isinstance(item_type, str):
            return f"'{item_type}'"
        return str(item_type)
    
    # Handle generic types
    origin = get_origin(item_type)
    if origin:
        args = get_args(item_type)
        if args:
            arg_names = ', '.join([typeName(arg) for arg in args])
            return f"{origin.__name__}[{arg_names}]"
        return origin.__name__
    
    # Handle basic types
    return item_type.__name__

def addGlowEffect(input_path: StrPath, output_path: StrPath, output: bool) -> None:
    """
    Add a glow effect to a video.

    Args:
        input_path (StrPath): Path to the input video file.
        output_path (StrPath): Path to save the output video file.
        output (bool): Whether to display progress bars.
        
    Returns:
        None
    """
    # 内部帧处理函数
    def _frame_glow(t: np.ndarray):
        # 获取MoviePy的numpy帧并转为PIL图像
        frame = t.astype(np.uint8)
        pil_img = Image.fromarray(frame).convert("RGBA")

        # 提升基础亮度
        brightness_enhancer = ImageEnhance.Brightness(pil_img)
        pil_img = brightness_enhancer.enhance(1.2)

        # 创建模糊光晕层
        glow = pil_img.filter(ImageFilter.GaussianBlur(radius=10))

        # 提升光晕的亮度和饱和度
        glow_bright_enhancer = ImageEnhance.Brightness(glow)
        glow = glow_bright_enhancer.enhance(1.5)
        glow_color_enhancer = ImageEnhance.Color(glow)
        glow = glow_color_enhancer.enhance(1.2)

        # 混合原图像与光晕层
        soft_glow_img = Image.blend(glow, pil_img, 0.4)
        glow_frame = np.array(soft_glow_img.convert("RGB")).astype(np.uint8)
        return np.clip(glow_frame, 0, 255)
    
    glow_video: VideoFileClip = VideoFileClip(input_path).image_transform(_frame_glow)
    glow_video.write_videofile(output_path, codec='libx264', audio=True, logger=RichProgressBarLogger(output=output, title="Glow Effect", leave_bars=False))

def findSpacePositions(string: str) -> List[List[int]]:
    """
    Find the 2D positions of all non-leading, non-trailing spaces in a string.
    Each position is represented as a list ``[row_index, column_index]``.
    
    Args:
        string (str): A string.
        
    Returns:
        List[List[int]]: A list of 2D positions of all non-leading, non-trailing spaces.
        Each position is represented as a list ``[row_index, column_index]``.
    """
    result = []  # 存储所有[行, 列]格式的空格位置
    for row_idx, s in enumerate(string.splitlines()):
        # 找到第一个非空格字符的列索引
        first_non_space = 0
        while first_non_space < len(s) and s[first_non_space] == ' ':
            first_non_space += 1
        
        # 找到最后一个非空格字符的列索引
        last_non_space = len(s) - 1
        while last_non_space >= 0 and s[last_non_space] == ' ':
            last_non_space -= 1
        
        # 全空格/空字符串，跳过
        if first_non_space > last_non_space:
            result.extend([[row_idx, col_idx] for col_idx in range(len(s))])  # 记录整行空格位置
            continue
        
        # 遍历中间部分，收集[行, 列]格式的位置
        for col_idx in range(first_non_space, last_non_space + 1):
            if s[col_idx] == ' ':
                result.append([row_idx, col_idx])
    
    return result

def findEmptyLinePositions(string: str) -> List[int]:
    """
    Find the line indices of all empty lines in a string.
    
    Args:
        string (str): A string.
        
    Returns:
        List[int]: A list of line indices of all empty lines.
    """
    return [idx for idx, line in enumerate(string.splitlines()) if line.strip() == '']

def replaceMiddleSpacesWithOccupyCharacter(string: str) -> str:
    """
    Replace all non-leading, non-trailing spaces in the input string with :data:`~.OCCUPY_CHARACTER`.
    Retain leading and trailing spaces.
    
    Args:
        string (str): Original string.
        
    Returns:
        str: Processed string with middle spaces replaced by :data:`~.OCCUPY_CHARACTER`.
    """
    result = []
    for s in string.splitlines():
        # 处理非字符串元素，直接保留原元素
        if not isinstance(s, str):
            result.append(s)
            continue
        
        # 空字符串直接保留
        if len(s) == 0:
            result.append(s)
            continue
        
        # 转为列表方便修改字符
        s_list = list(s)
        
        # 找到第一个非空格字符的索引
        first_non_space = 0
        while first_non_space < len(s_list) and s_list[first_non_space] == ' ':
            first_non_space += 1
        
        # 找到最后一个非空格字符的索引
        last_non_space = len(s_list) - 1
        while last_non_space >= 0 and s_list[last_non_space] == ' ':
            last_non_space -= 1
        
        # 全是空格的情况，直接保留原字符串
        if first_non_space > last_non_space:
            result.append(s.replace(' ', OCCUPY_CHARACTER))
            continue
        
        # 遍历中间区域，替换空格为1
        for idx in range(first_non_space, last_non_space + 1):
            if s_list[idx] == ' ':
                s_list[idx] = OCCUPY_CHARACTER
        
        # 转回字符串并加入结果
        result.append(''.join(s_list))
    
    return '\n'.join(result)

class DefaultProgressBar(Progress):
    """
    Default progress bar.
    """
    def __init__(self, output: bool):
        super().__init__(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[yellow]{task.completed}/{task.total}"),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            TransferSpeedColumn(),
            console=DEFAULT_OUTPUT_CONSOLE if output else None
        )

class RichProgressBarLogger(ProgressBarLogger):
    """
    A progress logger that uses Rich to display progress bars.
    """
    def __init__(
        self,
        output: bool,
        title: str,
        init_state=None,
        bars=None,
        leave_bars=True,
        ignored_bars=None,
        logged_bars="all",
        print_messages=True,
        min_time_interval=0.1,
        ignore_bars_under=0,
    ):
        # 调用父类构造函数，初始化核心属性
        super().__init__(
            init_state=init_state,
            bars=bars,
            ignored_bars=ignored_bars,
            logged_bars=logged_bars,
            ignore_bars_under=ignore_bars_under,
            min_time_interval=min_time_interval, # type: ignore
        )
        
        # 初始化自定义属性
        self.leave_bars = leave_bars
        self.print_messages = print_messages
        self.output = output
        self.title = title
        self.start_time = time.time()
        
        # 初始化 Rich 进度条
        self.progress_bar = copy(DefaultProgressBar(self.output))
        self.rich_bars = OrderedDict()  # 存储 {bar_name: task_id}
        
        # 启动 Rich 进度条
        if self.progress_bar and not self.progress_bar.live.is_started:
            self.progress_bar.start()

    def new_tqdm_bar(self, bar):
        """
        Create a Rich progress bar task for the given bar.
        """
        if not self.output or self.progress_bar is None:
            return
        
        # 关闭已有进度条
        if bar in self.rich_bars:
            self.close_tqdm_bar(bar)
        
        # 获取父类维护的进度条信息
        infos = self.bars[bar]
        # 创建 Rich 进度条任务
        task_id = self.progress_bar.add_task(description=f"[yellow]{self.title}[/yellow]", total=infos["total"])
        self.rich_bars[bar] = task_id

    def close_tqdm_bar(self, bar):
        """
        Close the Rich progress bar task for the given bar.
        """
        if not self.output or self.progress_bar is None:
            return
        
        if bar in self.rich_bars:
            task_id = self.rich_bars[bar]
            # 若不需要保留，移除任务
            if not self.leave_bars:
                self.progress_bar.remove_task(task_id)
            del self.rich_bars[bar]

    def bars_callback(self, bar, attr, value, old_value):
        """
        Update the Rich progress bar task based on the attribute change.
        """
        if bar not in self.rich_bars:
            self.new_tqdm_bar(bar)
        
        task_id = self.rich_bars.get(bar)
        if attr == "index":
            # 处理帧数更新（核心）
            if value >= old_value:
                total = self.bars[bar]["total"]
                # 计算处理速度
                elapsed = time.time() - self.start_time
                speed = value / elapsed if elapsed > 0 else 0.0
                
                # 更新 Rich 进度条
                self.progress_bar.update(
                    task_id, # type: ignore
                    completed=value,
                    speed=speed
                )
                
                # 完成后关闭（复刻原逻辑）
                if total and (value >= total):
                    self.close_tqdm_bar(bar)
            else:
                # 帧数回退：重置进度条
                self.new_tqdm_bar(bar)
                self.progress_bar.update(self.rich_bars[bar], completed=value)

    def stop(self):
        """
        Stop the Rich progress bar.
        """
        if self.progress_bar and self.progress_bar.live.is_started:
            self.progress_bar.stop()

__all__ = [
    "noManimOutput",
    "stripEmptyLines",
    "typeName",
    "addGlowEffect",
    "findSpacePositions",
    "findEmptyLinePositions",
    "replaceMiddleSpacesWithOccupyCharacter",
    "DefaultProgressBar",
    "RichProgressBarLogger"
]