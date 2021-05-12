import json
import re

from pygments.formatters.html import HtmlFormatter
from sphinx import __version__

"""Util as functions for some modules."""


def static_resource_uri(src: str, prefix: str = None) -> str:
    """Build static path of resource."""
    local_prefix = "_static" if prefix is None else prefix
    if src.startswith("http://") or src.startswith("https://"):
        return src
    return f"{local_prefix}/{src}"


def escapejson(string):
    """
    Escape `string`, which should be syntactically valid JSON (this is not
    verified), so that it is safe for inclusion in HTML <script> environments
    and as literal javascript.
    """
    replacements = (
        # Replace forward slashes to prevent '</script>' attacks
        ('/', '\\/'),
        # Replace line separators that are invalid javascript.
        # See http://timelessrepo.com/json-isnt-a-javascript-subset/
        (u'\u2028', '\\u2028'),
        (u'\u2029', '\\u2029'),
    )
    for fro, to in replacements:
        string = string.replace(fro, to)
    return string


def to_json(obj):
    return escapejson(json.dumps(obj, ensure_ascii=False))


class RjsPygmentsFormatter(HtmlFormatter):
    """Format code blocks with the same syntax used by highlight.js"""

    def _wrap_linespans(self, inner):
        i = self.linenostart
        for t, line in inner:
            # Is line of code?
            if t:
                lineno = ''
                if self.linenos:
                    lineno = '<td class="hljs-ln-numbers"><div class="hljs-ln-line hljs-ln-n" data-line-number="%d">%d</div></td>' % (
                        i, i)

                yield 1, '<tr>%s<td class="hljs-ln-code"><div class="hljs-ln-line">%s</div></td></tr>\n' % (
                lineno, line)
                i += 1
            else:
                yield 0, line

    def wrap(self, source, outfile):
        yield 0, '<table class="hljs-ln"><tbody>\n'
        yield from source
        yield 0, '</tbody></table>'

    def format_unencoded(self, tokensource, outfile):
        source = self._format_lines(tokensource)
        source = self._wrap_linespans(source)
        source = self.wrap(source, outfile)

        for t, piece in source:
            outfile.write(piece)


# Sphinx compatibility helpers
def sphinx_version():
    match = re.match(r'(\d+).(\d+).(\d+)', __version__)
    return tuple(int(x) for x in match.groups())


def sphinx_gte_4() -> bool:
    major, _, _ = sphinx_version()
    return major >= 4
