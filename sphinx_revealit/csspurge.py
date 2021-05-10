import re
from typing import List, Iterable


class CSSRule:
    def __init__(self, css: str):
        self.css = css
        self.classes = set()

        no_cmts = CSSPurge.filter_comments(self.css)
        match = re.search(r'([^{]+){', no_cmts)
        if match:
            sels = match.group(1)
            self.classes.update(re.findall(r'\.\\?([\w\d\-_]+)', sels))

    def matches_whitelist(self, whitelist: Iterable):
        if not self.classes:
            return True

        for cls in self.classes:
            if cls in whitelist:
                return True
        return False

    def __str__(self):
        return self.css


class CSSPurge:
    def __init__(self, css: str):
        self.css_rules = self._parse(css)

    @classmethod
    def from_file(cls, css_file):
        with open(css_file, 'r', encoding='utf-8') as f:
            css = f.read()
        return cls(css)

    @staticmethod
    def filter_comments(css: str) -> str:
        output = ''
        state = 0

        for c in css:
            if state < 2:
                output += c

            # Initial state, searching for comment
            if state == 0 and c == '/':
                state = 1
            elif state == 1:
                if c == '*':
                    state = 2
                    output = output[:-2]
                else:
                    state = 0
            # Comment block opened, discarding comment text
            elif state == 2 and c == '*':
                state = 3
            elif state == 3:
                if c == '/':
                    state = 0
                else:
                    state = 2

        return output

    @staticmethod
    def _parse(css: str) -> List[CSSRule]:
        in_comment = False
        bracket_level = 0
        # When 2 chars were parsed (open/close comment), dont parse the second char again
        dont_parse_next = False
        cur_rule = ''
        rules = []

        for i, c in enumerate(css):
            if (i + 1) < len(css):
                nc = css[i + 1]
            else:
                nc = ''

            cur_rule += c

            if dont_parse_next:
                dont_parse_next = False
            elif in_comment:
                if c == '*' and nc == '/':
                    in_comment = False
                    dont_parse_next = True
            else:
                if c == '/' and nc == '*':
                    in_comment = True
                    dont_parse_next = True

                if bracket_level > 0:
                    if c == '}':
                        bracket_level -= 1
                        if bracket_level == 0:
                            rules.append(CSSRule(cur_rule))
                            cur_rule = ''
                else:
                    if c == '{':
                        bracket_level += 1
        return rules

    def _filter_rules(self, whitelist: Iterable) -> List[CSSRule]:
        return list(filter(lambda r: r.matches_whitelist(whitelist), self.css_rules))

    def purge(self, whitelist: Iterable) -> str:
        filtered_rules = self._filter_rules(whitelist)
        return ''.join([str(rule) for rule in filtered_rules])

    def purge_to_file(self, whitelist: Iterable, out_file):
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(self.purge(whitelist))
