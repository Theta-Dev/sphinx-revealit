"""Custom directives for Reveal.js."""
import json

from docutils import nodes
from docutils.parsers.rst import Directive, directives

from sphinx_revealit.elements import RjsElementSection
from sphinx_revealit.nodes import (
    FlagAttribute,
    revealjs_break,
    revealjs_fragments,
    revealjs_section,
    revealjs_deck,
)
from sphinx_revealit.transforms import RevealjsIdAttribute


def raw_json(argument):
    """Type of direction attribute."""
    if argument is None:
        return directives.unchanged(argument)
    try:
        json.loads(argument)
    except json.decoder.JSONDecodeError:
        return ""
    return argument


REVEALJS_SECTION_ATTRIBUTES = {
    # Color backgrounds
    "data-background-color": directives.unchanged,
    # Image backgrounds
    "data-background-image": directives.unchanged,
    "data-background-position": directives.unchanged,
    "data-background-repeat": directives.unchanged,
    # Video backgrounds
    "data-background-video": directives.unchanged,
    "data-background-video-loop": directives.unchanged,
    "data-background-video-muted": directives.unchanged,
    # Image/Video backgrounds
    "data-background-size": directives.unchanged,
    "data-background-opacity": directives.unchanged,
    # Iframe backgrounds
    "data-background-iframe": directives.unchanged,
    "data-background-interactive": lambda x: FlagAttribute(),
    # Transition
    "data-transition": directives.unchanged,
    "data-background-transition": directives.unchanged,
    "data-auto-animate": lambda x: FlagAttribute(),
}


class RevealjsSection(Directive):  # noqa: D101
    option_spec = RjsElementSection.option_spec()

    def run(self):  # noqa: D102
        node = revealjs_section()
        # node.attributes = self.options
        node.revealit_el = RjsElementSection(self)
        return [
            node,
        ]


class RevealjsBreak(Directive):  # noqa: D101
    option_spec = dict(
        # if it is set, next section does not display title
        notitle=lambda x: FlagAttribute(),
        **REVEALJS_SECTION_ATTRIBUTES
    )

    def run(self):  # noqa: D102
        node = revealjs_break()
        node.attributes = self.options
        return [
            node,
        ]


class RevealjsDeck(Directive):  # noqa: D101
    has_content = True

    option_spec = {
        "theme": directives.unchanged,
        "google_font": directives.unchanged,
        "conf": raw_json,
    }

    def run(self):  # noqa: D102
        node = revealjs_deck()
        node.attributes = self.options
        node.content = "\n".join(self.content or [])
        return [
            node,
        ]


class RevealjsFragments(Directive):  # noqa: D101
    has_content = True

    def run(self):  # noqa: D102
        node = revealjs_fragments()
        if self.content:
            self.state.nested_parse(self.content, self.content_offset, node)
        # TODO: Parameter ?
        for child in node.children[0].children:
            child["classes"].append("fragment")
        return [
            node,
        ]


class RevealjsId(Directive):
    """
    Set the reveal.js data-id on the directive content or the next element.
    When applied to the next element, a "pending" element is inserted, and a
    transform does the work later.
    """

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = True

    def run(self):
        try:
            rjs_id = directives.class_option(self.arguments[0])
        except ValueError:
            raise self.error(
                'Invalid class attribute value for "%s" directive: "%s".'
                % (self.name, self.arguments[0]))
        node_list = []
        if self.content:
            container = nodes.Element()
            self.state.nested_parse(self.content, self.content_offset,
                                    container)
            for node in container:
                node['revealjs-id'] = rjs_id
            node_list.extend(container.children)
        else:
            pending = nodes.pending(
                RevealjsIdAttribute,
                {'revealjs-id': rjs_id, 'directive': self.name},
                self.block_text)
            self.state_machine.document.note_pending(pending)
            node_list.append(pending)
        return node_list
