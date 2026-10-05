from manim import config
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, TransferSpeedColumn
from copy import copy
from contextlib import contextmanager
from io import StringIO
from typing import get_args, get_origin, Union
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


@contextmanager
def noManimOutput():
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


def stripEmptyLines(text):
    lines = text.split("\n")

    start = 0
    while start < len(lines) and lines[start].strip() == '':
        start += 1

    end = len(lines)
    while end > start and lines[end - 1].strip() == '':
        end -= 1

    return '\n'.join(lines[start:end])


def typeName(item_type):
    if isinstance(item_type, UnionType):
        return str(item_type).replace(" | ", "' or '")

    if not isinstance(item_type, type):
        if isinstance(item_type, str):
            return f"'{item_type}'"
        return str(item_type)

    origin = get_origin(item_type)
    if origin:
        args = get_args(item_type)
        if args:
            arg_names = ', '.join([typeName(arg) for arg in args])
            return f"{origin.__name__}[{arg_names}]"
        return origin.__name__

    return item_type.__name__


def addGlowEffect(input_path, output_path, output):
    def _frame_glow(t):
        frame = t.astype(np.uint8)
        pil_img = Image.fromarray(frame).convert("RGBA")

        brightness_enhancer = ImageEnhance.Brightness(pil_img)
        pil_img = brightness_enhancer.enhance(1.2)

        glow = pil_img.filter(ImageFilter.GaussianBlur(radius=10))

        glow_bright_enhancer = ImageEnhance.Brightness(glow)
        glow = glow_bright_enhancer.enhance(1.6)
        glow_color_enhancer = ImageEnhance.Color(glow)
        glow = glow_color_enhancer.enhance(2)

        soft_glow_img = Image.blend(glow, pil_img, 0.4)
        glow_frame = np.array(soft_glow_img.convert("RGB")).astype(np.uint8)
        return np.clip(glow_frame, 0, 255)

    glow_video = VideoFileClip(input_path).image_transform(_frame_glow)
    glow_video.write_videofile(
        output_path,
        codec='libx264',
        audio=True,
        preset=FFMPEG_PRESET,
        threads=FFMPEG_THREADS,
        ffmpeg_params=["-bufsize", FFMPEG_BUFSIZE],
        logger=RichProgressBarLogger(output=output, title="Glow Effect", leave_bars=False),
    )


def findSpacePositions(string):
    result = []
    for row_idx, s in enumerate(string.splitlines()):
        first_non_space = 0
        while first_non_space < len(s) and s[first_non_space] == ' ':
            first_non_space += 1

        last_non_space = len(s) - 1
        while last_non_space >= 0 and s[last_non_space] == ' ':
            last_non_space -= 1

        if first_non_space > last_non_space:
            result.extend([[row_idx, col_idx] for col_idx in range(len(s))])
            continue

        for col_idx in range(first_non_space, last_non_space + 1):
            if s[col_idx] == ' ':
                result.append([row_idx, col_idx])

    return result


def findEmptyLinePositions(string):
    return [idx for idx, line in enumerate(string.splitlines()) if line.strip() == '']


def replaceMiddleSpacesWithOccupyCharacter(string):
    result = []
    for s in string.splitlines():
        if not isinstance(s, str):
            result.append(s)
            continue

        if len(s) == 0:
            result.append(s)
            continue

        s_list = list(s)

        first_non_space = 0
        while first_non_space < len(s_list) and s_list[first_non_space] == ' ':
            first_non_space += 1

        last_non_space = len(s_list) - 1
        while last_non_space >= 0 and s_list[last_non_space] == ' ':
            last_non_space -= 1

        if first_non_space > last_non_space:
            result.append(s.replace(' ', OCCUPY_CHARACTER))
            continue

        for idx in range(first_non_space, last_non_space + 1):
            if s_list[idx] == ' ':
                s_list[idx] = OCCUPY_CHARACTER

        result.append(''.join(s_list))

    return '\n'.join(result)


class DefaultProgressBar(Progress):
    def __init__(self, output):
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
    def __init__(
        self,
        output,
        title,
        init_state=None,
        bars=None,
        leave_bars=True,
        ignored_bars=None,
        logged_bars="all",
        print_messages=True,
        min_time_interval=0.1,
        ignore_bars_under=0,
    ):
        super().__init__(
            init_state=init_state,
            bars=bars,
            ignored_bars=ignored_bars,
            logged_bars=logged_bars,
            ignore_bars_under=ignore_bars_under,
            min_time_interval=min_time_interval,
        )

        self.leave_bars = leave_bars
        self.print_messages = print_messages
        self.output = output
        self.title = title
        self.start_time = time.time()

        self.progress_bar = copy(DefaultProgressBar(self.output))
        self.rich_bars = OrderedDict()

        if self.progress_bar and not self.progress_bar.live.is_started:
            self.progress_bar.start()

    def new_tqdm_bar(self, bar):
        if not self.output or self.progress_bar is None:
            return

        if bar in self.rich_bars:
            self.close_tqdm_bar(bar)

        infos = self.bars[bar]
        task_id = self.progress_bar.add_task(description=f"[yellow]{self.title}[/yellow]", total=infos["total"])
        self.rich_bars[bar] = task_id

    def close_tqdm_bar(self, bar):
        if not self.output or self.progress_bar is None:
            return

        if bar in self.rich_bars:
            task_id = self.rich_bars[bar]
            if not self.leave_bars:
                self.progress_bar.remove_task(task_id)
            del self.rich_bars[bar]

    def bars_callback(self, bar, attr, value, old_value):
        if not self.output or self.progress_bar is None:
            return
        if bar not in self.rich_bars:
            self.new_tqdm_bar(bar)

        task_id = self.rich_bars.get(bar)
        if task_id is None:
            return
        if attr == "index":
            if value >= old_value:
                total = self.bars[bar]["total"]
                elapsed = time.time() - self.start_time
                speed = value / elapsed if elapsed > 0 else 0.0

                self.progress_bar.update(
                    task_id,
                    completed=value,
                    speed=speed
                )

                if total and (value >= total):
                    self.close_tqdm_bar(bar)
            else:
                self.new_tqdm_bar(bar)
                self.progress_bar.update(self.rich_bars[bar], completed=value)

    def stop(self):
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
