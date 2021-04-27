"""Root module for sphinx-revealjs."""

__version__ = '0.1.0'

from sphinx.application import Sphinx

from sphinx_revealit.builders import RevealjsHTMLBuilder
from sphinx_revealit.directives import (
    RevealjsBreak,
    RevealjsFragments,
    RevealjsSection,
    RevealjsDeck,
    RevealjsId,
)
from sphinx_revealit.nodes import (
    revealjs_break,
    revealjs_fragments,
    revealjs_section,
    revealjs_deck,
)
from sphinx_revealit.themes import get_theme_path
from sphinx_revealit.writers import (
    depart_revealjs_break,
    not_write,
    visit_revealjs_break,
)


def setup(app: Sphinx):
    """Set up function called by Sphinx."""
    app.add_builder(RevealjsHTMLBuilder)
    app.add_node(
        revealjs_section, html=(not_write, not_write), revealjs=(not_write, not_write)
    )
    app.add_node(
        revealjs_break,
        html=(not_write, not_write),
        revealjs=(visit_revealjs_break, depart_revealjs_break),
    )
    app.add_node(
        revealjs_deck, html=(not_write, not_write), revealjs=(not_write, not_write)
    )
    app.add_node(
        revealjs_fragments, html=(not_write, not_write), revealjs=(not_write, not_write)
    )

    app.add_directive('rjs-deck', RevealjsDeck)
    app.add_directive('rjs-break', RevealjsBreak)
    app.add_directive('rjs-section', RevealjsSection)
    app.add_directive('rjs-fragments', RevealjsFragments)
    app.add_directive('rjs-id', RevealjsId)

    app.add_config_value('revealjs_use_section_ids', False, True)
    app.add_config_value('revealjs_static_path', [], True)
    app.add_config_value('revealjs_style_theme', 'black', True)
    app.add_config_value('revealjs_css_files', [], True)
    # app.add_config_value('revealjs_generic_font', 'sans-serif', True)
    app.add_config_value('revealjs_script_files', [], True)
    app.add_config_value('revealjs_script_conf', None, True)
    app.add_config_value('revealjs_script_plugins', [], True)

    app.add_config_value('revealjs_font_body', '', True)
    app.add_config_value('revealjs_font_title', '', True)
    app.add_config_value('revealjs_font_code', '', True)

    app.add_html_theme('sphinx_revealit', str(get_theme_path('sphinx_revealit')))
    return {
        'version': __version__,
        'env_version': 1,
        'parallel_read_safe': False,
    }
