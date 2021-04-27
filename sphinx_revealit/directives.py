"""Custom directives for Reveal.js."""

from docutils import nodes
from docutils.parsers.rst import Directive, directives

from sphinx_revealit.elements import RjsElementDeck, RjsElementSection
from sphinx_revealit.nodes import (
    revealjs_break,
    revealjs_fragments,
    revealjs_section,
    revealjs_deck,
)
from sphinx_revealit.transforms import RevealjsIdAttribute


class RevealjsSection(Directive):  # noqa: D101
    option_spec = RjsElementSection.option_spec()

    def run(self):  # noqa: D102
        node = revealjs_section()
        node.revealit_el = RjsElementSection(self)
        return [
            node,
        ]


class RevealjsBreak(Directive):  # noqa: D101
    option_spec = RjsElementSection.option_spec()

    def run(self):  # noqa: D102
        node = revealjs_break()
        node.revealit_el = RjsElementSection(self)
        return [
            node,
        ]


class RevealjsDeck(Directive):  # noqa: D101
    has_content = True
    option_spec = RjsElementDeck.option_spec()

    def run(self):  # noqa: D102
        node = revealjs_deck()
        node.revealit_el = RjsElementDeck(self)
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
