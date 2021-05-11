"""Definition for sphinx custom builder."""
import copy
import logging
import shutil
from os import path
from typing import Any, Dict, List, Tuple

from docutils.nodes import Node
from docutils.parsers.rst import directives
from importlib_resources import files
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.highlighting import PygmentsBridge
from sphinx.util import progress_message, status_iterator

from sphinx_revealit.collectors import RevealjsImageCollector, CSSClassCollector
from sphinx_revealit.contexts import RevealjsPlugin, RevealjsProjectContext
from sphinx_revealit.csspurge import CSSPurge
from sphinx_revealit.nodes import RevealjsNode
from sphinx_revealit.utils import RjsPygmentsFormatter, static_resource_uri
from sphinx_revealit.writers import RevealjsSlideTranslator

logger = logging.getLogger(__name__)


class RevealjsHTMLBuilder(StandaloneHTMLBuilder):
    """Sphinx builder class to generate Reveal.js presentation HTML.

    This manage theme path and configure default options.
    """

    name = 'revealjs'
    default_translator_class = RevealjsSlideTranslator
    search = False

    def __init__(self, app):  # noqa: D107
        super().__init__(app)
        self.revealjs_deck = None
        self.builtin_files = set()

        app.add_env_collector(RevealjsImageCollector)
        app.add_env_collector(CSSClassCollector)

    @property
    def revealjs_deck_opts(self) -> dict:
        if self.revealjs_deck:
            return self.revealjs_deck.revealit_el.cdata
        return {}

    def init(self):  # noqa
        # Always add sphinx_revealit plugin
        plugins = [
            RevealjsPlugin(static_resource_uri('sphinx_revealit.js'), 'sphinx_revealit')
        ]

        # Collect user-defined plugins
        for plugin in getattr(self.config, 'revealjs_script_plugins', []):
            # Builtin plugin
            if isinstance(plugin, str):
                self.builtin_files.add(self.get_builtin_plugin_path(plugin))
                plugins.append(RevealjsPlugin(static_resource_uri(plugin + '.js'), plugin))
            else:
                uri = static_resource_uri(plugin['src'])
                plugins.append(RevealjsPlugin(uri, plugin.get('name', '')))

        # Create RevealjsProjectContext
        self.revealjs_context = RevealjsProjectContext(
            4,
            [  # noqa: W503
                static_resource_uri(src)
                for src in getattr(self.config, 'revealjs_script_files', [])
            ],
            getattr(self.config, 'revealjs_script_conf', dict()),
            plugins,
        )

        # Hand over builder configs to html builder.
        setattr(self.config, 'html_static_path', self.config.revealjs_static_path)
        super().init()

    def init_css_files(self) -> None:  # noqa
        self.add_css_file(self.revealjs_context.engine.css_path, priority=0)
        self.add_css_file('tailwind.css', priority=0)
        self.add_css_file(self._get_style_filename(), priority=100)
        self.add_css_file('pygments.css', priority=300)

        for filename in self.get_builder_config('css_files', 'revealjs'):
            self.add_css_file(filename, priority=400)

    def init_js_files(self) -> None:
        for filename, attrs in self.app.registry.js_files:
            self.add_js_file(filename, **attrs)

        for filename, attrs in self.get_builder_config('js_files', 'html'):
            attrs.setdefault('priority', 800)  # User's JSs are loaded after extensions'
            self.add_js_file(filename, **attrs)

    def get_theme_config(self) -> Tuple[str, Dict]:
        """Find and return configuration about theme (name and option params).

        Find theme and merge options.
        """
        theme_name = getattr(self.config, 'revealjs_theme', 'sphinx_revealit')
        theme_options = getattr(self.config, 'revealjs_theme_options', {})
        return theme_name, theme_options

    def get_doc_context(self, docname, body, metatags):
        """Return customized context.

        if source has ``revealjs_deck`` property, add configures.
        """
        ctx = super().get_doc_context(docname, body, metatags)
        ctx['css_files'] = copy.copy(self.css_files)
        ctx['revealjs'] = self.revealjs_context
        return ctx

    def update_page_context(
        self, pagename: str, templatename: str, ctx: Dict, event_arg: Any
    ) -> None:  # noqa
        """Page context gets passed to the templating engine"""

        self.configure_theme(ctx)
        ctx['revealjs_page_confs'] = self.configure_page_script_conf()

        # Deck stylesheet
        if 'stylesheet' in self.revealjs_deck_opts:
            uri = directives.uri(self.revealjs_deck_opts['stylesheet'])
            ctx['css_files'].append(uri)

    def configure_theme(self, ctx: Dict):
        """Find and add theme css from conf and directive."""
        # Use directive or conf
        if 'theme' in self.revealjs_deck_opts:
            theme = self.revealjs_deck_opts['theme']
        else:
            theme = self.config.revealjs_style_theme

        # Build path of stylesheet
        if theme.startswith('http://') or theme.startswith('https://'):
            pass
        elif theme.endswith('.css'):
            theme = f'_static/{theme}'
        else:
            # Builtin theme
            self.builtin_files.add(self.get_builtin_theme_path(theme))
            theme = f'_static/{theme}.css'

        # 0: Reveal.js, 1: Tailwind, 2: Revealit styles
        ctx['css_files'].insert(3, theme)

    def configure_page_script_conf(self) -> List[str]:  # noqa
        if not self.revealjs_deck:
            return []
        configs = []
        if 'conf' in self.revealjs_deck_opts:
            configs.append(self.revealjs_deck_opts['conf'])
        if self.revealjs_deck.content:
            configs.append(self.revealjs_deck.content)
        return configs

    def init_highlighter(self) -> None:
        PygmentsBridge.html_formatter = RjsPygmentsFormatter
        super().init_highlighter()

    def write_genindex(self) -> None:
        pass

    def post_process_images(self, doctree: Node) -> None:
        for node in doctree.traverse(RevealjsNode):
            elm = getattr(node, 'revealit_el', None)

            if elm:
                for img in elm.images.values():
                    if img not in self.env.images:
                        # non-existing URI; let it alone
                        continue
                    self.images[img] = self.env.images[img][1]

        super().post_process_images(doctree)

    @staticmethod
    def _get_builtin_file_path(d, f):
        f = files('sphinx_revealit.res').joinpath(d).joinpath(f)
        if not path.isfile(f):
            raise FileNotFoundError(f)
        return f

    @staticmethod
    def get_builtin_theme_path(name: str):
        return RevealjsHTMLBuilder._get_builtin_file_path('theme', name + '.css')

    @staticmethod
    def get_builtin_plugin_path(name: str):
        return RevealjsHTMLBuilder._get_builtin_file_path('plugin', name + '.js')

    def copy_static_files(self) -> None:
        super().copy_static_files()

        for f in status_iterator(self.builtin_files, 'copying builtin files', 'brown',
                                 len(self.builtin_files), self.app.verbosity,
                                 stringify_func=path.basename):
            shutil.copyfile(f, path.join(self.outdir, '_static', path.basename(f)))

        with progress_message('purging tailwind.css'):
            whitelist = set()

            if hasattr(self.app.env, 'rjs_css_classes'):
                whitelist = self.app.env.rjs_css_classes

            purge = CSSPurge.from_file(files('sphinx_revealit.res').joinpath('tailwind.css'))
            purge.purge_to_file(whitelist, path.join(self.outdir, '_static', 'tailwind.css'))
