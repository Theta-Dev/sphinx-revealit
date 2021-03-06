"""Custom docutils nodes for Reveal.js."""
from docutils import nodes

from sphinx_revealit.elements import RjsElement


class FlagAttribute(object):
    """Flag options for docutils node."""
    pass


class SectionTagRenderer(object):
    """Mix-in class to build attributes combined string."""

    def attributes_str(self):
        """Build string of attributes for Reveal.js sections.

        Catch only keys starting 'data-'.
        Others are skipped.
        """
        pair = []
        for k, v in self.attributes.items():
            if not k.startswith('data-'):
                continue
            if isinstance(v, FlagAttribute):
                pair.append(k)
                continue
            pair.append(f'{k}="{v}"')
        return " ".join(pair)


class RevealjsNode(nodes.Structural, nodes.Element):
    revealit_el: RjsElement = None


class revealjs_deck(RevealjsNode):
    pass


class revealjs_section(SectionTagRenderer, RevealjsNode):
    pass


class revealjs_break(SectionTagRenderer, RevealjsNode):
    pass


class revealjs_fragments(RevealjsNode):
    pass


class revealjs_effect(RevealjsNode):
    pass


class revealjs_div(RevealjsNode):
    pass


class revealjs_title(RevealjsNode):
    pass
