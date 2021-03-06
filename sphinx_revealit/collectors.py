import os
from typing import Set

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment
from sphinx.environment.collectors import EnvironmentCollector
from sphinx.locale import __
from sphinx.util import logging

from sphinx_revealit.csspurge import CSSPurge
from sphinx_revealit.elements import RjsElement
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
        static_paths = app.builder.config['html_static_path']

        for node in doctree.traverse(RevealjsNode):
            elm = getattr(node, 'revealit_el', None)

            if isinstance(elm, RjsElement):
                for img_uri in elm.get_image_uris():
                    uri = directives.uri(img_uri)

                    if uri.find('://') != -1 or any(uri.startswith(p) for p in static_paths):
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

                    elm.images[img_uri] = imgpath


class CSSClassCollector(EnvironmentCollector):
    def clear_doc(self, app: Sphinx, env: BuildEnvironment, docname: str) -> None:
        env.rjs_css_classes = set()

    def merge_other(self, app: Sphinx, env: BuildEnvironment,
                    docnames: Set[str], other: BuildEnvironment) -> None:
        env.rjs_css_classes = getattr(env, 'rjs_css_classes', []) | getattr(other, 'rjs_css_classes', [])

    def process_doc(self, app: Sphinx, doctree: nodes.document) -> None:
        if not hasattr(app.env, 'rjs_css_classes'):
            app.env.rjs_css_classes = set()

        for node in doctree.traverse():
            if hasattr(node, 'attributes') and node.attributes.get('classes'):
                app.env.rjs_css_classes.update(node.attributes['classes'])

            if getattr(node, 'tagname', None) == 'raw' and node.attributes.get('format') == 'html':
                app.env.rjs_css_classes.update(CSSPurge.classes_from_html(node.rawsource))

            elm = getattr(node, 'revealit_el', None)

            if isinstance(elm, RjsElement):
                app.env.rjs_css_classes.update(elm.classes)

        pass
