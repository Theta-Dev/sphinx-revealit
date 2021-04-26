import json

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
