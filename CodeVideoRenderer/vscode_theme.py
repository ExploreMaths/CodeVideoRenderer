"""VS Code Dark+ syntax-highlighting style and Python lexer."""
from pygments.filter import Filter
from pygments.style import Style
from pygments.token import (
    Token, Keyword, Name, Comment, String, Error, Number, Operator,
    Punctuation, Literal, Generic, Whitespace,
)
from pygments.lexers.python import PythonLexer

__all__ = [
    "VSCodeDarkPlusStyle",
    "VSCodePythonLexer",
    "register_vscode",
    "resolve_language",
    "STYLE_NAME",
    "LEXER_NAME",
]

STYLE_NAME = "vscode-dark-plus"
LEXER_NAME = "python-vscode"

PYTHON_LANGUAGES = {"python", "python3", "py", "py3", "python2", "py2"}


def resolve_language(language):
    return LEXER_NAME if language in PYTHON_LANGUAGES else language


class VSCodeDarkPlusStyle(Style):
    name = STYLE_NAME
    background_color = "#1E1E1E"
    styles = {
        Token: "#D4D4D4",
        Whitespace: "",
        Comment: "#6A9955",
        Comment.Preproc: "#C586C0",
        # def/class/lambda blue; if/for/return… purple
        Keyword: "#569CD6",
        Keyword.Constant: "#569CD6",
        Keyword.Declaration: "#569CD6",
        Keyword.Reserved: "#C586C0",
        Keyword.Namespace: "#569CD6",
        Keyword.Type: "#4EC9B0",
        Operator: "#D4D4D4",
        Operator.Word: "#C586C0",        # and/or/not/in/is
        Name: "#D4D4D4",
        Name.Builtin: "#DCDCAA",         # print/len/range
        Name.Builtin.Pseudo: "#9CDCFE",  # self/cls
        Name.Function: "#DCDCAA",
        Name.Function.Magic: "#DCDCAA",
        Name.Class: "#4EC9B0",
        Name.Namespace: "#4EC9B0",
        Name.Exception: "#4EC9B0",
        Name.Decorator: "#DCDCAA",
        Name.Variable: "#9CDCFE",
        Name.Constant: "#9CDCFE",
        Name.Attribute: "#9CDCFE",
        Name.Tag: "#569CD6",
        Name.Label: "#9CDCFE",
        String: "#CE9178",
        String.Doc: "#CE9178",
        String.Interpol: "#CE9178",
        String.Escape: "#CE9178",
        String.Regex: "#CE9178",
        String.Symbol: "#CE9178",
        String.Other: "#CE9178",
        Number: "#B5CEA8",
        Punctuation: "#D4D4D4",
        Literal: "#B5CEA8",
        Generic: "#D4D4D4",
        Error: "#F44747",
    }


# control-flow keywords stay purple; the rest become blue (def/class)
_CONTROL_KEYWORDS = {
    "if", "elif", "else", "for", "while", "return", "break", "continue",
    "pass", "raise", "try", "except", "finally", "with", "assert",
    "import", "from", "as", "global", "nonlocal", "yield",
    "and", "or", "not", "is", "in", "del", "async", "await",
}


class _VSKeywordFilter(Filter):
    def filter(self, lexer, stream):
        for ttype, value in stream:
            if ttype is Keyword:
                if value in _CONTROL_KEYWORDS:
                    yield Keyword.Reserved, value
                else:
                    yield Keyword.Declaration, value
            else:
                yield ttype, value


class VSCodePythonLexer(PythonLexer):
    name = "Python (VS Code)"
    aliases = [LEXER_NAME]
    filenames = ["*.py"]

    def __init__(self, **options):
        super().__init__(**options)
        self.add_filter(_VSKeywordFilter())


_registered = False


def register_vscode():
    global _registered
    if _registered:
        return
    try:
        from pygments.styles import _STYLE_NAME_TO_MODULE_MAP
        _STYLE_NAME_TO_MODULE_MAP[STYLE_NAME] = (
            "CodeVideoRenderer.vscode_theme",
            "VSCodeDarkPlusStyle",
        )

        from pygments.lexers import LEXERS, _lexer_cache
        LEXERS["VSCodePythonLexer"] = (
            "CodeVideoRenderer.vscode_theme",
            VSCodePythonLexer.name,
            VSCodePythonLexer.aliases,
            VSCodePythonLexer.filenames,
            ("text/x-python",),
        )
        _lexer_cache[VSCodePythonLexer.name] = VSCodePythonLexer
        _registered = True
    except Exception:
        # fall back to Pygments' built-in python lexer if registration fails
        _registered = False


register_vscode()
