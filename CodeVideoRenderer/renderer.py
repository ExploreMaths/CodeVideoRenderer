from manim import VGroup, Code, SurroundingRectangle, RoundedRectangle, MovingCameraScene, rate_functions, RendererType, config, WHITE, GREY, UP, DOWN, LEFT, RIGHT, register_font
from manim.typing import Point3D
from pathlib import Path
from copy import copy
from typing import Literal, Union
from timeit import timeit
from rich import traceback
from dataclasses import dataclass
import numpy as np
import random, inspect, os

from .config import *
from .typing import *
from .utils import *

traceback.install()

class CameraFollowCursorCV:
    """
    CameraFollowCursorCV is a class designed to create animated videos that simulate the process of typing code. It animates code line by line and character by 
    character while smoothly moving the camera to follow the cursor, creating a professional-looking coding demonstration.

    Args:
        code (Union[tuple[Literal['string'], str], tuple[Literal['file'], StrPath]]): The code to be animated. **When using a string**, provide a tuple with the first element as `'string'` and the second element as the code string. **When using a file**, provide a tuple with the first element as `'file'` and the second element as the file path.
        language (PygmentsLanguage): The programming language of the code.
        formatter_style (PygmentsFormatterStyle): The style for syntax highlighting. Defaults to `"github-dark"`.
        line_spacing (float | int): The line spacing for the code. Defaults to `DEFAULT_LINE_SPACING`.
        interval_range (tuple[float | int, float | int]): The range of typing intervals between characters. Defaults to `(DEFAULT_TYPE_INTERVAL, DEFAULT_TYPE_INTERVAL)`.
        camera_scale (float | int): The scale factor for the camera. Defaults to 0.5.
        video_name (str): The name of the output video file. Defaults to `"CameraFollowCursorCV"`.
        renderer (Literal['cairo', 'opengl']): The renderer to use for video rendering. Defaults to `'cairo'`.
    """
    __all__ = ["render"]

    @typeChecker
    def __init__(self,
        code: Union[tuple[Literal['string'], str], tuple[Literal['file'], StrPath]],
        language: PygmentsLanguage,
        formatter_style: PygmentsFormatterStyle = "github-dark",
        line_spacing: float | int = DEFAULT_LINE_SPACING,
        interval_range: tuple[float | int, float | int] = (DEFAULT_TYPE_INTERVAL, DEFAULT_TYPE_INTERVAL),
        camera_scale: float | int = 0.5,
        video_name: str = "CameraFollowCursorCV",
        renderer: Literal['cairo', 'opengl'] = 'cairo',
    ):
        # ----- 视频名称 -----
        if not video_name:
            raise ValueError("video_name must be provided")
        
        # ----- 代码输入 -----
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
        
        # ----- 行间距 -----
        if line_spacing <= 0:
            raise ValueError("line_spacing must be greater than 0")

        # ----- 打字间隔 -----
        shortest_possible_duration = round(1/config.frame_rate, 7)
        if not all(interval >= shortest_possible_duration for interval in interval_range):
            raise ValueError(f"interval_range must be greater than or equal to {shortest_possible_duration}")
        del shortest_possible_duration
        if interval_range[0] > interval_range[1]:
            raise ValueError("The first term of interval_range must be less than or equal to the second term")

        # 参数
        global Parameters
        @dataclass
        class Parameters:
            code: Union[tuple[Literal['string'], str], tuple[Literal['file'], StrPath]]
            language: PygmentsLanguage
            formatter_style: PygmentsFormatterStyle
            line_spacing: float | int
            interval_range: tuple[float | int, float | int]
            camera_scale: float | int
            video_name: str
            renderer: Literal['cairo', 'opengl']
        Parameters.code = code
        Parameters.language = language
        Parameters.formatter_style = formatter_style
        Parameters.line_spacing = line_spacing
        Parameters.interval_range = interval_range
        Parameters.camera_scale = camera_scale
        Parameters.video_name = video_name
        Parameters.renderer = renderer

        # 其他
        self.code_str = stripEmptyLines(self.code_str)
        self.space_positions = findSpacePositions(self.code_str)
        self.empty_line_positions = findEmptyLinePositions(self.code_str)
        self.code_str = replaceMiddleSpacesWithOccupyCharacter("\n".join([" " if line == "" else line for line in self.code_str.splitlines()]))
        self.code_str_lines = self.code_str.splitlines()
        self.origin_config = {
            'disable_caching': config.disable_caching,
            'renderer': config.renderer
        }
        config.disable_caching = True
        config.renderer = renderer
        self.scene = self._create_scene()

    def _create_scene(self):
        """Create manim scene to animate code rendering."""
        class CameraFollowCursorCVScene(MovingCameraScene):

            def construct(scene):
                """Build the code animation scene."""

                # 初始化光标
                cursor = RoundedRectangle(
                    height=DEFAULT_CURSOR_HEIGHT,
                    width=DEFAULT_CURSOR_WIDTH,
                    corner_radius=DEFAULT_CURSOR_WIDTH / 2,
                    fill_opacity=1,
                    fill_color=WHITE,
                    color=WHITE
                )

                # 创建代码块
                with register_font(os.path.join(os.path.dirname(__file__), 'fonts/CodeVideoRendererFont.ttf')):
                    line_number_mobject, code_mobject = Code(
                        code_string=self.code_str + f"\n{(max([len(line.rstrip()) for line in self.code_str_lines])*2)*' ' + OCCUPY_CHARACTER}",
                        language=Parameters.language, 
                        formatter_style=Parameters.formatter_style, 
                        paragraph_config={
                            'font': 'CodeVideoRendererFont',
                            'line_spacing': Parameters.line_spacing
                        }
                    ).submobjects[1:3]
                line_number_mobject.set_color(GREY)

                total_line_numbers = len(self.code_str_lines)
                total_char_numbers = len(''.join(line.strip() for line in self.code_str_lines))

                # 调整代码对齐（manim内置bug）
                offset_lines = []
                for line_index, line in enumerate(self.code_str_lines):
                    if all(check in "acegmnopqrsuvwxyz+,-.:;<=>_~ " for check in line):
                        if line_index == 0:
                            code_mobject.shift(DOWN*CODE_OFFSET)
                        offset_lines.append(line_index)
                del line_index, line
                    
                # 创建代码行矩形框
                code_line_rectangle = SurroundingRectangle(
                    VGroup(code_mobject[-1], line_number_mobject[-1]), # type: ignore[reportArgumentType]
                    color="#333333",
                    fill_opacity=1,
                    stroke_width=0
                ).set_y(code_mobject[0].get_y())
                # 处理第一行出现代码偏移时的code_line_rectangle偏移问题
                if 0 in offset_lines:
                    code_line_rectangle.shift(UP*CODE_OFFSET/2)
                
                # 初始化光标位置
                cursor.align_to(code_mobject[0], LEFT).set_y(code_line_rectangle.get_y())

                # 适配opengl
                if config.renderer == RendererType.OPENGL:
                    scene.camera.frame = scene.camera # type: ignore[reportAttributeAccessIssue]

                # 入场动画
                target_center = cursor.get_center()
                start_center = target_center + UP * 3
                scene.camera.frame.scale(Parameters.camera_scale).move_to(start_center) # type: ignore[reportAttributeAccessIssue]
                scene.add(code_line_rectangle, line_number_mobject[0].set_color(WHITE), cursor)

                scene.play(
                    scene.camera.frame.animate.move_to(target_center), # type: ignore[reportArgumentType, reportAttributeAccessIssue]
                    run_time=1,
                    rate_func=rate_functions.ease_out_cubic
                )
                
                # 定义固定动画
                scene.Animation_list: list[dict[str, Point3D | float]] = []
                def linebreakAnimation():
                    scene.Animation_list.append({"move_to": cursor.get_center()})

                camera_scale = Parameters.camera_scale
                def JUDGE_cameraScaleAnimation():
                    nonlocal camera_scale
                    distance = (scene.camera.frame.get_x() - line_number_mobject.get_x()) / 14.22 # type: ignore[reportAttributeAccessIssue]
                    if distance > camera_scale:
                        scene.Animation_list.append({"scale": distance/camera_scale})
                        camera_scale = distance

                def playAnimation(**kwargs):
                    if scene.Animation_list:
                        cameraAnimation = scene.camera.frame.animate # type: ignore[reportAttributeAccessIssue]

                        for anim in scene.Animation_list:
                            if "move_to" in anim:
                                cameraAnimation.move_to(anim["move_to"])
                            elif "scale" in anim:
                                cameraAnimation.scale(anim["scale"])
                        
                        scene.play(cameraAnimation, **kwargs)
                        scene.Animation_list.clear()
                        del cameraAnimation

                with copy(DefaultProgressBar(self.output)) as progress:
                    total_progress = progress.add_task(description="[yellow]Total[/yellow]", total=total_char_numbers)

                    # 遍历代码行
                    for line in range(total_line_numbers):

                        line_number_mobject.set_color(GREY)
                        line_number_mobject[line].set_color(WHITE)

                        char_num = len(self.code_str_lines[line].strip())
                        current_line_progress = progress.add_task(description=f"[green]Line {line+1}[/green]", total=char_num)

                        code_line_rectangle.set_y(code_mobject[line].get_y())
                        # 处理出现代码偏移时的code_line_rectangle偏移问题
                        if line in offset_lines:
                            code_line_rectangle.shift(UP*CODE_OFFSET/2)
                        scene.add(line_number_mobject[line])

                        cursor.align_to(code_mobject[line], LEFT).set_y(code_line_rectangle.get_y())
                        if line != 0:
                            linebreakAnimation()
                        JUDGE_cameraScaleAnimation()
                        playAnimation(run_time=DEFAULT_LINE_BREAK_RUN_TIME)

                        # 如果当前行为空行，跳过
                        if line in self.empty_line_positions:
                            progress.remove_task(current_line_progress)
                            continue
                        
                        first_non_space_index = len(self.code_str_lines[line]) - len(self.code_str_lines[line].lstrip())
                        total_typing_chars = char_num # 当前行实际要打的字数

                        # 遍历当前行的每个字符
                        submobjects_char_index = 0
                        for column in range(first_non_space_index, char_num + first_non_space_index):
                            # 处理manim==0.19.1更新出现的空格消失问题
                            if not self.code_str_lines[line][column].isspace():
                                if [line, column] not in self.space_positions:
                                    scene.add(code_mobject[line][submobjects_char_index])
                                submobjects_char_index += 1
                            cursor.next_to(
                                code_mobject[line][submobjects_char_index-1],
                                RIGHT,
                                buff=DEFAULT_CURSOR_TO_CHAR_BUFFER
                            ).set_y(code_line_rectangle.get_y())
                            
                            # 相机持续摆动逻辑
                            line_break = False
                            if column == first_non_space_index and first_non_space_index != 0:
                                # 如果是缩进后的第一个字符，先执行换行归位
                                linebreakAnimation()
                                line_break = True
                            else:
                                # 计算当前行的进度 (0.0 -> 1.0)
                                current_idx = column - first_non_space_index
                                max_idx = total_typing_chars - 1
                                
                                if max_idx > 0:
                                    alpha = current_idx / max_idx
                                else:
                                    alpha = 1.0
                                
                                # 包络线 sin(alpha * pi)，确保头尾为0
                                envelope = np.sin(alpha * np.pi)
                                
                                # 振荡项: sin(alpha * omega)
                                wave_count = total_typing_chars / 15
                                omega = wave_count * 2 * np.pi
                                oscillation = np.sin(alpha * omega)
                                
                                # 振幅为相机框高度的 2.5%
                                amplitude = scene.camera.frame.height * 0.025 # type: ignore[reportAttributeAccessIssue]
                                offset_y = amplitude * envelope * oscillation
                                
                                target_pos = cursor.get_center() + UP * offset_y
                                scene.Animation_list.append({"move_to": target_pos})

                            # 缩放检测 & 播放
                            JUDGE_cameraScaleAnimation()
                            playAnimation(
                                run_time=DEFAULT_LINE_BREAK_RUN_TIME if line_break else random.uniform(*Parameters.interval_range),
                                rate_func=rate_functions.smooth if line_break else rate_functions.linear
                            )

                            # 输出进度
                            progress.advance(total_progress, advance=1)
                            progress.advance(current_line_progress, advance=1)

                        progress.remove_task(current_line_progress)
                    progress.remove_task(total_progress)

                scene.wait()

            def render(scene):
                """Override render to add timing log."""
                if self.output:
                    DEFAULT_OUTPUT_CONSOLE.log(f"Start rendering {Parameters.video_name}.mp4.")
                    DEFAULT_OUTPUT_CONSOLE.log("Start rendering CameraFollowCursorCVScene. [dim](by manim)[/]")
                    if config.renderer == RendererType.CAIRO:
                        DEFAULT_OUTPUT_CONSOLE.log('[blue]Currently using CPU (Cairo Renderer) for rendering.[/]')
                    else:
                        DEFAULT_OUTPUT_CONSOLE.log('[blue]Currently using GPU (OpenGL Renderer) for rendering.[/]')
                    DEFAULT_OUTPUT_CONSOLE.log("Manim's config has been modified.")
                
                # 渲染并计算时间
                with noManimOutput():
                    total_render_time = timeit(super().render, number=1)
                if self.output:
                    DEFAULT_OUTPUT_CONSOLE.log(f"Successfully rendered CameraFollowCursorCVScene in {total_render_time:,.2f} seconds. [dim](by manim)[/]")
                del total_render_time

                # 恢复配置
                config.disable_caching = self.origin_config['disable_caching']
                config.renderer = self.origin_config['renderer']
                if self.output:
                    DEFAULT_OUTPUT_CONSOLE.log("Manim's config has been restored.")
                del self.origin_config
                if self.output:
                    DEFAULT_OUTPUT_CONSOLE.log(f"Start adding glow effect to CameraFollowCursorCVScene.mp4. [dim](by moviepy)[/]\n")

                # 添加发光效果
                input_path = str(scene.renderer.file_writer.movie_file_path)
                output_path = '\\'.join(input_path.split('\\')[:-1]) + rf'\{Parameters.video_name}.mp4'
                total_effect_time = timeit(lambda: addGlowEffect(input_path=input_path, output_path=output_path, output=self.output), number=1)
                if self.output:
                    DEFAULT_OUTPUT_CONSOLE.log(f"Successfully added glow effect in {total_effect_time:,.2f} seconds. [dim](by moviepy)[/]")
                    DEFAULT_OUTPUT_CONSOLE.log(f"File ready at '{output_path}'.")
                del input_path, output_path, total_effect_time

        return CameraFollowCursorCVScene()
    
    @typeChecker
    def render(self, output: bool = DEFAULT_OUTPUT_VALUE):
        """
        Render the scene, optionally with console output.

        Args:
            output (bool): Whether to print console output during rendering. Defaults to `DEFAULT_OUTPUT_VALUE`
        """
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