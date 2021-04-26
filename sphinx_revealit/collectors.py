import os
from typing import Set

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment
from sphinx.environment.collectors import EnvironmentCollector
from sphinx.locale import __
from sphinx.util import logging

from sphinx_revealit.elements import OptionImage
from sphinx_revealit.nodes import RevealjsNode

logger = logging.getLogger(__name__)


class RevealjsImageCollector(EnvironmentCollector):
    def clear_doc(self, app: Sphinx, env: BuildEnvironment, docname: str) -> None:
        env.images.purge_doc(docname)

    def merge_other(self, app: Sphinx, env: BuildEnvironment,
                    docnames: Set[str], other: BuildEnvironment) -> None:
        env.images.merge_other(docnames, other.images)

    def process_doc(self, app: Sphinx, doctree: nodes.document) -> None:
        docname = app.env.docname

        for node in doctree.traverse(RevealjsNode):
            elm = getattr(node, 'revealit_el', None)

            if elm:
                for key, val in elm.data.items():
                    if isinstance(elm.options.get(key), OptionImage):
                        uri = directives.uri(val)

                        if uri.find('://') != -1 or uri.startswith('_static'):
                            continue
                        # Update imgpath to a relative path from srcdir
                        # from a relative path from current document.

                        imgpath, _ = app.env.relfn2path(uri, docname)

                        app.env.dependencies[docname].add(imgpath)
                        if not os.access(os.path.join(app.srcdir, imgpath), os.R_OK):
                            logger.warning(__('image file not readable: %s') % imgpath, type='image',
                                           location=node, subtype='not_readable')
                            continue
                        app.env.images.add_file(docname, imgpath)

                        elm.images[val] = imgpath
