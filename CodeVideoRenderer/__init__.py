"""Code video rendering built on Manim: animate code being typed while the camera follows the cursor."""
from .renderer import *
from .config import *
from .typing import *
from .utils import *
from .postprocess import *
from .vscode_theme import VSCodeDarkPlusStyle, register_vscode, STYLE_NAME
from .ime import is_cjk, cjk_run_at, get_ime
from .version import __version__
