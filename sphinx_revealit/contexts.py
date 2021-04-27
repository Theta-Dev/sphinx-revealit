"""Contexts for passing between objects."""
from typing import List

from .utils import static_resource_uri, to_json


class RevealjsEngine:
    """Reveal.js core metadata."""

    def __init__(
        self, version: int, js_path: str, css_path: str, theme_dir: str
    ):  # noqa
        self.version = version
        self.js_path = js_path
        self.css_path = css_path
        self.theme_dir = theme_dir

    @classmethod
    def from_version(cls, version: int = 4):  # noqa
        return cls(
            version,
            'revealjs4/dist/reveal.js',
            'revealjs4/dist/reveal.css',
            'revealjs4/dist/theme',
        )


class RevealjsPlugin:
    '''Plugin metadata.'''

    def __init__(self, src: str, name: str = None, options: str = None):  # noqa
        self.src = src
        self.name = name
        self.options = options


class RevealjsProjectContext(object):
    """Context object for Reveal.js (project-wide)."""

    def __init__(
        self,
        engine_version: int,
        script_files: List[str] = None,
        script_conf: dict = None,
        script_plugins: List[RevealjsPlugin] = None,
    ):  # noqa
        self.engine = RevealjsEngine.from_version(engine_version)
        self.script_conf = to_json(script_conf)
        self.script_plugins = script_plugins or []
        self._script_files = script_files or []

    @property
    def script_files(self):  # noqa
        return [static_resource_uri(self.engine.js_path)] + self._script_files
