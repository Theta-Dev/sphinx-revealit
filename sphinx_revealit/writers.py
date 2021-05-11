"""Custom write module."""
from docutils import nodes
from docutils.nodes import Node
from sphinx.writers.html5 import HTML5Translator

from sphinx_revealit.elements import RjsElementSection
from sphinx_revealit.nodes import RevealjsNode, revealjs_break


def has_child_sections(node: nodes.Element, name: str):
    """Search has specified section in children."""
    nodes = set([n.tagname for n in node.children])
    return name in nodes


def find_child_section(node: nodes.Element, name: str):
    """Search and return first specified section in children."""
    for n in node.children:
        if n.tagname == name:
            return n
    return None


class RevealjsSlideTranslator(HTML5Translator):
    """Translate Reveal.js HTML class."""

    permalink_text = False

    def __init__(self, builder, *args):  # noqa: D107
        super().__init__(builder, *args)
        self.builder.add_permalinks = False
        self._proc_first_on_section = False

    def unknown_visit(self, node: Node) -> None:
        pass

    def visit_section(self, node: nodes.section):
        """Begin ``section`` node.

        - Find first ``revealjs_section`` node and build attributes string.
        - When enter next section, nest level.
        """
        self.section_level += 1
        meta = find_child_section(node, 'revealjs_section')
        if meta is not None:
            elm = meta.revealit_el
        else:
            elm = RjsElementSection()

        # if node.attributes.get('ids') and self.config.revealjs_use_section_ids:
        #     attrs += ' id='{}''.format(node.attributes['ids'][-1])
        if self.section_level == 1:
            self.builder.revealjs_deck = find_child_section(node, 'revealjs_deck')
            self._proc_first_on_section = True
            self.body.append(elm.get_opening_tag(node, self.builder.imgpath, self.builder.images))
            return
        if self._proc_first_on_section:
            self._proc_first_on_section = False
            self.body.append(elm.get_closing_tag())

        if has_child_sections(node, 'section'):
            self._proc_first_on_section = True
            self.body.append('<section>\n')
        self.body.append(elm.get_opening_tag(node, self.builder.imgpath, self.builder.images))

    def depart_section(self, node: nodes.section):
        """End ``section``.

        Dedent section level
        """
        self.section_level -= 1
        if self.section_level >= 1:
            self.body.append('</section>\n')

    def visit_title(self, node):
        if isinstance(node.parent, nodes.section):
            section_meta = find_child_section(node.parent, 'revealjs_section')

            if section_meta:
                if section_meta.revealit_el.cdata.get('notitle'):
                    self.body.append('<!--')
                    self.context.append('-->\n')
                    return

        super().visit_title(node)

    def visit_comment(self, node: nodes.comment):
        """Begin ``comment`` node.

        comment node render as speaker note.
        """
        self.body.append('<aside class="notes">\n')

    def depart_comment(self, node: nodes.comment):
        """End ``comment`` node.

        Close speaker note.
        """
        self.body.append('</aside>\n')

    def visit_literal_block(self, node: nodes.literal_block):
        """Begin ``literal_block``"""
        if node.rawsource != node.astext():
            # most probably a parsed-literal block -- don't highlight
            return super().visit_literal_block(node)

        lang = node.get('language', 'default')
        linenos = node.get('linenos', False)
        highlight_args = node.get('highlight_args', {})

        hl_lines = highlight_args.get('hl_lines')
        if node.attributes.get('revealjs-hl-lines'):
            hl_lines = node.attributes['revealjs-hl-lines']

        opts = self.config.highlight_options.get(lang, {})

        highlighted = self.highlighter.highlight_block(
            node.rawsource, lang, opts=opts, linenos=bool(linenos),
            location=node
        )

        pre_attrs = {
            'CLASS': 'highlight highlight-%s notranslate"' % lang,
        }
        code_attrs = {
            'CLASS': 'hljs',
        }

        if node.attributes.get('revealjs-id'):
            pre_attrs['DATA-ID'] = node.attributes['revealjs-id']
        if hl_lines:
            code_attrs['DATA-LINE-NUMBERS'] = hl_lines
        if node.attributes.get('revealjs-index'):
            code_attrs['DATA-FRAGMENT-INDEX'] = node.attributes['revealjs-index']

        starttag = self.starttag(node, 'pre', suffix='', **pre_attrs)
        code_tag = self.starttag({}, 'code', suffix='', **code_attrs)

        self.body.append(starttag + code_tag + highlighted + '</code></pre>\n')
        raise nodes.SkipNode

    def visit_paragraph(self, node: nodes.paragraph):
        if node.attributes.get('revealjs-id'):
            self.body.append('<p data-id="%s">' % node.attributes['revealjs-id'])
        else:
            super(RevealjsSlideTranslator, self).visit_paragraph(node)


def not_write(self, node):
    """visit/depart function for declare 'no write'."""
    pass


def visit_revealjs_break(self, node: revealjs_break):
    """Close current section."""
    elm = node.revealit_el
    self.body.append(elm.get_closing_tag())


def depart_revealjs_break(self, node: revealjs_break):
    """Open as next section.

    If node does not have attribute 'notitle',
    render title from current original section.
    """
    attrs = node.attributes_str()
    self.body.append(f'<section {attrs}>\n')
    if 'notitle' not in node.attributes:
        title = find_child_section(node.parent, 'title')
        self.body.append(f'<h{self.section_level}>')
        self.body.append(title.children[0])
        self.body.append(f'</h{self.section_level}>')
        self.body.append('\n')


def visit_revealjs_element(self, node: RevealjsNode):
    elm = node.revealit_el
    self.body.append(elm.get_opening_tag(node, self.builder.imgpath, self.builder.images))


def depart_revealjs_element(self, node: RevealjsNode):
    elm = node.revealit_el
    self.body.append(elm.get_closing_tag())
