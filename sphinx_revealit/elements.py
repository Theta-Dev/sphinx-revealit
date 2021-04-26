import posixpath

from docutils.parsers.rst import Directive
from sphinx.util import logging

logger = logging.getLogger(__name__)


class Option:
    @staticmethod
    def spec(x):
        return x

    def __init__(self, attr_name):
        self.attr_name = attr_name

    def get_attr(self, val):
        return '%s="%s"' % (self.attr_name, val)

    def get_cls(self, val):
        return ''


class OptionFlag(Option):
    @staticmethod
    def spec(x):
        return True

    def get_attr(self, val):
        return self.attr_name


class OptionConstAttr(Option):
    @staticmethod
    def spec(x):
        return True

    def __init__(self, attr_name, attr_val):
        super().__init__(attr_name)
        self.attr_val = attr_val

    def get_attr(self, val):
        return super().get_attr(self.attr_val)


class OptionClass(Option):
    def get_attr(self, val):
        return ''

    def get_cls(self, val):
        return self.attr_name


class OptionImage(Option):
    pass


class RjsElement:
    tag = ''
    options: dict[str, Option] = {}

    custom_attrs: list[str] = []
    custom_flags: list[str] = []

    required_arguments = 0
    optional_arguments = 0

    def __init__(self, directive: Directive = None):
        self.data = {}
        self.args = []

        if directive and directive.arguments:
            self.args = directive.arguments[0:self.required_arguments + self.optional_arguments]

        if directive and directive.options:
            for key, val in directive.options.items():
                self.data[key] = val

        self.images = {}

    @classmethod
    def option_spec(cls):
        opts = {key: opt.spec for key, opt in cls.options.items()}
        cattrs = {key: Option.spec for key in cls.custom_attrs}
        cflags = {key: OptionFlag.spec for key in cls.custom_flags}

        opts.update(cattrs)
        opts.update(cflags)
        return opts

    def get_attrs(self, imgpath, images):
        attrs = []
        for key, val in self.data.items():
            if key in self.options:
                vstr = val
                if isinstance(self.options[key], OptionImage):
                    if val in self.images:
                        aimg = self.images[val]
                        vstr = posixpath.join(imgpath, images[aimg])

                astr = self.options[key].get_attr(vstr)

                if astr:
                    attrs.append(astr)
        return attrs

    def get_classes(self):
        """Return list of classes"""
        cls = []
        for key, val in self.data.items():
            if key in self.options:
                cstr = self.options[key].get_cls(val)
                if cstr:
                    cls.append(cstr)
        return cls

    def get_opening_tag(self, node, imgpath, images):
        attrs = self.get_attrs(imgpath, images)
        cls = self.get_classes()

        n_cls = node.get('classes', [])
        # ids = node.get('ids', [])

        cls.extend(n_cls)

        # TODO: use ids config option
        # if ids:
        #     attrs.insert(0, 'id="%s"' % ids[0])

        if cls:
            attrs.append('class="%s"' % ' '.join(cls))

        if attrs:
            return '<%s %s>\n' % (self.tag, ' '.join(attrs))
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
    }

    custom_flags = ['notitle']

    def __init__(self, directive: Directive = None):
        super().__init__(directive)

        if directive and directive.options:
            self.notitle = directive.options.get('notitle', False)
        else:
            self.notitle = False
