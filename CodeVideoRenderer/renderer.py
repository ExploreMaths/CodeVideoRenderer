from manim import VGroup, Group, Code, SurroundingRectangle, RoundedRectangle, Rectangle, Line, MovingCameraScene, rate_functions, RendererType, config, WHITE, GREY, UP, DOWN, LEFT, RIGHT, register_font, FadeOut, FadeIn, Text, ImageMobject
from pathlib import Path
from copy import copy
from timeit import timeit
from rich import traceback
import numpy as np
import random, inspect, os, re

from .config import *
from .utils import *
from .vscode_theme import register_vscode, resolve_language, STYLE_NAME
from .ime import is_cjk, get_ime

traceback.install()
register_vscode()

# griddycode completion icons (Icons/function.png, Icons/variable.png preloaded in settings.gd)
AUTOCOMPLETE_ICONS = {
    "function": os.path.join(os.path.dirname(__file__), "icons", "function.png"),
    "variable": os.path.join(os.path.dirname(__file__), "icons", "variable.png"),
}

# griddycode completion option colors: LuaSingleton.keywords.function / .variable (settings.gd)
AUTOCOMPLETE_COLORS = {
    "function": "#61afef",
    "variable": "#d19a66",
}

# completion box colors, matching griddycode "One Dark Pro Darker" gui colors
_SUGGEST_BG = "#1e2227"
_SUGGEST_BORDER = "#3d4556"
_SUGGEST_FG = "#abb2bf"
_SUGGEST_DETAIL = "#7f848e"
_SUGGEST_SELECTED_BG = "#2c313a"


def detect_functions(code_str):
    """Port of griddycode `Lua/Plugins/py.lua` `detect_functions`: def / async def names."""
    names = []
    for line in code_str.splitlines():
        m = re.search(r"def\s+([\w_]+)\s*\(", line)
        if m:
            names.append(m.group(1))
        m = re.search(r"async\s+def\s+([\w_]+)\s*\(", line)
        if m:
            names.append(m.group(1))
    return names


def detect_variables(code_str):
    """Port of griddycode `Lua/Plugins/py.lua` `detect_variables`: builtins + `name = ...` assignments."""
    names = ["self", "__name__", "__annotations__", "__build_class__", "__builtins__",
             "__cached__", "__dict__", "__doc__", "__file__", "__import__", "__loader__",
             "__name__", "__package__", "__path__", "__spec__"]
    for line in code_str.splitlines():
        m = re.search(r"(\w+)\s*=\s*.+", line)
        if m:
            names.append(m.group(1))
    return names


class CameraFollowCursorCV:
    """Animate code being typed while the camera follows the cursor."""
    __all__ = ["render"]

    def __init__(self,
        code,
        language,
        formatter_style="vscode-dark-plus",
        line_spacing=DEFAULT_LINE_SPACING,
        interval_range=(DEFAULT_TYPE_INTERVAL, DEFAULT_TYPE_INTERVAL),
        camera_scale=0.5,
        video_name="CameraFollowCursorCV",
        renderer='cairo',
        clear_code=False,
        clear_code_mode='backspace',
        clear_code_run_time=1.0,
        clear_code_interval=0.03,
        autocomplete=False,
        autocomplete_wait_time=0.6,
        chinese_ime=False,
        ime_wait_time=0.6,
        background_color="#23272e",
        line_highlight_color="#2c313c",
        end_wait_time=1.0,
        quality=None,
        frame_rate=None,
    ):
        if not video_name:
            raise ValueError("video_name must be provided")

        if code[0] == 'string':
            self.code_str = code[1].expandtabs(tabsize=DEFAULT_TAB_WIDTH)
            if not all(char not in NOT_AVAILABLE_CHARACTERS for char in self.code_str):
                raise ValueError("'code_string' contains invalid characters")
        elif code[0] == 'file':
            try:
                self.code_str = Path(code[1]).read_text(encoding="utf-8").expandtabs(tabsize=DEFAULT_TAB_WIDTH)
                if not all(char not in NOT_AVAILABLE_CHARACTERS for char in self.code_str):
                    raise ValueError(f"'{code[1]}' contains invalid characters")
            except UnicodeDecodeError:
                raise ValueError(f"Failed to decode '{code[1]}' with UTF-8 encoding") from None

        if line_spacing <= 0:
            raise ValueError("line_spacing must be greater than 0")

        min_interval = round(1/config.frame_rate, 7)
        if not all(interval >= min_interval for interval in interval_range):
            raise ValueError(f"interval_range must be greater than or equal to {min_interval}")
        del min_interval
        if interval_range[0] > interval_range[1]:
            raise ValueError("The first term of interval_range must be less than or equal to the second term")

        if clear_code_interval <= 0:
            raise ValueError("clear_code_interval must be greater than 0")

        global Parameters
        class Parameters:
            pass
        Parameters.code = code
        Parameters.language = language
        Parameters.formatter_style = formatter_style
        Parameters.line_spacing = line_spacing
        Parameters.interval_range = interval_range
        Parameters.camera_scale = camera_scale
        Parameters.video_name = video_name
        Parameters.renderer = renderer
        Parameters.clear_code = clear_code
        Parameters.clear_code_mode = clear_code_mode
        Parameters.clear_code_run_time = clear_code_run_time
        Parameters.clear_code_interval = clear_code_interval
        Parameters.autocomplete = autocomplete
        Parameters.autocomplete_wait_time = autocomplete_wait_time
        Parameters.chinese_ime = chinese_ime
        Parameters.ime_wait_time = ime_wait_time
        Parameters.background_color = background_color
        Parameters.line_highlight_color = line_highlight_color
        Parameters.end_wait_time = end_wait_time

        self.code_str = stripEmptyLines(self.code_str)
        self.space_positions = findSpacePositions(self.code_str)
        self.empty_line_positions = findEmptyLinePositions(self.code_str)
        # griddycode settings.gd: completion options = detected functions + detected variables
        self.detected_symbols = []
        _seen = set()
        for _f in detect_functions(self.code_str):
            if ("function", _f) not in _seen:
                _seen.add(("function", _f))
                self.detected_symbols.append((_f, "function"))
        for _v in detect_variables(self.code_str):
            if ("variable", _v) not in _seen:
                _seen.add(("variable", _v))
                self.detected_symbols.append((_v, "variable"))
        self.code_str = replaceMiddleSpacesWithOccupyCharacter("\n".join([" " if line == "" else line for line in self.code_str.splitlines()]))
        self.code_str_lines = self.code_str.splitlines()
        self.origin_config = {
            'disable_caching': config.disable_caching,
            'renderer': config.renderer,
            'background_color': config.background_color,
            'quality': config.quality,
            'frame_rate': config.frame_rate,
        }
        config.disable_caching = True
        config.renderer = renderer
        config.background_color = background_color
        if quality is not None:
            config.quality = quality
        if frame_rate is not None:
            config.frame_rate = frame_rate
        self.scene = self._create_scene()

    def _create_scene(self):
        class CameraFollowCursorCVScene(MovingCameraScene):

            def construct(scene):

                cursor = RoundedRectangle(
                    height=DEFAULT_CURSOR_HEIGHT,
                    width=DEFAULT_CURSOR_WIDTH,
                    corner_radius=DEFAULT_CURSOR_WIDTH / 2,
                    fill_opacity=1,
                    fill_color=WHITE,
                    color=WHITE
                )

                with register_font(os.path.join(os.path.dirname(__file__), 'fonts/CodeVideoRendererFont.ttf')):
                    line_number_mobject, code_mobject = Code(
                        code_string=self.code_str + f"\n{(max([len(line.rstrip()) for line in self.code_str_lines])*2)*' ' + OCCUPY_CHARACTER}",
                        language=resolve_language(Parameters.language),
                        formatter_style=Parameters.formatter_style,
                        paragraph_config={
                            'font': 'CodeVideoRendererFont',
                            'line_spacing': Parameters.line_spacing
                        }
                    ).submobjects[1:3]
                line_number_mobject.set_color(GREY)

                total_lines = len(self.code_str_lines)
                total_chars = len(''.join(line.strip() for line in self.code_str_lines))

                # Adjust code alignment (manim built-in bug)
                offset_lines = []
                for line_index, line in enumerate(self.code_str_lines):
                    if all(check in "acegmnopqrsuvwxyz+,-.:;<=>_~ " for check in line):
                        if line_index == 0:
                            code_mobject.shift(DOWN*CODE_OFFSET)
                        offset_lines.append(line_index)
                del line_index, line

                code_line_rectangle = SurroundingRectangle(
                    VGroup(code_mobject[-1], line_number_mobject[-1]),
                    color=Parameters.line_highlight_color,
                    fill_opacity=1,
                    stroke_width=0
                ).set_y(code_mobject[0].get_y())
                # Handle the code_line_rectangle offset when the first line is offset
                if 0 in offset_lines:
                    code_line_rectangle.shift(UP*CODE_OFFSET/2)

                cursor.align_to(code_mobject[0], LEFT).set_y(code_line_rectangle.get_y())

                if config.renderer == RendererType.OPENGL:
                    scene.camera.frame = scene.camera

                target_center = cursor.get_center()
                start_center = target_center + UP * 3
                scene.camera.frame.scale(Parameters.camera_scale).move_to(start_center)
                scene.add(code_line_rectangle, line_number_mobject[0].set_color(WHITE), cursor)

                scene.play(
                    scene.camera.frame.animate.move_to(target_center),
                    run_time=1,
                    rate_func=rate_functions.ease_out_cubic
                )

                scene.Animation_list = []
                def linebreakAnimation():
                    scene.Animation_list.append({"move_to": cursor.get_center() + drift_offset()})

                camera_scale = Parameters.camera_scale
                longest_line = 0

                # griddycode camera.gd idle sway: offset = (sin(d*speed)*radius, cos(d*speed)*radius)
                drift_time = [0.0]
                def drift_offset():
                    radius = scene.camera.frame.height * 0.1
                    t = drift_time[0]
                    return np.array([np.sin(t * 2.0) * radius, np.cos(t * 2.0) * radius, 0.0])

                def JUDGE_cameraScaleAnimation():
                    nonlocal camera_scale
                    # griddycode camera.gd: zoom = clamp(10 - (chars + 1) / SCALE, 1, 10), SCALE = 7
                    godot_zoom = max(1.0, min(10.0, 10.0 - (longest_line + 1) / 7.0))
                    target_scale = Parameters.camera_scale * 10.0 / godot_zoom
                    if target_scale != camera_scale:
                        scene.Animation_list.append({"scale": target_scale / camera_scale})
                        camera_scale = target_scale

                def playAnimation(**kwargs):
                    if scene.Animation_list:
                        camera_anim = scene.camera.frame.animate

                        for anim in scene.Animation_list:
                            if "move_to" in anim:
                                camera_anim.move_to(anim["move_to"])
                            elif "scale" in anim:
                                camera_anim.scale(anim["scale"])

                        scene.play(camera_anim, **kwargs)
                        drift_time[0] += kwargs.get("run_time", 0.0)
                        scene.Animation_list.clear()
                        del camera_anim

                typed_mobjects = []

                font_path = os.path.join(os.path.dirname(__file__), 'fonts/CodeVideoRendererFont.ttf')

                # griddycode settings.gd: completion options = detected functions + detected variables
                completion_symbols = self.detected_symbols

                def showAutocomplete(keyword):
                    matches = [(n, k) for n, k in completion_symbols if n == keyword]
                    if not matches:
                        return
                    with register_font(font_path):
                        rows = []
                        for name, kind in matches:
                            icon = ImageMobject(AUTOCOMPLETE_ICONS[kind]).scale_to_fit_height(0.3)
                            display = name + "()" if kind == "function" else name
                            label_t = Text(display, font="CodeVideoRendererFont", font_size=20, color=AUTOCOMPLETE_COLORS[kind])
                            icon.next_to(label_t, LEFT, buff=0.14)
                            rows.append(Group(icon, label_t))

                    # griddycode completion box: icon + colored name per row, no detail column.
                    pad_x, pad_y = 0.25, 0.15
                    row_buff = 0.1
                    max_row_w = max(r.width for r in rows)
                    row_h = max(r.height for r in rows)
                    row_step = row_h + row_buff

                    box = RoundedRectangle(
                        width=max_row_w + 2 * pad_x,
                        height=row_step * len(rows) + 2 * pad_y,
                        corner_radius=0.06,
                        color=_SUGGEST_BG, fill_color=_SUGGEST_BG, fill_opacity=1, stroke_width=0,
                    )

                    content_left = box.get_left()[0] + pad_x
                    top_y = box.get_top()[1] - pad_y
                    for i, row in enumerate(rows):
                        row_y = top_y - row_step * i - row_h / 2
                        row.move_to([content_left + row.width / 2, row_y, 0])

                    # first row is selected (completion_selected_color)
                    sel = Rectangle(
                        width=box.width - 0.1, height=row_step,
                        color=_SUGGEST_SELECTED_BG, fill_opacity=1, stroke_width=0,
                    ).move_to([box.get_x(), rows[0].get_y(), 0])

                    popup = Group(box, sel, *rows)
                    popup.next_to(cursor, DOWN, buff=0.3)

                    scene.add(popup)
                    scene.play(FadeIn(popup), run_time=0.12)
                    scene.wait(Parameters.autocomplete_wait_time)
                    scene.play(FadeOut(popup), run_time=0.12)

                def showIme(pinyin, candidates):
                    if not candidates:
                        return
                    with register_font(font_path):
                        py_t = Text(pinyin, font="CodeVideoRendererFont", font_size=18, color="#9CDCFE")
                        cands = [Text(c, font="CodeVideoRendererFont", font_size=20, color="#808080") for c in candidates]
                    cands[0].set_color(_SUGGEST_FG)

                    cand_row = VGroup(*cands).arrange(RIGHT, aligned_edge=UP, buff=0.22)
                    inner_w = max(py_t.get_width(), cand_row.get_width())
                    bar = Rectangle(width=inner_w, height=0.03, fill_color=_SUGGEST_BORDER, fill_opacity=1, stroke_width=0)
                    content = VGroup(py_t, bar, cand_row).arrange(DOWN, aligned_edge=LEFT, buff=0.12)

                    hl = Rectangle(
                        width=cands[0].width + 0.18, height=cands[0].height + 0.12,
                        color=_SUGGEST_SELECTED_BG, fill_opacity=1, stroke_width=0,
                    ).move_to(cands[0])

                    box = RoundedRectangle(
                        width=inner_w + 0.44, height=content.height + 0.3,
                        corner_radius=0.06,
                        color=_SUGGEST_BORDER, fill_color=_SUGGEST_BG, fill_opacity=1, stroke_width=1,
                    )
                    popup = VGroup(box, hl, py_t, bar, cand_row)
                    popup.next_to(cursor, DOWN, buff=0.3)

                    scene.add(popup)
                    scene.play(FadeIn(popup), run_time=0.12)
                    scene.wait(Parameters.ime_wait_time)
                    scene.play(FadeOut(popup), run_time=0.12)

                with copy(DefaultProgressBar(self.output)) as progress:
                    total_progress = progress.add_task(description="[yellow]Total[/yellow]", total=total_chars)

                    for line in range(total_lines):

                        line_number_mobject.set_color(GREY)
                        line_number_mobject[line].set_color(WHITE)

                        char_num = len(self.code_str_lines[line].strip())
                        current_line_progress = progress.add_task(description=f"[green]Line {line+1}[/green]", total=char_num)

                        code_line_rectangle.set_y(code_mobject[line].get_y())
                        # Handle the code_line_rectangle offset when the line is offset
                        if line in offset_lines:
                            code_line_rectangle.shift(UP*CODE_OFFSET/2)
                        scene.add(line_number_mobject[line])

                        cursor.align_to(code_mobject[line], LEFT).set_y(code_line_rectangle.get_y())
                        if line != 0:
                            linebreakAnimation()
                        JUDGE_cameraScaleAnimation()
                        playAnimation(run_time=DEFAULT_LINE_BREAK_RUN_TIME)

                        if line in self.empty_line_positions:
                            progress.remove_task(current_line_progress)
                            continue

                        indent = len(self.code_str_lines[line]) - len(self.code_str_lines[line].lstrip())

                        # Compute the autocomplete trigger point for this line (the moment the symbol is fully typed)
                        char_idx = 0
                        for column in range(indent, char_num + indent):
                            # Handle the disappearing-space issue introduced in manim==0.19.1
                            if not self.code_str_lines[line][column].isspace():
                                if [line, column] not in self.space_positions:
                                    scene.add(code_mobject[line][char_idx])
                                    typed_mobjects.append(code_mobject[line][char_idx])
                                char_idx += 1
                            cursor.next_to(
                                code_mobject[line][char_idx-1],
                                RIGHT,
                                buff=DEFAULT_CURSOR_TO_CHAR_BUFFER
                            ).set_y(code_line_rectangle.get_y())

                            # griddycode tracks the longest line as it is typed so the
                            # camera zoom reacts in real time (camera.gd get_longest_line)
                            longest_line = max(longest_line, column + 1)

                            line_break = False
                            if column == indent and indent != 0:
                                # If this is the first character after indentation, perform the line-break reset first
                                linebreakAnimation()
                                line_break = True
                            else:
                                scene.Animation_list.append({"move_to": cursor.get_center() + drift_offset()})

                            JUDGE_cameraScaleAnimation()
                            playAnimation(
                                run_time=DEFAULT_LINE_BREAK_RUN_TIME if line_break else random.uniform(*Parameters.interval_range),
                                rate_func=rate_functions.smooth if line_break else rate_functions.linear
                            )

                            progress.advance(total_progress, advance=1)
                            progress.advance(current_line_progress, advance=1)

                            # griddycode settings.gd: completion shows once a detected symbol name is fully typed
                            if Parameters.autocomplete:
                                end = column + 1
                                start = column
                                while start >= 0 and (self.code_str_lines[line][start].isalnum() or self.code_str_lines[line][start] == "_"):
                                    start -= 1
                                start += 1
                                word = self.code_str_lines[line][start:end]
                                nxt = self.code_str_lines[line][end] if end < len(self.code_str_lines[line]) else ""
                                if word and (nxt == "" or not (nxt.isalnum() or nxt == "_")):
                                    for name, _kind in completion_symbols:
                                        if word == name:
                                            showAutocomplete(name)
                                            break

                            # Chinese character typed: show the IME candidate box (triggered on the first char of each CJK run)
                            if Parameters.chinese_ime:
                                ch = self.code_str_lines[line][column]
                                if is_cjk(ch):
                                    prev_ch = self.code_str_lines[line][column - 1] if column > 0 else ""
                                    if not is_cjk(prev_ch):
                                        pinyin, cands = get_ime(self.code_str_lines[line], column)
                                        if cands:
                                            showIme(pinyin, cands)

                        progress.remove_task(current_line_progress)
                    progress.remove_task(total_progress)

                if Parameters.clear_code:
                    # Pull the camera back to the full code view and hold it still before
                    # deleting; otherwise the camera stays at the last character during
                    # backspace deletion and looks like it is "deleting along with the code"
                    frame = scene.camera.frame
                    code_center = code_mobject.get_center()
                    fit_h = code_mobject.get_height() * 1.4 + 1.5
                    fit_w = code_mobject.get_width() * 1.4 + 1.5
                    aspect = frame.get_width() / frame.get_height()
                    need_h = max(fit_h, fit_w / aspect)
                    scene.play(
                        frame.animate.move_to(code_center).set_height(need_h),
                        run_time=0.6,
                        rate_func=rate_functions.ease_in_out_cubic,
                    )

                    if Parameters.clear_code_mode == "backspace":
                        # Delete character by character in reverse, like pressing backspace
                        for mobject in reversed(typed_mobjects):
                            cursor.next_to(mobject, RIGHT, buff=DEFAULT_CURSOR_TO_CHAR_BUFFER).set_y(code_line_rectangle.get_y())
                            scene.play(
                                FadeOut(mobject),
                                run_time=Parameters.clear_code_interval,
                                rate_func=rate_functions.linear
                            )
                        scene.play(
                            FadeOut(VGroup(line_number_mobject, cursor, code_line_rectangle)),
                            run_time=Parameters.clear_code_run_time,
                            rate_func=rate_functions.ease_in_out_cubic
                        )
                    else:
                        scene.play(
                            FadeOut(VGroup(code_mobject, line_number_mobject, cursor, code_line_rectangle)),
                            run_time=Parameters.clear_code_run_time,
                            rate_func=rate_functions.ease_in_out_cubic
                        )

                scene.wait(Parameters.end_wait_time)

            def render(scene):
                if self.output:
                    DEFAULT_OUTPUT_CONSOLE.log(f"Start rendering {Parameters.video_name}.mp4.")
                    DEFAULT_OUTPUT_CONSOLE.log("Start rendering CameraFollowCursorCVScene. [dim](by manim)[/]")
                    if config.renderer == RendererType.CAIRO:
                        DEFAULT_OUTPUT_CONSOLE.log('[blue]Currently using CPU (Cairo Renderer) for rendering.[/]')
                    else:
                        DEFAULT_OUTPUT_CONSOLE.log('[blue]Currently using GPU (OpenGL Renderer) for rendering.[/]')
                    DEFAULT_OUTPUT_CONSOLE.log("Manim's config has been modified.")

                with noManimOutput():
                    total_render_time = timeit(super().render, number=1)
                if self.output:
                    DEFAULT_OUTPUT_CONSOLE.log(f"Successfully rendered CameraFollowCursorCVScene in {total_render_time:,.2f} seconds. [dim](by manim)[/]")
                del total_render_time

                config.disable_caching = self.origin_config['disable_caching']
                config.renderer = self.origin_config['renderer']
                config.background_color = self.origin_config['background_color']
                config.quality = self.origin_config['quality']
                config.frame_rate = self.origin_config['frame_rate']
                if self.output:
                    DEFAULT_OUTPUT_CONSOLE.log("Manim's config has been restored.")
                del self.origin_config
                if self.output:
                    DEFAULT_OUTPUT_CONSOLE.log(f"Start adding glow effect to CameraFollowCursorCVScene.mp4. [dim](by moviepy)[/]\n")

                input_path = Path(scene.renderer.file_writer.movie_file_path)
                output_path = str(input_path.with_name(f"{Parameters.video_name}.mp4"))
                total_effect_time = timeit(lambda: addGlowEffect(input_path=input_path, output_path=output_path, output=self.output), number=1)
                if self.output:
                    DEFAULT_OUTPUT_CONSOLE.log(f"Successfully added glow effect in {total_effect_time:,.2f} seconds. [dim](by moviepy)[/]")
                    DEFAULT_OUTPUT_CONSOLE.log(f"File ready at '{output_path}'.")
                del input_path, output_path, total_effect_time

        return CameraFollowCursorCVScene()

    def render(self, output=DEFAULT_OUTPUT_VALUE):
        self.output = output
        self.scene.render()

    def __getattribute__(self, name):
        frames = inspect.stack()
        is_internal_call = False

        for frame in frames[1:]:
            frame_self = frame.frame.f_locals.get('self')
            if isinstance(frame_self, CameraFollowCursorCV):
                is_internal_call = True
                break

        if not is_internal_call:
            allowed_attrs = super().__getattribute__("__all__")
            if name not in allowed_attrs:
                raise AttributeError(f"'CameraFollowCursorCV' object has no attribute '{name}'")

        return super().__getattribute__(name)

__all__ = ["CameraFollowCursorCV"]
