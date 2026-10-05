"""ffmpeg wrappers for post-processing rendered videos: subtitles, audio, quality, overlays."""
import json
import os
import shutil
import subprocess
import tempfile
from fractions import Fraction
from pathlib import Path

from .config import FFMPEG_THREADS, FFMPEG_PRESET, FFMPEG_BUFSIZE

_POSITION_ALIASES = {
    "top-left": "tl",
    "top-right": "tr",
    "bottom-left": "bl",
    "bottom-right": "br",
    "center": "center",
    "tl": "tl",
    "tr": "tr",
    "bl": "bl",
    "br": "br",
}

_RESOLUTION_PRESETS = {
    "480p": (854, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "2k": (2560, 1440),
    "4k": (3840, 2160),
}


def find_ffmpeg():
    for var in ("CODEVIDEORENDERER_FFMPEG", "FFMPEG_BINARY"):
        candidate = os.environ.get(var)
        if candidate and Path(candidate).exists():
            return str(Path(candidate))

    which = shutil.which("ffmpeg")
    if which:
        return which

    common = [
        r"C:\ffmpeg\bin\ffmpeg.exe",
        r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
        "/usr/local/bin/ffmpeg",
        "/usr/bin/ffmpeg",
        "/opt/homebrew/bin/ffmpeg",
    ]
    for candidate in common:
        if Path(candidate).exists():
            return candidate

    try:
        import imageio_ffmpeg

        bundled = imageio_ffmpeg.get_ffmpeg_exe()
        if bundled and Path(bundled).exists():
            return bundled
    except Exception:
        pass

    raise FileNotFoundError(
        "Could not locate ffmpeg. Install it and make it available on PATH, or "
        "set the CODEVIDEORENDERER_FFMPEG environment variable to its full path."
    )


def find_ffprobe():
    ffmpeg = Path(find_ffmpeg())
    name = "ffprobe.exe" if os.name == "nt" else "ffprobe"
    candidate = ffmpeg.with_name(name)
    if candidate.exists():
        return str(candidate)

    which = shutil.which("ffprobe")
    if which:
        return which

    raise FileNotFoundError("Could not locate ffprobe (expected next to ffmpeg).")


def _run_ffmpeg(args):
    # output path is always the last argument; inject encode options before it
    opts = ["-threads", str(FFMPEG_THREADS)]
    if "libx264" in args:
        opts += ["-preset", FFMPEG_PRESET, "-bufsize", FFMPEG_BUFSIZE]
    cmd = [find_ffmpeg(), "-hide_banner", "-loglevel", "error", "-y", *args[:-1], *opts, args[-1]]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg failed ({proc.returncode}): {proc.stderr.strip()}")


def _run_ffprobe(args):
    cmd = [find_ffprobe(), "-v", "error", *args]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"ffprobe failed ({proc.returncode}): {proc.stderr.strip()}")
    return proc.stdout


def _default_output(input_path, tag):
    p = Path(input_path)
    return str(p.with_name(f"{p.stem}_{tag}{p.suffix}"))


def _ffmpeg_filter_path(path):
    p = str(path).replace("\\", "/")
    if os.name == "nt":
        p = p.replace(":", r"\:")
    return p


def _drawtext_escape(text):
    return (
        text.replace("\\", "\\\\")
        .replace(":", "\\:")
        .replace("'", "\\'")
        .replace("%", "\\%")
    )


def _default_font():
    candidates = [
        r"C:\Windows\Fonts\msyh.ttc",  # Microsoft YaHei
        r"C:\Windows\Fonts\msyh.ttf",
        r"C:\Windows\Fonts\simhei.ttf",
        r"C:\Windows\Fonts\simsun.ttc",
        r"C:\Windows\Fonts\arial.ttf",
        "/System/Library/Fonts/PingFang.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return candidate
    return ""


def _has_audio_stream(path):
    out = _run_ffprobe(["-select_streams", "a", "-show_entries", "stream=index", "-of", "json", str(path)])
    try:
        return bool(json.loads(out).get("streams"))
    except Exception:
        return False


def _probe_video_info(path):
    out = _run_ffprobe(
        [
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height,r_frame_rate",
            "-of",
            "json",
            str(path),
        ]
    )
    stream = json.loads(out)["streams"][0]
    fps = float(Fraction(stream.get("r_frame_rate", "30/1")))
    return int(stream["width"]), int(stream["height"]), fps


def _parse_resolution(resolution):
    # -2 width keeps the aspect ratio (ffmpeg scale=-2:HEIGHT)
    if isinstance(resolution, (tuple, list)) and len(resolution) == 2:
        return int(resolution[0]), int(resolution[1])
    if isinstance(resolution, int):
        return -2, int(resolution)
    key = str(resolution).lower()
    if key in _RESOLUTION_PRESETS:
        return _RESOLUTION_PRESETS[key]
    raise ValueError(
        f"Unsupported resolution {resolution!r}. Use a preset "
        f"({', '.join(_RESOLUTION_PRESETS)}), a height (int), or a (width, height) tuple."
    )


def remove_subtitles(input_path, output_path=None):
    output_path = output_path or _default_output(input_path, "no_subs")
    _run_ffmpeg(["-i", str(input_path), "-map", "0", "-c", "copy", "-sn", str(output_path)])
    return str(output_path)


def add_subtitles(
    input_path,
    subtitle_path,
    output_path=None,
    soft=False,
    style=None,
    font=None,
    fontsize=None,
    color=None,
    position=None,
    margin=None,
):
    output_path = output_path or _default_output(input_path, "subbed")

    if soft:
        _run_ffmpeg(
            [
                "-i", str(input_path),
                "-i", str(subtitle_path),
                "-map", "0", "-map", "1",
                "-c", "copy", "-c:s", "mov_text",
                "-metadata:s:s:0", "language=chi",
                str(output_path),
            ]
        )
    else:
        vf = f"subtitles='{_ffmpeg_filter_path(subtitle_path)}'"
        force = dict(style or {})
        if font:
            force["Fontname"] = font
        if fontsize:
            force["Fontsize"] = str(fontsize)
        if color:
            force["PrimaryColour"] = _ass_color(color)
        if position:
            force["Alignment"] = str(_ass_alignment(position))
        if margin:
            force["MarginV"] = str(margin)
        if force:
            vf += ":force_style='" + ",".join(f"{k}={v}" for k, v in force.items()) + "'"
        _run_ffmpeg(
            [
                "-i", str(input_path),
                "-vf", vf,
                "-c:v", "libx264", "-c:a", "copy",
                str(output_path),
            ]
        )
    return str(output_path)


def add_background_music(
    input_path,
    music_path,
    output_path=None,
    volume=0.3,
    loop=True,
    mix_original=True,
):
    output_path = output_path or _default_output(input_path, "bgm")
    loop_args = ["-stream_loop", "-1"] if loop else []
    has_audio = _has_audio_stream(input_path)

    if has_audio and mix_original:
        filter_complex = (
            f"[1:a]volume={volume}[bg];"
            f"[0:a][bg]amix=inputs=2:duration=first:normalize=0[aout]"
        )
        audio_map = "[aout]"
    else:
        filter_complex = f"[1:a]volume={volume}[bg]"
        audio_map = "[bg]"

    _run_ffmpeg(
        [
            "-i", str(input_path),
            *loop_args,
            "-i", str(music_path),
            "-filter_complex", filter_complex,
            "-map", "0:v", "-map", audio_map,
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            str(output_path),
        ]
    )
    return str(output_path)


def extract_audio(input_path, output_path=None, format="mp3"):
    fmt = format.lower().lstrip(".")
    codecs = {"mp3": "libmp3lame", "wav": "pcm_s16le", "m4a": "aac", "aac": "aac"}
    if fmt not in codecs:
        raise ValueError(f"Unsupported audio format {format!r}. Choose from {sorted(codecs)}.")

    if output_path is None:
        output_path = str(Path(input_path).with_suffix(f".{fmt}"))
    _run_ffmpeg(["-i", str(input_path), "-vn", "-acodec", codecs[fmt], str(output_path)])
    return str(output_path)


def remove_audio(input_path, output_path=None):
    output_path = output_path or _default_output(input_path, "mute")
    _run_ffmpeg(["-i", str(input_path), "-c", "copy", "-an", str(output_path)])
    return str(output_path)


def concat_videos(
    input_paths,
    output_path,
    reencode=False,
):
    paths = [str(Path(p).resolve()) for p in input_paths]
    if len(paths) < 2:
        raise ValueError("concat_videos requires at least two input videos.")

    if reencode:
        inputs = []
        for p in paths:
            inputs += ["-i", p]
        n = len(paths)
        has_audio_flags = [_has_audio_stream(p) for p in paths]

        # Normalize video streams to yuv420p so differing pixel formats do not break concat
        v_parts = [f"[{i}:v]format=yuv420p[v{i}]" for i in range(n)]

        if all(has_audio_flags):
            a_parts = [f"[{i}:a]aformat=sample_rates=44100:channel_layouts=stereo[a{i}]" for i in range(n)]
            joins = "".join(f"[v{i}][a{i}]" for i in range(n))
            filter_complex = ";".join(v_parts + a_parts) + ";" + joins + f"concat=n={n}:v=1:a=1[v][a]"
            _run_ffmpeg(
                [
                    *inputs,
                    "-filter_complex", filter_complex,
                    "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-c:a", "aac",
                    str(output_path),
                ]
            )
        elif not any(has_audio_flags):
            joins = "".join(f"[v{i}]" for i in range(n))
            filter_complex = ";".join(v_parts) + ";" + joins + f"concat=n={n}:v=1:a=0[v]"
            _run_ffmpeg(
                [
                    *inputs,
                    "-filter_complex", filter_complex,
                    "-map", "[v]",
                    "-c:v", "libx264", "-an",
                    str(output_path),
                ]
            )
        else:
            raise ValueError(
                "concat_videos(reencode=True) requires all inputs to either have audio or "
                "all to be silent; mixed audio presence is not supported. Normalise the "
                "inputs first (e.g. with remove_audio / add_background_music)."
            )
        return str(output_path)

    with tempfile.TemporaryDirectory() as tmp:
        list_file = Path(tmp) / "concat.txt"
        list_file.write_text(
            "".join(f"file '{p}'" + "\n" for p in paths),
            encoding="utf-8",
        )
        _run_ffmpeg(["-f", "concat", "-safe", "0", "-i", str(list_file), "-c", "copy", str(output_path)])
    return str(output_path)


def set_quality(
    input_path,
    output_path=None,
    resolution=None,
    fps=None,
    bitrate=None,
    crf=None,
):
    output_path = output_path or _default_output(input_path, "quality")
    args = ["-i", str(input_path)]

    if resolution is not None:
        width, height = _parse_resolution(resolution)
        if width == -2:
            vf = f"scale=-2:{height}"
        else:
            vf = f"scale={width}:{height}"
        args += ["-vf", vf]

    args += ["-c:v", "libx264"]
    if fps is not None:
        args += ["-r", str(fps)]
    if bitrate is not None:
        args += ["-b:v", str(bitrate)]
    if crf is not None:
        args += ["-crf", str(crf)]
    args += ["-c:a", "aac", "-b:a", "192k", str(output_path)]

    _run_ffmpeg(args)
    return str(output_path)


def trim_video(
    input_path,
    output_path=None,
    start=0.0,
    end=None,
    duration=None,
):
    output_path = output_path or _default_output(input_path, "trim")
    args = ["-i", str(input_path), "-ss", str(start)]
    if duration is not None:
        args += ["-t", str(duration)]
    elif end is not None:
        args += ["-to", str(end)]
    args += ["-c", "copy", str(output_path)]
    _run_ffmpeg(args)
    return str(output_path)


def change_speed(
    input_path,
    output_path=None,
    speed=1.0,
):
    if speed <= 0:
        raise ValueError("speed must be greater than 0")
    output_path = output_path or _default_output(input_path, f"speed{speed}".replace(".", "_"))
    _run_ffmpeg(
        [
            "-i", str(input_path),
            "-filter_complex", f"[0:v]setpts={1 / speed:.6f}*PTS[v];[0:a]atempo={speed}[a]",
            "-map", "[v]", "-map", "[a]",
            str(output_path),
        ]
    )
    return str(output_path)


def _overlay_position(position, margin):
    pos = _POSITION_ALIASES.get(position.lower(), "br")
    if pos == "tl":
        return f"{margin}", f"{margin}"
    if pos == "tr":
        return f"W-w-{margin}", f"{margin}"
    if pos == "bl":
        return f"{margin}", f"H-h-{margin}"
    if pos == "center":
        return "(W-w)/2", "(H-h)/2"
    return f"W-w-{margin}", f"H-h-{margin}"  # bottom-right


def _drawtext_position(position, margin):
    pos = _POSITION_ALIASES.get(position.lower(), "br")
    if pos == "tl":
        return f"{margin}", f"{margin}"
    if pos == "tr":
        return f"w-text_w-{margin}", f"{margin}"
    if pos == "bl":
        return f"{margin}", f"h-text_h-{margin}"
    if pos == "center":
        return "(w-text_w)/2", "(h-text_h)/2"
    return f"w-text_w-{margin}", f"h-text_h-{margin}"


def add_watermark(
    input_path,
    output_path=None,
    text=None,
    image_path=None,
    position="bottom-right",
    fontsize=24,
    opacity=0.6,
    color="white",
    margin=20,
):
    if text is None and image_path is None:
        raise ValueError("Provide either `text` or `image_path` for the watermark.")
    output_path = output_path or _default_output(input_path, "wm")

    if image_path is not None:
        x, y = _overlay_position(position, margin)
        _run_ffmpeg(
            [
                "-i", str(input_path),
                "-i", str(image_path),
                "-filter_complex",
                f"[1]format=rgba,colorchannelmixer=aa={opacity}[wm];[0][wm]overlay={x}:{y}",
                "-c:a", "copy",
                str(output_path),
            ]
        )
        return str(output_path)

    font = _default_font()
    x, y = _drawtext_position(position, margin)
    drawtext = (
        f"drawtext=text='{_drawtext_escape(text)}'"
        f":x={x}:y={y}"
        f":fontsize={fontsize}"
        f":fontcolor={color}@{opacity}"
    )
    if font:
        drawtext += f":fontfile='{_ffmpeg_filter_path(font)}'"
    _run_ffmpeg(["-i", str(input_path), "-vf", drawtext, "-c:a", "copy", str(output_path)])
    return str(output_path)


def add_title_card(
    input_path,
    output_path=None,
    title=None,
    subtitle=None,
    duration=3.0,
    background_color="black",
    title_color="white",
    subtitle_color="0xCCCCCC",
    fontsize=64,
):
    output_path = output_path or _default_output(input_path, "titled")
    title = title or Path(input_path).stem
    width, height, fps = _probe_video_info(input_path)
    font = _default_font()

    text = _drawtext_escape(title)
    drawtext = (
        f"drawtext=text='{text}'"
        f":x=(w-text_w)/2:y=(h-text_h)/2-40"
        f":fontsize={fontsize}:fontcolor={title_color}"
    )
    if subtitle:
        drawtext += (
            f",drawtext=text='{_drawtext_escape(subtitle)}'"
            f":x=(w-text_w)/2:y=(h)/2+60"
            f":fontsize={fontsize // 2}:fontcolor={subtitle_color}"
        )
    if font:
        drawtext = drawtext.replace("fontsize=", f"fontfile='{_ffmpeg_filter_path(font)}':fontsize=")

    with tempfile.TemporaryDirectory() as tmp:
        title_clip = Path(tmp) / "title.mp4"
        has_audio = _has_audio_stream(input_path)

        # Keep the title card's audio stream consistent with the source video so concat(reencode) joins cleanly
        title_args = [
            "-f", "lavfi",
            "-i", f"color=c={background_color}:s={width}x{height}:d={duration}:r={fps}",
        ]
        if has_audio:
            title_args += ["-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo"]
        title_args += ["-vf", drawtext, "-c:v", "libx264", "-pix_fmt", "yuv420p"]
        if has_audio:
            title_args += ["-c:a", "aac", "-shortest"]
        else:
            title_args += ["-an"]
        title_args += [str(title_clip)]
        _run_ffmpeg(title_args)

        concat_videos([title_clip, input_path], output_path, reencode=True)
    return str(output_path)


def extract_cover(
    input_path,
    output_path=None,
    time=0.5,
    width=None,
):
    if output_path is None:
        output_path = str(Path(input_path).with_name(f"{Path(input_path).stem}_cover.png"))
    args = ["-ss", str(time), "-i", str(input_path), "-frames:v", "1"]
    if width is not None:
        args += ["-vf", f"scale={int(width)}:-2"]
    args += [str(output_path)]
    _run_ffmpeg(args)
    return str(output_path)


def _ass_time(seconds):
    ms = int(round(seconds * 1000))
    return f"{ms // 3600000}:{(ms // 60000) % 60:02d}:{(ms // 1000) % 60:02d}.{(ms // 10) % 100:02d}"


def _ass_color(color):
    named = {
        "white": "FFFFFF", "black": "000000", "red": "FF0000", "green": "00FF00",
        "blue": "0000FF", "yellow": "FFFF00", "cyan": "00FFFF", "magenta": "FF00FF",
    }
    c = named.get(str(color).lower(), str(color).lstrip("#").lstrip("0x").lstrip("0X"))
    if len(c) != 6 or any(ch not in "0123456789abcdefABCDEF" for ch in c):
        c = "FFFFFF"
    # ASS stores colour as &HAABBGGRR
    return f"&H00{c[4:6]}{c[2:4]}{c[0:2]}"


def _ass_alignment(position):
    v, _, h = str(position).lower().partition("-")
    v_index = {"bottom": 0, "middle": 1, "top": 2}.get(v, 0)
    h_index = {"left": 0, "center": 1, "right": 2}.get(h, 1)
    return v_index * 3 + h_index + 1


def _build_ass(lyrics, width, height, font, fontsize, color, highlight_color, position, margin, karaoke):
    header = (
        "[Script Info]\n"
        "ScriptType: v4.00+\n"
        f"PlayResX: {width}\n"
        f"PlayResY: {height}\n"
        "WrapStyle: 2\n"
        "\n"
        "[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
        f"Style: Default,{font or 'Arial'},{fontsize},{_ass_color(color)},{_ass_color(highlight_color)},{_ass_color(color)},&H00000000,0,0,0,0,100,100,0,0,1,2,0,{_ass_alignment(position)},10,10,{margin},1\n"
        "\n"
        "[Events]\n"
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    )
    out = [header]
    for start, end, text in lyrics:
        text = str(text).replace("\\", "\\\\").replace("\n", "\\N")
        if karaoke:
            text = f"{{\\k{int(round((end - start) * 100))}}}{text}"
        out.append(f"Dialogue: 0,{_ass_time(start)},{_ass_time(end)},Default,,0,0,0,,{text}")
    return "\n".join(out) + "\n"


def add_background(
    input_path,
    output_path=None,
    color=None,
    image=None,
    blur=0,
):
    output_path = output_path or _default_output(input_path, "bg")
    width, height, _ = _probe_video_info(input_path)

    if image is not None:
        filter_complex = (
            f"[1:v]scale={width}:{height}:force_original_aspect_ratio=increase,"
            f"crop={width}:{height},gblur=sigma={blur}[bg];"
            f"[0:v]format=rgba[fg];[bg][fg]overlay=0:0"
        )
        _run_ffmpeg(
            [
                "-i", str(input_path),
                "-loop", "1", "-i", str(image),
                "-filter_complex", filter_complex,
                "-map", "0:a?", "-c:a", "copy",
                "-shortest",
                str(output_path),
            ]
        )
        return str(output_path)

    _run_ffmpeg(
        [
            "-f", "lavfi", "-i", f"color=c={color or 'black'}:s={width}x{height}",
            "-i", str(input_path),
            "-filter_complex", "[1:v]format=rgba[fg];[0:v][fg]overlay=0:0",
            "-map", "1:a?", "-c:a", "copy",
            "-shortest",
            str(output_path),
        ]
    )
    return str(output_path)


def replace_background(
    input_path,
    background,
    output_path=None,
    key_color="0x00FF00",
    similarity=0.3,
    blend=0.1,
    blur=0,
):
    output_path = output_path or _default_output(input_path, "bg")
    width, height, _ = _probe_video_info(input_path)
    filter_complex = (
        f"[0:v]chromakey={key_color}:{similarity}:{blend}[fg];"
        f"[1:v]scale={width}:{height}:force_original_aspect_ratio=increase,"
        f"crop={width}:{height},gblur=sigma={blur}[bg];"
        f"[bg][fg]overlay=0:0"
    )
    _run_ffmpeg(
        [
            "-i", str(input_path),
            "-loop", "1", "-i", str(background),
            "-filter_complex", filter_complex,
            "-map", "0:a?", "-c:a", "copy",
            "-shortest",
            str(output_path),
        ]
    )
    return str(output_path)


def add_sound(
    input_path,
    sound,
    output_path=None,
    at=0.0,
    volume=1.0,
):
    output_path = output_path or _default_output(input_path, "sfx")
    delay = int(round(at * 1000))
    sfx = f"[1:a]volume={volume},adelay={delay}|{delay}[sfx]"
    if _has_audio_stream(input_path):
        fc = f"{sfx};[0:a][sfx]amix=inputs=2:duration=first:normalize=0[aout]"
        audio_map = "[aout]"
    else:
        fc = sfx
        audio_map = "[sfx]"
    _run_ffmpeg(
        [
            "-i", str(input_path),
            "-i", str(sound),
            "-filter_complex", fc,
            "-map", "0:v", "-map", audio_map,
            "-c:v", "copy", "-c:a", "aac",
            str(output_path),
        ]
    )
    return str(output_path)


def add_lyrics(
    input_path,
    lyrics,
    output_path=None,
    font="",
    fontsize=48,
    color="white",
    highlight_color="yellow",
    position="bottom-center",
    margin=80,
    karaoke=True,
):
    output_path = output_path or _default_output(input_path, "lyrics")
    width, height, _ = _probe_video_info(input_path)
    ass = _build_ass(lyrics, width, height, font, fontsize, color, highlight_color, position, margin, karaoke)
    with tempfile.TemporaryDirectory() as tmp:
        ass_path = Path(tmp) / "lyrics.ass"
        ass_path.write_text(ass, encoding="utf-8")
        vf = f"subtitles='{_ffmpeg_filter_path(ass_path)}'"
        _run_ffmpeg(
            [
                "-i", str(input_path),
                "-vf", vf,
                "-c:v", "libx264", "-c:a", "copy",
                str(output_path),
            ]
        )
    return str(output_path)


__all__ = [
    "find_ffmpeg",
    "find_ffprobe",
    "remove_subtitles",
    "add_subtitles",
    "add_background_music",
    "extract_audio",
    "remove_audio",
    "concat_videos",
    "set_quality",
    "trim_video",
    "change_speed",
    "add_watermark",
    "add_title_card",
    "extract_cover",
    "add_background",
    "replace_background",
    "add_sound",
    "add_lyrics",
]
