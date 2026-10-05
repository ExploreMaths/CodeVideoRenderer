# Prefer the installed distribution's version; fall back to this when running from source.
__version__ = "1.5.0"

try:
    from importlib.metadata import version as _pkg_version
    __version__ = _pkg_version("codevideorenderer")
except Exception:  # pragma: no cover - only triggered when the distribution is not installed
    pass
