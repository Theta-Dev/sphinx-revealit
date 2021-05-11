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
        return repr(self.val)

    def __str__(self):
        return str(self.val)

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


class OptionClass(OptionFlag):
    def apply(self, elm: 'RjsElement', val):
        elm.add_cls(self.attr_name)


class OptionCClass(Option):
    def __init__(self):
        super().__init__('')

    def apply(self, elm: 'RjsElement', val):
        classes = str(val).split()
        for c in classes:
            elm.add_cls(c)


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

    def __init__(self, arguments: list = None, options: dict = None):
        self.attrs = {}
        self.classes = []
        self.cdata = {}

        # Image URI -> Actual path (gets populated by collector)
        self.images = {}

        if arguments:
            for i, val in enumerate(arguments[0:len(self.arguments)]):
                self.arguments[i].apply(self, val)

        if options:
            for key, val in options.items():
                if key in self.options:
                    self.options[key].apply(self, val)

    @classmethod
    def from_directive(cls, directive: Directive):
        return cls(directive.arguments, directive.options)

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
                elif val:
                    attr_strs.append('%s="%s"' % (key, str(val)))

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
        'background-video': OptionImage('data-background-video'),
        'background-video-loop': OptionFlag('data-background-video-loop'),
        'background-video-muted': OptionFlag('data-background-video-muted'),
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

        'center': OptionClass('center'),
        'dark': OptionClass('dark-background'),
        'light': OptionClass('light-background'),
        'class': OptionCClass(),

        'notitle': OptionCDataFlag('notitle'),
    }


class RjsElementDeck(RjsElement):
    options = {
        'theme': OptionCData('theme'),
        'conf': OptionCDataJSON('conf'),
        'stylesheet': OptionCData('stylesheet'),
    }


class RjsElementEffect(RjsElement):
    tag = 'div'
    arguments = [OptionCClass()]
    options = {
        'data-id': Option('data-id'),
        'index': Option('data-fragment-index'),
    }

    def __init__(self, arguments: list = None, options: dict = None):
        super().__init__(arguments, options)
        self.add_cls('fragment')


class RjsElementFragments(RjsElement):
    tag = 'div'
    arguments = [OptionCData('animation')]
    options = {
        'stack': OptionClass('r-stack')
    }


class RjsElementDiv(RjsElement):
    tag = 'div'
    arguments = [OptionCClass()]
    options = {
        'data-id': Option('data-id'),
        'style': Option('style'),
    }


class RjsElementBox(RjsElementDiv):
    def __init__(self, arguments: list = None, options: dict = None):
        super().__init__(arguments, options)
        self.classes.append('box')


class RjsElementTitle(RjsElement):
    tag = 'h'
    options = {
        'data-id': Option('data-id'),
        'class': OptionCClass(),
        'style': Option('style'),
    }

    def __init__(self, arguments: list = None, options: dict = None):
        super().__init__(arguments, options)

        if not arguments:
            return

        raw_args = arguments[0]
        args_split = [a.strip() for a in str(raw_args).split('\n', 2)]

        level = 3
        self.content = ''

        if len(args_split) == 1:
            self.content = args_split[0]
        elif len(args_split) == 2:
            try:
                level = int(args_split[0])
                assert level > 0
                assert level <= 6
            except ValueError:
                logger.error('RevealJS title level must be a number')
            except AssertionError:
                logger.error('RevealJS title level not between 1 and 6')

            self.content = args_split[1]

        self.tag = 'h%s' % str(level)

    def get_closing_tag(self):
        return '%s\n%s' % (self.content, super().get_closing_tag())
