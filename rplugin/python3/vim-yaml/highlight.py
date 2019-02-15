from ruamel.yaml.reader import Reader
from ruamel.yaml.scanner import RoundTripScanner
from ruamel.yaml.resolver import VersionedResolver
from ruamel.yaml import tokens


class Loader(Reader, RoundTripScanner, VersionedResolver):

    def __init__(self, stream, version=None):
        Reader.__init__(self, stream, loader=self)
        RoundTripScanner.__init__(self, loader=self)
        VersionedResolver.__init__(self, version, loader=self)


class Highlighter:

    def __init__(self, start=0, end=0):
        self.start = start
        self.end = end
        self.groups = {
            tokens.ValueToken:             'Special',
            tokens.ScalarToken:            'String',
            tokens.FlowSequenceStartToken: 'Special',
            tokens.FlowSequenceEndToken:   'Special',
            tokens.BlockEntryToken:        'Operator',
            tokens.DocumentStartToken:     'PreProc',
            tokens.DocumentEndToken:       'PreProc',
            # Used for dictionary keys, if they are scalars
            'key':                         'Identifier',
        }

    def highlight(self, document):
        loader = Loader(document)
        token = None
        while True:
            last_token, token = token, loader.get_token()
            if token is None:
                break
            if self.start <= token.start_mark.line <= self.end \
                    or self.start <= token.end_mark.line <= self.end:
                group = None
                if isinstance(last_token, tokens.KeyToken) \
                        and isinstance(token, tokens.ScalarToken):
                    group = self.groups['key']
                elif token.__class__ in self.groups:
                    group = self.groups[token.__class__]
                if group is not None:
                    for region in self.split_region(token):
                        yield (group, *region)

    @staticmethod
    def split_region(token):
        '''Get highlight items for token.

        Neovim can't handle multiline highlights, so
        we must split tokens here when necessary.'''
        difference = token.start_mark.line - token.end_mark.line
        if difference == 0:
            yield (token.start_mark.line,
                   token.start_mark.column,
                   token.end_mark.column)
        else:
            for line in range(token.start_mark.line,
                              token.end_mark.line + 1):
                if line == token.start_mark.line:
                    yield (line, token.start_mark.column, -1)
                elif line == token.end_mark.line:
                    yield (line, 0, token.end_mark.column)
                else:
                    yield (line,)
