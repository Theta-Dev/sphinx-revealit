from docutils import nodes
from docutils.transforms import Transform


class RevealjsIdAttribute(Transform):
    """
    Move the "revealjs-id" attribute specified in the "pending" node into the
    immediately following non-comment element.
    """
    default_priority = 210

    applicable_nodes = [
        nodes.literal_block,
        nodes.paragraph,
    ]

    def apply(self):
        pending = self.startnode
        parent = pending.parent
        child = pending
        while parent:
            # Check for appropriate following siblings:
            for index in range(parent.index(child) + 1, len(parent)):
                element = parent[index]
                if element.__class__ in RevealjsIdAttribute.applicable_nodes:
                    element.attributes['revealjs-id'] = pending.details['revealjs-id']
                    pending.parent.remove(pending)
                    return
            else:
                # At end of section or container; apply to sibling
                child = parent
                parent = parent.parent
        error = self.document.reporter.error(
            'No suitable element following "%s" directive'
            % pending.details['directive'],
            nodes.literal_block(pending.rawsource, pending.rawsource),
            line=pending.line)
        pending.replace_self(error)
