from typing import List

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx.directives.code import CodeBlock, LiteralInclude
from sphinx.util import logging

from sphinx_revealit.elements import (
    RjsElementDeck,
    RjsElementSection,
    RjsElementEffect,
    RjsElementFragments,
    RjsElementDiv,
    RjsElementBox,
    RjsElementTitle,
)
from sphinx_revealit.nodes import (
    revealjs_break,
    revealjs_fragments,
    revealjs_section,
    revealjs_deck,
    revealjs_effect,
    revealjs_div,
    revealjs_title,
)
from sphinx_revealit.transforms import RevealjsIdAttribute

logger = logging.getLogger(__name__)


class RevealjsSection(Directive):
    option_spec = RjsElementSection.option_spec()

    def run(self) -> List[nodes.Node]:
        node = revealjs_section()
        node.revealit_el = RjsElementSection.from_directive(self)
        return [node]


class RevealjsBreak(Directive):  # noqa: D101
    option_spec = RjsElementSection.option_spec()

    def run(self) -> List[nodes.Node]:
        node = revealjs_break()
        node.revealit_el = RjsElementSection.from_directive(self)
        return [node]


class RevealjsDeck(Directive):  # noqa: D101
    has_content = True
    option_spec = RjsElementDeck.option_spec()

    def run(self) -> List[nodes.Node]:
        node = revealjs_deck()
        node.revealit_el = RjsElementDeck.from_directive(self)
        node.content = "\n".join(self.content or [])
        return [node]


class RevealjsEffect(Directive):
    has_content = True
    option_spec = RjsElementEffect.option_spec()
    required_arguments = RjsElementEffect.n_req_arguments
    optional_arguments = RjsElementEffect.n_opt_arguments()

    def run(self) -> List[nodes.Node]:
        node = revealjs_effect()
        node.revealit_el = RjsElementEffect.from_directive(self)

        if self.content:
            self.state.nested_parse(self.content, self.content_offset, node)

        return [node]


class RevealjsEffects(Directive):
    has_content = True
    required_arguments = 1
    final_argument_whitespace = True
    option_spec = {'data-id': directives.unchanged}

    def run(self) -> List[nodes.Node]:
        root_node = revealjs_effect()
        cur_node = root_node

        def add_element(args, opts):
            if cur_node.revealit_el:
                new_node = revealjs_effect()
                new_node.revealit_el = RjsElementEffect(args, opts)
                cur_node.children.append(new_node)
                return new_node
            else:
                if 'data-id' in self.options:
                    opts['data-id'] = self.options['data-id']

                cur_node.revealit_el = RjsElementEffect(args, opts)
                return cur_node

        if self.arguments[0]:
            args = self.arguments[0].split()
            for a in args:
                argdata = a.split('.')
                if len(argdata) == 2:
                    index, anim = argdata
                    options = {'index': index}
                else:
                    anim = argdata[0]
                    options = {}

                cur_node = add_element([anim], options)
        else:
            cur_node = add_element([], {})

        if self.content:
            self.state.nested_parse(self.content, self.content_offset, cur_node)

        return [root_node]


class RevealjsFragments(Directive):  # noqa: D101
    has_content = True
    option_spec = RjsElementFragments.option_spec()
    required_arguments = RjsElementFragments.n_req_arguments
    optional_arguments = RjsElementFragments.n_opt_arguments()

    def run(self) -> List[nodes.Node]:
        node = revealjs_fragments()
        node.revealit_el = RjsElementFragments.from_directive(self)

        if self.content:
            self.state.nested_parse(self.content, self.content_offset, node)

        def transform_children(node: nodes.Node, animation):
            to_transform = [
                nodes.paragraph, nodes.list_item, nodes.image, revealjs_div,
            ]

            if hasattr(node, 'children'):
                for i, child in enumerate(node.children):
                    if child.__class__ in to_transform:
                        child['classes'].append('fragment')

                        if animation:
                            child['classes'].append(animation)
                    else:
                        transform_children(child, animation)

        animation = node.revealit_el.cdata.get('animation', None)

        transform_children(node, animation)
        return [node]


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

    def run(self) -> List[nodes.Node]:
        try:
            rjs_id = self.arguments[0]
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
                node.attributes['revealjs-id'] = rjs_id
            node_list.extend(container.children)
        else:
            pending = nodes.pending(
                RevealjsIdAttribute,
                {'revealjs-id': rjs_id, 'directive': self.name},
                self.block_text)
            self.state_machine.document.note_pending(pending)
            node_list.append(pending)
        return node_list


CODE_BLOCK_OPTIONS = {
    'data-id': directives.unchanged,
    'index': directives.unchanged,
}


def code_block_pre(self):
    hl_lines = self.options.get('emphasize-lines')
    if hl_lines:
        self.options['emphasize-lines'] = hl_lines.replace('|', ',')
    return hl_lines


def code_block_post(self, nodes, hl_lines):
    for option, attr in (('data-id', 'revealjs-id'), ('index', 'revealjs-index')):
        val = self.options.get(option)
        if val:
            nodes[0].attributes[attr] = val

    nodes[0].attributes['revealjs-hl-lines'] = hl_lines
    return nodes


class RevealjsCode(CodeBlock):
    option_spec = {
        **CodeBlock.option_spec,
        **CODE_BLOCK_OPTIONS,
    }

    def run(self) -> List[nodes.Node]:
        hl_lines = code_block_pre(self)
        nodes = super().run()
        return code_block_post(self, nodes, hl_lines)


class RevealjsLiteralInclude(LiteralInclude):
    option_spec = {
        **LiteralInclude.option_spec,
        **CODE_BLOCK_OPTIONS,
    }

    def run(self) -> List[nodes.Node]:
        hl_lines = code_block_pre(self)
        nodes = super().run()
        return code_block_post(self, nodes, hl_lines)


class RevealjsDiv(Directive):
    has_content = True
    option_spec = RjsElementDiv.option_spec()
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True

    def run(self) -> List[nodes.Node]:
        node = revealjs_div()
        node.revealit_el = RjsElementDiv.from_directive(self)

        if self.content:
            self.state.nested_parse(self.content, self.content_offset, node)

        return [node]


class RevealjsBox(Directive):
    has_content = True
    option_spec = RjsElementBox.option_spec()
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True

    def run(self) -> List[nodes.Node]:
        node = revealjs_div()
        node.revealit_el = RjsElementBox.from_directive(self)

        if self.content:
            self.state.nested_parse(self.content, self.content_offset, node)

        return [node]


class RevealjsTitle(Directive):
    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True

    def run(self) -> List[nodes.Node]:
        node = revealjs_title()
        node.revealit_el = RjsElementTitle.from_directive(self)

        if self.content:
            self.state.nested_parse(self.content, self.content_offset, node)

        return [node]
