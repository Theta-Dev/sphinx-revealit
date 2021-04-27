import json
import posixpath
from typing import List, Dict

from docutils.parsers.rst import Directive
from sphinx.util import logging

logger = logging.getLogger(__name__)


class Attr:
    def out(self, elm: 'RjsElement', env_imgpath, env_images):
        return ''


class AttrVal(Attr):
    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return self.val

    def out(self, elm: 'RjsElement', env_imgpath, env_images):
        return '="%s"' % self.val


class AttrValImage(AttrVal):
    def out(self, elm: 'RjsElement', env_imgpath, env_images):
        if self.val in elm.images:
            aimg = elm.images[self.val]
            imgpath = posixpath.join(env_imgpath, env_images[aimg])
        else:
            imgpath = self.val

        return '="%s"' % imgpath


class Option:
    def spec(self, x):
        return AttrVal(x)

    def __init__(self, attr_name):
        self.attr_name = attr_name

    def apply(self, elm: 'RjsElement', val):
        elm.add_attr(self.attr_name, val)


class OptionConstAttr(Option):
    def spec(self, x):
        return AttrVal(self.attr_val)

    def __init__(self, attr_name, attr_val):
        super().__init__(attr_name)
        self.attr_val = attr_val


class OptionFlag(Option):
    def spec(self, x):
        return Attr()


class OptionClass(Option):
    def apply(self, elm: 'RjsElement', val):
        elm.add_cls(self.attr_name)


class OptionImage(Option):
    def spec(self, x):
        return AttrValImage(x)


class OptionCData(Option):
    def spec(self, x):
        return x

    def apply(self, elm: 'RjsElement', val):
        elm.add_cdata(self.attr_name, val)


class OptionCDataFlag(OptionCData):
    def spec(self, x):
        return True


class OptionCDataJSON(Option):
    def spec(self, x):
        if x is None:
            return x
        try:
            json.loads(x)
        except json.decoder.JSONDecodeError:
            return ''
        return x


class RjsElement:
    tag = ''
    options: Dict[str, Option] = {}

    arguments: List[Option] = []
    n_req_arguments = 0

    def __init__(self, directive: Directive = None):
        self.attrs = {}
        self.classes = []
        self.cdata = {}

        # Image URI -> Actual path (gets populated by collector)
        self.images = {}

        if directive:
            if directive.arguments:
                for val, i in enumerate(directive.arguments[0:len(self.arguments)]):
                    self.arguments[i].apply(self, val)

            if directive.options:
                for key, val in directive.options.items():
                    if key in self.options:
                        self.options[key].apply(self, val)

    @classmethod
    def option_spec(cls):
        return {key: opt.spec for key, opt in cls.options.items()}

    @classmethod
    def n_opt_arguments(cls):
        n = len(cls.arguments) - cls.n_req_arguments
        assert n >= 0
        return n

    def add_attr(self, name, val):
        if val:
            self.attrs[name] = val

    def add_cls(self, cls):
        if cls:
            self.classes.append(cls)

    def add_cdata(self, name, val):
        if val:
            self.cdata[name] = val

    def get_image_uris(self) -> list:
        uris = []

        for attr in self.attrs.values():
            if isinstance(attr, AttrValImage):
                uris.append(attr.val)
        return uris

    def get_opening_tag(self, node, env_imgpath, env_images):
        attrs = self.attrs.copy()
        classes = node.get('classes', []) + self.classes

        if classes:
            attrs['class'] = AttrVal(' '.join(classes))

        if attrs:
            attr_strs = []
            for key, val in attrs.items():
                if isinstance(val, Attr):
                    attr_strs.append(key + val.out(self, env_imgpath, env_images))

            return '<%s %s>\n' % (self.tag, ' '.join(attr_strs))
        else:
            return '<%s>\n' % self.tag

    def get_closing_tag(self):
        return '</%s>\n' % self.tag


class RjsElementSection(RjsElement):
    tag = 'section'
    options = {
        'background-color': Option('data-background-color'),
        'background-image': OptionImage('data-background-image'),
        'background-position': Option('data-background-position'),
        'background-repeat': Option('data-background-repeat'),
        'background-size': Option('data-background-size'),
        'background-video': Option('data-background-video'),
        'background-video-loop': Option('data-background-video-loop'),
        'background-video-muted': Option('data-background-video-muted'),
        'background-opacity': Option('data-background-opacity'),
        'background-iframe': Option('data-background-iframe'),
        'background-interactive': Option('data-background-interactive'),
        'transition': Option('data-transition'),
        'background-transition': Option('data-background-transition'),
        'auto-animate': OptionFlag('data-auto-animate'),
        'auto-animate-easing': Option('data-auto-animate-easing'),
        'auto-animate-no-unmatched': OptionConstAttr('data-auto-animate-unmatched', 'false'),
        'auto-animate-duration': Option('data-auto-animate-duration'),
        'auto-animate-delay': Option('data-auto-animate-delay'),
        'visibility': Option('data-visibility'),

        'notitle': OptionCDataFlag('notitle'),
    }


class RjsElementDeck(RjsElement):
    options = {
        'theme': OptionCData('theme'),
        'conf': OptionCDataJSON('conf'),
        'stylesheet': OptionCData('stylesheet'),
    }
