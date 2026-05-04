from __future__ import annotations
from manim import config
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, TransferSpeedColumn
from copy import copy
from contextlib import contextmanager
from io import StringIO
from typing import get_args, get_origin, Literal, Generator, Any, Callable, TypeVar, Union, List
from moviepy.video.io.VideoFileClip import VideoFileClip
from PIL import Image, ImageFilter, ImageEnhance
from proglog import ProgressBarLogger
from collections import OrderedDict
from os import PathLike
from functools import wraps
import numpy as np
import time, sys, inspect, re

try:
    from typing import ParamSpec
    from types import UnionType
except ImportError:
    from typing_extensions import ParamSpec
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

def checkType(value: Any, expected_type: Union[Any, type[Any]], param_name: str, path: str = "") -> None:
    """
    Recursively check if a value matches the expected type.

    Args:
        value (Any): The value to check.
        expected_type (Union[Any, type[Any]]): The expected type.
        param_name (str): The name of the parameter being checked.
        path (str, optional): The path to the current value (for nested types). Defaults to ``""``.
        
    Raises:
        TypeError: If the value doesn't match the expected type.
        ValueError: If the value doesn't match a Literal type.
    """
    # Handle None type
    if expected_type is None:
        if value is not None:
            raise TypeError(f"Parameter '{param_name}'{path}: Expected 'None', got '{type(value).__name__}'")
        return
    
    # Handle PathLike types
    if expected_type is PathLike or (hasattr(expected_type, '__name__') and expected_type.__name__ == 'PathLike'):
        if not isinstance(value, (str, PathLike)):
            raise TypeError(f"Parameter '{param_name}'{path}: Expected 'str' or 'PathLike', got '{type(value).__name__}'")
        return
    
    # Handle PathLike types
    if expected_type is PathLike or (hasattr(expected_type, '__name__') and expected_type.__name__ == 'PathLike'):
        if not isinstance(value, (str, PathLike)):
            raise TypeError(f"Parameter '{param_name}'{path}: Expected 'str' or 'PathLike', got '{type(value).__name__}'")
        return
    
    # Handle Literal types
    if get_origin(expected_type) is Literal:
        literal_values = get_args(expected_type)
        if value not in literal_values:
            raise ValueError(f"Parameter '{param_name}'{path}: Expected one of {literal_values}, got '{value}'")
        return
    
    # Handle Union types (both Union and UnionType)
    origin = get_origin(expected_type)
    if origin is Union or isinstance(expected_type, UnionType):
        union_types = get_args(expected_type)
        if not union_types:
            # Empty Union is equivalent to Never type
            raise TypeError(f"Parameter '{param_name}'{path}: Expected 'Never', got '{type(value).__name__}'")
        
        # Track all errors to find the most specific one
        errors = []
        
        # Check if any union type matches
        for union_type in union_types:
            try:
                checkType(value, union_type, param_name, path)
                return  # If any type matches, return successfully
            except (TypeError, ValueError) as e:
                errors.append(e)
                continue
        
        # If no types match, find the most specific error
        if errors:
            # For tuple types, prefer errors that get deeper into the tuple
            # This helps with cases like ('string', 1) where we want the error about the second element
            best_error = errors[0]
            
            # Check if all errors are about the same index
            same_index = True
            index = None
            
            for error in errors:
                error_str = str(error)
                match = re.search(r"\(index (\d+)\)", error_str)
                if match:
                    current_index = int(match.group(1))
                    if index is None:
                        index = current_index
                    elif current_index != index:
                        same_index = False
                else:
                    same_index = False
            
            # If all errors are about the same index, combine the error messages
            if same_index and len(errors) == len(union_types):
                # Extract the specific value being checked (from the tuple)
                specific_value = value
                if isinstance(value, (list, tuple)) and index < len(value): # type: ignore[reportOptionalOperand]
                    specific_value = value[index] # type: ignore[reportCallIssue, reportArgumentType]
                
                # Check if it's a tuple type with different element types at the same index
                all_item_types = []
                seen_types = set()
                
                # Extract all item types from the tuple union types
                for union_type in union_types:
                    if get_origin(union_type) is tuple:
                        item_types = get_args(union_type)
                        if index < len(item_types): # type: ignore[reportOptionalOperand]
                            item_type = item_types[index] # type: ignore[reportCallIssue, reportArgumentType]
                            # Check if this item type is itself a union
                            item_origin = get_origin(item_type)
                            if item_origin is Union or isinstance(item_type, UnionType):
                                # If it's a union, extract all its types
                                for nested_type in get_args(item_type):
                                    type_name = typeName(nested_type)
                                    if type_name not in seen_types:
                                        all_item_types.append(type_name)
                                        seen_types.add(type_name)
                            else:
                                # Otherwise, add the type directly
                                type_name = typeName(item_type)
                                if type_name not in seen_types:
                                    all_item_types.append(type_name)
                                    seen_types.add(type_name)
                
                # Create a combined error message
                if all_item_types:
                    # Check if any of the item types is a Literal type
                    has_literal = False
                    all_literal_values = []
                    seen_values = set()
                    
                    for union_type in union_types:
                        if get_origin(union_type) is tuple:
                            item_types = get_args(union_type)
                            if index < len(item_types): # type: ignore[reportOptionalOperand]
                                item_type = item_types[index] # type: ignore[reportCallIssue, reportArgumentType]
                                if get_origin(item_type) is Literal:
                                    has_literal = True
                                    literal_vals = get_args(item_type)
                                    for val in literal_vals:
                                        if val not in seen_values:
                                            all_literal_values.append(val)
                                            seen_values.add(val)
                    
                    if has_literal and all_literal_values:
                        # Literal error message
                        values_str = ", ".join([f"'{v}'" for v in all_literal_values])
                        raise ValueError(f"Parameter '{param_name}' (index {index}): Expected one of ({values_str}), got '{specific_value}'")
                    else:
                        # Regular type error message
                        expected_types_str = "' or '".join(all_item_types)
                        raise TypeError(f"Parameter '{param_name}' (index {index}): Expected {expected_types_str}, got '{type(specific_value).__name__}'")
            
            # Otherwise, use the existing logic to find the best error
            for error in errors[1:]:
                error_str = str(error)
                best_error_str = str(best_error)
                
                # Prefer errors that mention PathLike (for StrPath type)
                if "PathLike" in error_str and "PathLike" not in best_error_str:
                    best_error = error
                # Prefer errors that mention a specific index in a tuple
                elif "[index" in error_str and "[index" not in best_error_str:
                    best_error = error
                # If both mention indexes, prefer the one with the higher index (more specific)
                elif "[index" in error_str and "[index" in best_error_str:
                    error_idx = int(re.search(r"\(index (\d+)\)", error_str).group(1)) # type: ignore[reportOptionalMemberAccess]
                    best_error_idx = int(re.search(r"\(index (\d+)\)", best_error_str).group(1)) # type: ignore[reportOptionalMemberAccess]
                    if error_idx > best_error_idx:
                        best_error = error
            raise best_error
        
        # If no error was captured, raise a generic error
        # Special handling for StrPath type to show more informative error message
        if len(union_types) == 2:
            # Check if this is Union[str, PathLike[str]] (StrPath)
            has_str = False
            has_pathlike = False
            
            for t in union_types:
                if t is str:
                    has_str = True
                elif t is PathLike or (hasattr(t, '__origin__') and t.__origin__ is PathLike):
                    has_pathlike = True
                elif hasattr(t, '__name__') and t.__name__ == 'PathLike':
                    has_pathlike = True
                # Also check for PathLike[str] specifically
                elif hasattr(t, '__origin__') and t.__origin__ is PathLike and hasattr(t, '__args__') and t.__args__:
                    has_pathlike = True
            
            if has_str and has_pathlike:
                raise TypeError(f"Parameter '{param_name}'{path}: Expected 'str' or 'PathLike', got '{type(value).__name__}'")
        
        expected_types_str = "' or '".join([typeName(t) for t in union_types])
        raise TypeError(f"Parameter '{param_name}'{path}: Expected {expected_types_str}, got '{type(value).__name__}'")

    # Handle Tuple types
    if get_origin(expected_type) is tuple:
        if not isinstance(value, tuple):
            raise TypeError(f"Parameter '{param_name}'{path}: Expected 'tuple', got '{type(value).__name__}'")
        item_types = get_args(expected_type)
        if len(value) != len(item_types):
            raise ValueError(f"Parameter '{param_name}'{path}: Expected tuple of length {len(item_types)}, got {len(value)}")
        for idx, (item, item_type) in enumerate(zip(value, item_types)):
            checkType(item, item_type, param_name, f" (index {idx})")
        return
    
    # Handle List types
    if get_origin(expected_type) is list:
        if not isinstance(value, list):
            raise TypeError(f"Parameter '{param_name}'{path}: Expected 'list', got '{type(value).__name__}'")
        item_type = get_args(expected_type)[0] if get_args(expected_type) else Any
        for idx, item in enumerate(value):
            checkType(item, item_type, param_name, f" (index {idx})")
        return
    
    # Handle Dict types
    if get_origin(expected_type) is dict:
        if not isinstance(value, dict):
            raise TypeError(f"Parameter '{param_name}'{path}: Expected 'dict', got '{type(value).__name__}'")
        args = get_args(expected_type)
        key_type = args[0] if len(args) > 0 else Any
        value_type = args[1] if len(args) > 1 else Any
        for key, val in value.items():
            checkType(key, key_type, param_name, f" (key '{key}')")
            checkType(val, value_type, param_name, f" (value for key '{key}')")
        return
    
    # Handle Set types
    if get_origin(expected_type) is set:
        if not isinstance(value, set):
            raise TypeError(f"Parameter '{param_name}'{path}: Expected 'set', got '{type(value).__name__}'")
        item_type = get_args(expected_type)[0] if get_args(expected_type) else Any
        for item in value:
            checkType(item, item_type, param_name, f" (item '{item}')")
        return
    
    # Handle other generic types (like Optional, etc.)
    origin = get_origin(expected_type)
    if origin:
        # For other generic types, at least check if the value is an instance of the origin
        try:
            is_instance = isinstance(value, origin)
        except TypeError:
            # Handle cases where isinstance can't be used (e.g., for some typing types)
            is_instance = False
        
        if not is_instance:
            raise TypeError(f"Parameter '{param_name}'{path}: Expected '{typeName(expected_type)}', got '{type(value).__name__}'")
        return
    
    # Handle basic types
    try:
        is_instance = isinstance(value, expected_type)
    except TypeError:
        # Handle cases where isinstance can't be used (e.g., for some typing types)
        is_instance = False

    if not is_instance:
        # Special case for PathLike[str]
        if expected_type is PathLike[str] or (hasattr(expected_type, '__args__') and 
                                             len(expected_type.__args__) == 1 and 
                                             expected_type.__args__[0] is str and
                                             getattr(expected_type, '__origin__', None) is PathLike):
            if not isinstance(value, (str, PathLike)):
                raise TypeError(f"Parameter '{param_name}'{path}: Expected 'str' or 'PathLike[str]', got '{type(value).__name__}'")
            return
        
        raise TypeError(f"Parameter '{param_name}'{path}: Expected '{typeName(expected_type)}', got '{type(value).__name__}'")

P = ParamSpec('P')
R = TypeVar('R')
def typeChecker(func: Callable[P, R]) -> Callable[P, R]:
    """
    Decorator to check types of function arguments and return value.

    Args:
        func (Callable): The function to decorate.
        
    Returns:
        Callable: The wrapped function with type checking.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs)
        
        for param_name, param_value in bound_args.arguments.items():
            param_type = sig.parameters[param_name].annotation
            if param_type is inspect.Parameter.empty:
                continue  # 无注解则跳过
            
            # Use recursive type checking
            checkType(param_value, param_type, param_name)
                        
        return func(*args, **kwargs)
    return wrapper

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
            min_time_interval=min_time_interval, # type: ignore[reportArgumentType]
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
                    task_id, # type: ignore[reportArgumentType]
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
    "checkType",
    "typeChecker",
    "addGlowEffect",
    "findSpacePositions",
    "findEmptyLinePositions",
    "replaceMiddleSpacesWithOccupyCharacter",
    "DefaultProgressBar",
    "RichProgressBarLogger"
]