"""Definition for sphinx custom builder."""
import copy
import logging
from os import path
from typing import Any, Dict, List, Tuple

from docutils.nodes import Node
from docutils.parsers.rst import directives
from importlib_resources import files
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.util import progress_message

from sphinx_revealit.collectors import RevealjsImageCollector, CSSClassCollector
from sphinx_revealit.contexts import RevealjsPlugin, RevealjsProjectContext
from sphinx_revealit.csspurge import CSSPurge
from sphinx_revealit.nodes import RevealjsNode
from sphinx_revealit.utils import static_resource_uri
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

        app.add_env_collector(RevealjsImageCollector)
        app.add_env_collector(CSSClassCollector)

    @property
    def revealjs_deck_opts(self) -> dict:
        if self.revealjs_deck:
            return self.revealjs_deck.revealit_el.cdata
        return {}

    def init(self):  # noqa
        # Create RevealjsProjectContext
        self.revealjs_context = RevealjsProjectContext(
            4,
            [  # noqa: W503
                static_resource_uri(src)
                for src in getattr(self.config, 'revealjs_script_files', [])
            ],
            getattr(self.config, 'revealjs_script_conf', dict()),
            [
                RevealjsPlugin(
                    static_resource_uri(plugin['src']),
                    plugin.get('name', ''),
                    plugin.get('options', '{}').strip(),
                )
                for plugin in getattr(self.config, 'revealjs_script_plugins', [])
            ],
        )
        # Hand over builder configs to html builder.
        setattr(self.config, 'html_static_path', self.config.revealjs_static_path)
        super().init()

    def init_css_files(self) -> None:  # noqa
        self.add_css_file(self.revealjs_context.engine.css_path)
        self.add_css_file('tailwind.css')
        for filename in self.get_builder_config('css_files', 'revealjs'):
            self.add_css_file(filename)

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
            theme = f'_static/{self.revealjs_context.engine.theme_dir}/{theme}.css'
        # index 0: '_static/revealjs4/dist/reveal.css'
        # index 1: theme css file path
        # index 2 or later: other css files
        ctx['css_files'].insert(1, theme)

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
        self.highlighter = None
        self.dark_highlighter = None

    def create_pygments_style_file(self) -> None:
        pass

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

    def copy_static_files(self) -> None:
        super().copy_static_files()

        with progress_message('purging tailwind.css'):
            whitelist = set()

            if hasattr(self.app.env, 'rjs_css_classes'):
                whitelist = self.app.env.rjs_css_classes

            purge = CSSPurge.from_file(files('sphinx_revealit.res').joinpath('tailwind.css'))
            purge.purge_to_file(whitelist, path.join(self.outdir, '_static', 'tailwind.css'))
